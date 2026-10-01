from io import BytesIO
from pathlib import Path

import pytest

from src.document_processor import chunk_text, clean_text, process_file, process_paths


def test_clean_text_joins_hyphenated_line_and_normalizes_paragraphs():
    raw = "Inteli-\ngência   artificial.\n\n  Segundo   parágrafo. "
    assert clean_text(raw) == "Inteligência artificial.\n\nSegundo parágrafo."


def test_chunk_text_creates_unique_overlapping_chunks():
    text = " ".join(f"palavra{i}" for i in range(90))
    chunks = chunk_text(text, "teste.txt", None, chunk_words=40, overlap_words=10)

    assert len(chunks) == 3
    assert len({chunk.id for chunk in chunks}) == 3
    assert chunks[0].text.split()[-10:] == chunks[1].text.split()[:10]
    assert all(chunk.source == "teste.txt" for chunk in chunks)


def test_empty_text_produces_no_chunks():
    assert chunk_text("  \n\n ", "vazio.txt", None) == []


def test_invalid_overlap_is_rejected():
    with pytest.raises(ValueError):
        chunk_text("texto suficiente", "teste.txt", None, chunk_words=20, overlap_words=20)


def test_process_txt_bytes():
    chunks = process_file(BytesIO(b"Pesquisa com rastreabilidade e fontes."), "base.txt")
    assert len(chunks) == 1
    assert "rastreabilidade" in chunks[0].text


def test_unsupported_extension_is_rejected():
    with pytest.raises(ValueError, match="Formato não suportado"):
        process_file("conteúdo".encode(), "arquivo.csv")


def test_sample_pdfs_are_extractable_with_page_metadata():
    paths = sorted(Path("inputs").glob("*.pdf"))
    chunks = process_paths(paths)

    assert len(paths) == 3
    assert len(chunks) >= 8
    assert all(chunk.page is not None and chunk.page >= 2 for chunk in chunks)
    assert {chunk.source for chunk in chunks} == {path.name for path in paths}
