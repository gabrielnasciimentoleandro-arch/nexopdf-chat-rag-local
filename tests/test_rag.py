from src.embeddings import TfidfEmbedder
from src.models import DocumentChunk
from src.rag import RAGPipeline
from src.vector_store import InMemoryVectorStore


def pipeline() -> RAGPipeline:
    chunks = [
        DocumentChunk(
            "c1",
            "A revisão humana é indispensável para verificar afirmações e referências produzidas por inteligência artificial. O estudante permanece responsável pelo texto final.",
            "guia.pdf",
            2,
            0,
        ),
        DocumentChunk(
            "c2",
            "A rastreabilidade registra perguntas, fontes consultadas, decisões tomadas e motivos de exclusão.",
            "metodo.pdf",
            3,
            0,
        ),
    ]
    store = InMemoryVectorStore(TfidfEmbedder())
    store.index(chunks)
    return RAGPipeline(store)


def test_extractive_answer_is_grounded_and_cited():
    answer = pipeline().ask("Por que a revisão humana é importante?", use_ollama=False)

    assert answer.mode == "Extrativo local"
    assert "revisão humana" in answer.text.lower()
    assert "[Fonte 1]" in answer.text
    assert answer.sources[0].chunk.source == "guia.pdf"


def test_short_question_returns_validation_message():
    answer = pipeline().ask("oi", use_ollama=False)
    assert answer.mode == "validação"
    assert not answer.sources


def test_prompt_contains_page_citations():
    rag = pipeline()
    results = rag.store.search("rastreabilidade", top_k=1)
    prompt = rag._build_prompt("O que registrar?", results)
    assert "metodo.pdf, p. 3" in prompt
    assert "PERGUNTA" in prompt


def test_pipeline_uses_local_generator_when_enabled():
    class FakeOllama:
        model = "modelo-teste"

        def generate(self, system_prompt: str, user_prompt: str) -> str:
            assert "SOMENTE o contexto" in system_prompt
            assert "guia.pdf, p. 2" in user_prompt
            return "A revisão humana verifica as afirmações. [Fonte 1]"

    rag = pipeline()
    rag.ollama = FakeOllama()
    answer = rag.ask("Por que a revisão humana é importante?", use_ollama=True)

    assert answer.mode == "Ollama · modelo-teste"
    assert "[Fonte 1]" in answer.text
    assert answer.sources
