"""Índice vetorial em memória com busca por similaridade de cosseno."""

from __future__ import annotations

import numpy as np
from scipy.sparse import issparse

from .embeddings import Embedder, Matrix
from .models import DocumentChunk, SearchResult


class InMemoryVectorStore:
    """Armazena embeddings localmente durante a sessão."""

    def __init__(self, embedder: Embedder) -> None:
        self.embedder = embedder
        self.chunks: list[DocumentChunk] = []
        self.matrix: Matrix | None = None

    def index(self, chunks: list[DocumentChunk]) -> None:
        if not chunks:
            raise ValueError("Nenhum trecho com texto foi encontrado nos documentos.")
        self.chunks = list(chunks)
        self.matrix = self.embedder.fit_transform([chunk.text for chunk in chunks])

    def search(
        self,
        query: str,
        *,
        top_k: int = 4,
        min_score: float = 0.01,
    ) -> list[SearchResult]:
        if self.matrix is None or not self.chunks:
            raise RuntimeError("A base vetorial ainda não foi indexada.")
        if not query.strip():
            return []

        query_vector = self.embedder.transform([query])
        products = self.matrix @ query_vector.T
        if issparse(products):
            scores = products.toarray().ravel()
        else:
            scores = np.asarray(products).ravel()

        ranked_indices = np.argsort(scores)[::-1]
        results: list[SearchResult] = []
        for index in ranked_indices:
            score = float(scores[index])
            if score < min_score:
                continue
            results.append(SearchResult(chunk=self.chunks[int(index)], score=score))
            if len(results) >= max(1, top_k):
                break
        return results

    @property
    def document_names(self) -> list[str]:
        return sorted({chunk.source for chunk in self.chunks})
