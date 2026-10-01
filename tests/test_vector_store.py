from src.embeddings import TfidfEmbedder
from src.models import DocumentChunk
from src.vector_store import InMemoryVectorStore


def make_chunk(identifier: str, text: str) -> DocumentChunk:
    return DocumentChunk(identifier, text, f"{identifier}.pdf", 1, 0)


def test_search_ranks_relevant_chunk_first():
    store = InMemoryVectorStore(TfidfEmbedder())
    store.index(
        [
            make_chunk("privacidade", "Dados pessoais exigem anonimização e processamento local seguro."),
            make_chunk("metodologia", "A revisão de literatura utiliza critérios de inclusão e exclusão."),
            make_chunk("qualidade", "A revisão humana verifica respostas e referências acadêmicas."),
        ]
    )

    results = store.search("Como proteger dados pessoais?", top_k=2)

    assert results
    assert results[0].chunk.source == "privacidade.pdf"
    assert results[0].score > 0


def test_document_names_are_unique_and_sorted():
    store = InMemoryVectorStore(TfidfEmbedder())
    store.index(
        [
            make_chunk("b", "texto sobre pesquisa e método"),
            make_chunk("a", "texto sobre dados e privacidade"),
            DocumentChunk("a2", "outro trecho relevante", "a.pdf", 2, 1),
        ]
    )
    assert store.document_names == ["a.pdf", "b.pdf"]
