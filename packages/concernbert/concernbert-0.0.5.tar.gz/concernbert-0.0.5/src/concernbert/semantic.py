import enum
import itertools as it
import logging
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import nltk
import numpy as np
from tree_sitter_languages import get_language, get_parser
from gensim.corpora import Dictionary
from gensim.matutils import sparse2full
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models.lsimodel import LsiModel
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tree_sitter import Node

from concernbert.embeddings import Embedder

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
logging.getLogger("gensim").setLevel(logging.ERROR)

_STOP_WORDS = set(stopwords.words("english"))
_STEMMER = PorterStemmer()

_JAVA_LANGUAGE = get_language("java")
_JAVA_PARSER = get_parser("java")
_JAVA_QUERY = _JAVA_LANGUAGE.query(
    """
    (class_declaration
        name: (identifier) @name) @class
    (record_declaration
        name: (identifier) @name) @record
    (enum_declaration
        name: (identifier) @name) @enum
    (interface_declaration
        name: (identifier) @name) @interface
    (annotation_type_declaration
        name: (identifier) @name) @annotation
    (method_declaration
        name: (identifier) @name) @method
    (constructor_declaration
        name: (identifier) @name) @constructor
    (field_declaration
        declarator: (variable_declarator
            name: (identifier) @name)) @field
    (line_comment) @line_comment
    (block_comment) @block_comment
    (identifier) @identifier
    (type_identifier) @type_identifier
"""
)


class _CaptureKind(enum.Enum):
    """Different capture kinds found in `JAVA_QUERY`."""

    # Types
    ANNOTATION = 1
    CLASS = 2
    ENUM = 3
    INTERFACE = 4
    RECORD = 5

    # Functions
    CONSTRUCTOR = 6
    METHOD = 7

    # Fields
    FIELD = 8

    # Block comment (includes both normal block comments and doc comments)
    LINE_COMMENT = 9
    BLOCK_COMMENT = 10

    # Identifiers
    NAME = 11
    IDENTIFIER = 12
    TYPE_IDENTIFIER = 13

    def is_name(self) -> bool:
        return self == _CaptureKind.NAME

    def is_field(self) -> bool:
        return self == _CaptureKind.FIELD

    def is_function(self) -> bool:
        return self == _CaptureKind.CONSTRUCTOR or self == _CaptureKind.METHOD

    def is_entity(self) -> bool:
        return self.is_field() or self.is_function()

    def is_comment(self) -> bool:
        return self == _CaptureKind.LINE_COMMENT or self == _CaptureKind.BLOCK_COMMENT

    def is_identifier(self) -> bool:
        return (
            self == _CaptureKind.NAME
            or self == _CaptureKind.IDENTIFIER
            or self == _CaptureKind.TYPE_IDENTIFIER
        )

    def is_human_text(self) -> bool:
        "Is this text that does not contain Java keywords, operators, etc.?"
        return self.is_comment() or self.is_identifier()


@dataclass(frozen=True)
class _Capture:
    node: Node
    kind: _CaptureKind


def _iter_ancestors(node: Node) -> Iterable[Node]:
    curr: Node | None = node.parent
    while curr is not None:
        yield curr
        curr = curr.parent


def _to_parents_dict(nodes: list[Node]) -> dict[Node, Node | None]:
    """Given a list of nodes, return a child-to-parent mapping."""
    parents: dict[Node, Node | None] = dict()
    ids: set[int] = set(n.id for n in nodes)
    for node in nodes:
        parents[node] = next((a for a in _iter_ancestors(node) if a.id in ids), None)
    return parents


def _to_children_dict(
    parents: dict[Node, Node | None],
) -> dict[Node | None, list[Node]]:
    """Return a parent-to-children mapping given a child-to-parent mapping."""
    children: dict[Node | None, list[Node]] = {None: []}
    for node in parents:
        children[node] = []
    for child, parent in parents.items():
        children[parent].append(child)
    for lst in children.values():
        lst.sort(key=lambda n: n.byte_range)
    return children


def _to_names_dict(
    captures: dict[int, _Capture], children: dict[Node | None, list[Node]]
) -> dict[Node, str]:
    names: dict[Node, str] = dict()
    for capture in captures.values():
        nodes = children[capture.node]
        try:
            name = next(n for n in nodes if captures[n.id].kind.is_name())
            names[capture.node] = name.text.decode()
        except StopIteration:
            continue
    return names


def _iter_descendants(
    children: dict[Node | None, list[Node]], parent: Node | None
) -> Iterable[Node]:
    descendants: list[Node] = children.get(parent, [])
    while True:
        if len(descendants) == 0:
            break
        yield from descendants
        descendants.clear()
        for node in descendants:
            descendants.extend(children.get(node, []))


def _find_captures(content_bytes: bytes) -> dict[int, _Capture]:
    captures: dict[int, _Capture] = dict()
    tree = _JAVA_PARSER.parse(content_bytes)
    for node, capture_name in _JAVA_QUERY.captures(tree.root_node):
        capture = _Capture(node, _CaptureKind[capture_name.upper()])
        if (c := captures.get(node.id)) and c.kind.value < capture.kind.value:
            continue
        captures[node.id] = capture
    return captures


def _join_singles(terms: list[str]) -> list[str]:
    ret = []
    joined_term = []
    for t in terms:
        if len(t) == 1:
            joined_term.append(t[0])
        elif len(t) > 1:
            if len(joined_term) > 0:
                ret.append("".join(joined_term))
                joined_term = []
            ret.append(t)
    if len(joined_term) > 0:
        ret.append("".join(joined_term))
    return ret


def _split_camel(name: str) -> list[str]:
    if name.isupper():
        return [name.lower()]
    indices = [i for i, x in enumerate(name) if x.isupper() or x.isnumeric()]
    indices = [0] + indices + [len(name)]
    return _join_singles([name[a:b].lower() for a, b in it.pairwise(indices)])


def _strip_doubleslash(token: str) -> str:
    if token.startswith("//"):
        return token[2:]
    return token


def _tokenize(text: str) -> list[str]:
    # First break up by whitespace
    tokens = (_strip_doubleslash(z) for z in text.split())

    # Then break up identifiers
    by_forward_slashes = it.chain(*(z.split("/") for z in tokens))
    by_backward_slashes = it.chain(*(z.split("\\") for z in by_forward_slashes))
    by_dashes = it.chain(*(z.split("-") for z in by_backward_slashes))
    by_underscores = it.chain(*(z.split("_") for z in by_dashes))
    by_camel = it.chain(*(_split_camel(z) for z in by_underscores))

    # Run each keyword through an English tokenizer and stemmer
    by_english = it.chain(*(nltk.word_tokenize(t) for t in by_camel))
    words = (t for t in by_english if t.isalpha() and t not in _STOP_WORDS)
    return [_STEMMER.stem(i) for i in words]


@dataclass
class MethodDoc:
    method_text: str
    preceding_comments_tokens: list[str]
    entity_tokens: list[str]


def find_method_docs(content: str) -> list[MethodDoc]:
    "Return a list of methods where each method is a list of processed tokens."
    content_bytes = content.encode()
    captures = _find_captures(content_bytes)
    nodes = [c.node for c in captures.values()]
    parents = _to_parents_dict(nodes)
    children = _to_children_dict(parents)

    # A "top" is a node that contains at least one function
    tops = {parents[n] for n in nodes if captures[n.id].kind.is_function()}

    # Build a document for each method in the source code
    docs: list[MethodDoc] = []
    for top in tops:
        members = children[top]
        members.sort(key=lambda m: m.byte_range)
        for i, member in enumerate(members):
            capture = captures[member.id]
            if not capture.kind.is_function():
                continue

            # Collect preceding comments
            preceding_comments: list[str] = []
            for j in range(i - 1, 0, -1):
                node = members[j]
                if not captures[node.id].kind.is_comment():
                    break
                preceding_comments.append(node.text.decode())
            preceding_comments.reverse()

            # Collect tokens of preceding comments
            preceding_comments_tokens: list[str] = []
            for comment in preceding_comments:
                preceding_comments_tokens.extend(_tokenize(comment))

            # Collect tokens from descendant "human text"
            entity_tokens: list[str] = []
            for desc in _iter_descendants(children, member):
                if captures[desc.id].kind.is_human_text():
                    entity_tokens.extend(_tokenize(desc.text.decode()))

            # Create MethodDoc
            method_text = member.text.decode()
            docs.append(
                MethodDoc(method_text, preceding_comments_tokens, entity_tokens)
            )
    return docs


@dataclass
class EntityDoc:
    name: str
    kind: str
    lineno: int
    text: str


def find_entity_docs(content: str) -> list[list[EntityDoc]]:
    content_bytes = content.encode()
    captures = _find_captures(content_bytes)
    nodes = [c.node for c in captures.values()]
    parents = _to_parents_dict(nodes)
    children = _to_children_dict(parents)
    names = _to_names_dict(captures, children)

    # A "top" is a node that contains at least one entity
    tops = [parents[n] for n in nodes if captures[n.id].kind.is_entity()]
    tops = [t for t in set(tops) if t is not None]
    tops.sort(key=lambda t: t.byte_range)

    # Build a document for each method in the source code
    docs_by_top: list[list[EntityDoc]] = list()
    for top in tops:
        docs: list[EntityDoc] = []
        for member in children[top]:
            if member.is_missing or member.has_error:
                continue
            capture = captures[member.id]
            if not capture.kind.is_entity():
                continue
            name = names[member]
            kind = capture.kind.name
            lineno = member.range.start_point[0] + 1
            text = member.text.decode()
            docs.append(EntityDoc(name, kind, lineno, text))
        if len(docs) > 1:
            docs_by_top.append(docs)
    return docs_by_top


class MyCorpus:
    def __init__(
        self,
        name: str,
        cache_dir: str,
        files: Iterable[tuple[str, str]],
        *,
        preceding_comments: bool,
    ) -> None:
        self.name = name
        cache_path = Path(cache_dir, name, "corpus.pkl")
        if cache_path.exists():
            with cache_path.open("rb") as f:
                self._method_docs, self._files = pickle.load(f)
        else:
            self._method_docs: list[MethodDoc] = []
            self._files: dict[str, list[int]] = {}
            for filename, content in files:
                method_docs = find_method_docs(content)
                n = len(self._method_docs)
                indices = list(range(n, n + len(method_docs)))
                self._method_docs.extend(method_docs)
                self._files[filename] = indices
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with cache_path.open("wb") as f:
                pickle.dump((self._method_docs, self._files), f)
        self.docs: list[list[str]] = []
        self.preceding_comments = preceding_comments
        for method_doc in self._method_docs:
            tokens: list[str] = []
            if preceding_comments:
                tokens.extend(method_doc.preceding_comments_tokens)
            tokens.extend(method_doc.entity_tokens)
            self.docs.append(tokens)
        self.vocab = Dictionary(self.docs)
        self.corpus = [self.vocab.doc2bow(d) for d in self.docs]

    def cache_key(self) -> str:
        if self.preceding_comments:
            return "C"
        return "NC"

    def get_tokens(self, method_doc: MethodDoc) -> list[str]:
        tokens: list[str] = []
        if self.preceding_comments:
            tokens.extend(method_doc.preceding_comments_tokens)
        tokens.extend(method_doc.entity_tokens)
        return tokens

    def get_doc_indices(self, filename: str) -> list[int]:
        return self._files[filename]

    def get_doc(self, index: int) -> MethodDoc:
        return self._method_docs[index]

    def to_tagged_docs(self) -> list[TaggedDocument]:
        return [TaggedDocument(d, [i]) for i, d in enumerate(self.docs)]


class MyLsi:
    def __init__(self, corpus: MyCorpus, dim: int, cache_dir: str):
        self._corpus = corpus
        cache_path = Path(
            cache_dir, corpus.name, f"lsi-{dim}-{corpus.cache_key()}.model"
        )
        if cache_path.exists():
            self._lsi = LsiModel.load(str(cache_path))
            return
        self._lsi = LsiModel(
            corpus.corpus, id2word=corpus.vocab, num_topics=dim, random_seed=42
        )
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._lsi.save(str(cache_path))

    def embed(self, filename: str) -> np.ndarray:
        vecs: list[np.ndarray] = []
        for doc_index in self._corpus.get_doc_indices(filename):
            bow = self._to_bow(self._corpus.get_tokens(self._corpus.get_doc(doc_index)))
            vecs.append(sparse2full(self._lsi[bow], length=self._lsi.num_topics))
        return np.array(vecs)

    def _to_bow(self, doc: list[str]) -> list[tuple[int, int]]:
        return self._corpus.vocab.doc2bow(doc)  # type: ignore


class MyDoc2Vec:
    def __init__(self, corpus: MyCorpus, dim: int, cache_dir: str):
        self._corpus = corpus
        cache_path = Path(
            cache_dir, corpus.name, f"d2v-{dim}-{corpus.cache_key()}.model"
        )
        if cache_path.exists():
            self._doc2vec: Doc2Vec = Doc2Vec.load(str(cache_path))  # type: ignore
            return
        docs = self._corpus.to_tagged_docs()
        self._doc2vec = Doc2Vec(
            docs, vector_size=dim, min_count=1, workers=4, seed=42
        )
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._doc2vec.save(str(cache_path))

    def embed(self, filename: str) -> np.ndarray:
        indices = self._corpus.get_doc_indices(filename)
        return self._doc2vec[indices]


class MyBert:
    def __init__(self, corpus: MyCorpus, embedder: Embedder):
        self._corpus = corpus
        self._embedder = embedder

    def embed(self, filename: str) -> np.ndarray:
        indices = self._corpus.get_doc_indices(filename)
        texts = [self._corpus.get_doc(i).method_text for i in indices]
        embeddings = self._embedder.embed(texts, pbar=False)
        vecs: list[np.ndarray] = []
        for text in texts:
            vecs.append(embeddings[text])
        return np.array(vecs)
