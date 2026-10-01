"""Extração, limpeza e fragmentação de documentos."""

from __future__ import annotations

import hashlib
import io
import re
from collections.abc import Iterable
from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader

from .models import DocumentChunk

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def clean_text(text: str) -> str:
    """Normaliza texto extraído sem apagar limites de parágrafo."""
    text = text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        normalized = re.sub(r"\s+", " ", paragraph).strip()
        if normalized:
            paragraphs.append(normalized)
    return "\n\n".join(paragraphs)


def chunk_text(
    text: str,
    source: str,
    page: int | None,
    *,
    chunk_words: int = 170,
    overlap_words: int = 35,
) -> list[DocumentChunk]:
    """Divide um texto em janelas de palavras com sobreposição controlada."""
    if chunk_words < 20:
        raise ValueError("chunk_words deve ser pelo menos 20")
    if overlap_words < 0 or overlap_words >= chunk_words:
        raise ValueError("overlap_words deve estar entre 0 e chunk_words - 1")

    words = clean_text(text).split()
    if not words:
        return []

    chunks: list[DocumentChunk] = []
    start = 0
    index = 0
    while start < len(words):
        end = min(start + chunk_words, len(words))
        content = " ".join(words[start:end]).strip()
        digest = hashlib.sha256(
            f"{source}|{page}|{index}|{content}".encode()
        ).hexdigest()[:16]
        chunks.append(
            DocumentChunk(
                id=digest,
                text=content,
                source=source,
                page=page,
                chunk_index=index,
            )
        )
        if end >= len(words):
            break
        start = end - overlap_words
        index += 1
    return chunks


def extract_pdf(
    stream: BinaryIO | bytes,
    source: str,
    *,
    chunk_words: int = 170,
    overlap_words: int = 35,
) -> list[DocumentChunk]:
    """Extrai texto por página de um PDF e retorna trechos citáveis."""
    data = io.BytesIO(stream) if isinstance(stream, bytes) else stream
    reader = PdfReader(data)
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:  # pragma: no cover - depende do PDF
            raise ValueError(f"O arquivo {source} está protegido por senha.") from exc

    chunks: list[DocumentChunk] = []
    total_pages = len(reader.pages)
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        # Folhas de rosto muito curtas normalmente contêm apenas título e créditos,
        # não evidências úteis para responder perguntas.
        if total_pages > 1 and page_number == 1 and len(clean_text(text).split()) < 60:
            continue
        chunks.extend(
            chunk_text(
                text,
                source,
                page_number,
                chunk_words=chunk_words,
                overlap_words=overlap_words,
            )
        )
    return chunks


def extract_plain_text(
    stream: BinaryIO | bytes | str,
    source: str,
    *,
    chunk_words: int = 170,
    overlap_words: int = 35,
) -> list[DocumentChunk]:
    """Lê TXT/Markdown em UTF-8 e cria trechos."""
    if isinstance(stream, str):
        text = stream
    elif isinstance(stream, bytes):
        text = stream.decode("utf-8", errors="replace")
    else:
        raw = stream.read()
        text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
    return chunk_text(
        text,
        source,
        None,
        chunk_words=chunk_words,
        overlap_words=overlap_words,
    )


def process_file(
    content: BinaryIO | bytes,
    filename: str,
    *,
    chunk_words: int = 170,
    overlap_words: int = 35,
) -> list[DocumentChunk]:
    """Processa um arquivo aceito de acordo com sua extensão."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Formato não suportado: {suffix or 'sem extensão'}")
    if suffix == ".pdf":
        return extract_pdf(
            content,
            filename,
            chunk_words=chunk_words,
            overlap_words=overlap_words,
        )
    return extract_plain_text(
        content,
        filename,
        chunk_words=chunk_words,
        overlap_words=overlap_words,
    )


def process_paths(paths: Iterable[Path], **chunk_options: int) -> list[DocumentChunk]:
    """Processa uma coleção de caminhos locais."""
    chunks: list[DocumentChunk] = []
    for path in paths:
        with path.open("rb") as file:
            chunks.extend(process_file(file, path.name, **chunk_options))
    return chunks
