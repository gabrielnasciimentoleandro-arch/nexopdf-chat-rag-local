"""Provedores de embeddings locais, com opção leve e semântica."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import numpy as np
from scipy.sparse import spmatrix
from sklearn.feature_extraction.text import TfidfVectorizer

Matrix = np.ndarray | spmatrix


class Embedder(Protocol):
    name: str

    def fit_transform(self, texts: Sequence[str]) -> Matrix: ...

    def transform(self, texts: Sequence[str]) -> Matrix: ...


class TfidfEmbedder:
    """Vetores esparsos TF-IDF: rápidos, privados e sem downloads de modelo."""

    name = "TF-IDF local"

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
            norm="l2",
            max_features=30_000,
        )

    def fit_transform(self, texts: Sequence[str]) -> Matrix:
        if not texts:
            raise ValueError("Não há textos para indexar.")
        return self.vectorizer.fit_transform(texts)

    def transform(self, texts: Sequence[str]) -> Matrix:
        return self.vectorizer.transform(texts)


class FastEmbedder:
    """Embeddings neurais multilíngues via ONNX, carregados sob demanda."""

    name = "MiniLM multilíngue"
    default_model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self, model_name: str | None = None) -> None:
        try:
            from fastembed import TextEmbedding
        except ImportError as exc:
            raise RuntimeError(
                "Instale requirements-semantic.txt para usar embeddings semânticos."
            ) from exc
        self.model = TextEmbedding(model_name=model_name or self.default_model)

    def fit_transform(self, texts: Sequence[str]) -> Matrix:
        return self._encode(texts)

    def transform(self, texts: Sequence[str]) -> Matrix:
        return self._encode(texts)

    def _encode(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 0), dtype=np.float32)
        vectors = np.vstack(list(self.model.embed(list(texts)))).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.maximum(norms, 1e-12)


def build_embedder(mode: str) -> Embedder:
    """Cria o provedor solicitado por um identificador estável."""
    if mode == "semantic":
        return FastEmbedder()
    if mode == "tfidf":
        return TfidfEmbedder()
    raise ValueError(f"Modo de embeddings desconhecido: {mode}")
