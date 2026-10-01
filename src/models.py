"""Modelos de domínio usados pelo pipeline RAG."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """Trecho de um documento, com metadados rastreáveis."""

    id: str
    text: str
    source: str
    page: int | None
    chunk_index: int

    @property
    def citation(self) -> str:
        page_label = f", p. {self.page}" if self.page else ""
        return f"{self.source}{page_label}"


@dataclass(frozen=True, slots=True)
class SearchResult:
    """Trecho recuperado e sua similaridade com a pergunta."""

    chunk: DocumentChunk
    score: float


@dataclass(slots=True)
class Answer:
    """Resposta final com fontes e informações sobre o modo utilizado."""

    text: str
    sources: list[SearchResult] = field(default_factory=list)
    mode: str = "extrativo"
    notice: str | None = None
