"""Interface Streamlit do NexoPDF."""

from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from src.document_processor import SUPPORTED_EXTENSIONS, process_file, process_paths
from src.embeddings import build_embedder
from src.ollama_client import OllamaClient
from src.rag import RAGPipeline
from src.vector_store import InMemoryVectorStore

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
DEFAULT_MODEL = "qwen2.5:3b"

st.set_page_config(
    page_title="NexoPDF · Chat com seus documentos",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root {
  --ink: #15213b;
  --muted: #63708a;
  --purple: #6257e8;
  --purple-dark: #4b42cb;
  --lavender: #efedff;
  --paper: #f7f8fc;
  --line: #e6e8f0;
  --green: #24a474;
}
[data-testid="stAppViewContainer"] { background: var(--paper); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
  background: #111a31;
  border-right: 0;
}
[data-testid="stSidebar"] * { color: #f6f7ff; }
[data-testid="stSidebar"] small, [data-testid="stSidebar"] .stCaption { color: #aeb7cc !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
  background: #1a2541;
  border: 1px dashed #4d5a78;
}
[data-testid="stSidebar"] button[kind="secondary"] {
  border-color: #465473;
  background: #1a2541;
}
[data-testid="stSidebar"] button[kind="primary"] {
  background: var(--purple);
  border-color: var(--purple);
}
[data-testid="stMainBlockContainer"] { max-width: 1080px; padding-top: 2.2rem; }
.nexo-brand { display: flex; align-items: center; gap: 12px; margin: 2px 0 5px; }
.nexo-mark {
  width: 38px; height: 38px; display: grid; place-items: center; border-radius: 12px;
  color: white; background: linear-gradient(145deg, #8d83ff, #574be1);
  box-shadow: 0 10px 25px rgba(98,87,232,.3); font-size: 21px;
}
.nexo-name { font-size: 21px; font-weight: 750; letter-spacing: -.035em; }
.nexo-tagline { margin: 0 0 24px 50px; color: #aeb7cc; font-size: 11px; }
.hero-eyebrow {
  color: var(--purple); font-size: 11px; font-weight: 750; letter-spacing: .16em;
  text-transform: uppercase; margin-bottom: 12px;
}
.hero-title { color: var(--ink); font-size: clamp(39px, 5vw, 62px); font-weight: 720; line-height: .98; letter-spacing: -.055em; margin: 0; }
.hero-title span { color: var(--purple); }
.hero-copy { max-width: 650px; color: var(--muted); font-size: 17px; line-height: 1.6; margin: 20px 0 25px; }
.privacy-pill {
  display: inline-flex; align-items: center; gap: 7px; padding: 8px 12px;
  border: 1px solid #dfe2ec; border-radius: 999px; color: #526079; background: white;
  font-size: 11px; font-weight: 650;
}
.privacy-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 4px #e4f6ef; }
.metric-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 31px 0 28px; }
.metric-card { padding: 17px 19px; border: 1px solid var(--line); border-radius: 17px; background: rgba(255,255,255,.86); box-shadow: 0 7px 24px rgba(29,39,74,.04); }
.metric-value { color: var(--ink); font-size: 23px; font-weight: 750; letter-spacing: -.03em; }
.metric-label { color: var(--muted); font-size: 10px; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; margin-top: 2px; }
.section-label { color: var(--ink); font-size: 14px; font-weight: 730; margin: 12px 0 10px; }
.stButton > button { border-radius: 12px; font-weight: 650; }
[data-testid="stChatMessage"] {
  background: white; border: 1px solid var(--line); border-radius: 18px; padding: 8px 6px;
  box-shadow: 0 5px 20px rgba(29,39,74,.035);
}
[data-testid="stChatInput"] { border-radius: 16px; background: white; }
.source-box { padding: 12px 14px; margin: 7px 0; border-left: 3px solid var(--purple); border-radius: 7px 12px 12px 7px; color: #44516c; background: #f5f4ff; font-size: 12px; line-height: 1.5; }
.source-meta { display: block; color: var(--purple-dark); font-size: 10px; font-weight: 750; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 4px; }
.mode-badge { display: inline-block; margin-top: 5px; padding: 4px 8px; color: #4e477f; background: var(--lavender); border-radius: 999px; font-size: 9px; font-weight: 750; text-transform: uppercase; letter-spacing: .06em; }
.sidebar-status { padding: 11px 12px; border: 1px solid #33415f; border-radius: 12px; background: #18233d; font-size: 12px; line-height: 1.45; }
.sidebar-status strong { color: #9f96ff !important; }
hr { border-color: var(--line) !important; }
@media (max-width: 700px) {
  [data-testid="stMainBlockContainer"] { padding-top: 1.35rem; }
  .hero-title { font-size: 42px; }
  .metric-row { grid-template-columns: 1fr; }
  .metric-card { padding: 13px 16px; }
}
</style>
""",
    unsafe_allow_html=True,
)


def build_pipeline(chunks, embedding_mode: str, model: str) -> RAGPipeline:
    embedder = build_embedder(embedding_mode)
    store = InMemoryVectorStore(embedder)
    store.index(chunks)
    return RAGPipeline(store, OllamaClient(model=model))


def demo_paths() -> list[Path]:
    return sorted(INPUTS.glob("*.pdf")) + sorted(INPUTS.glob("*.txt"))


def load_demo(embedding_mode: str, model: str) -> None:
    chunks = process_paths(demo_paths())
    st.session_state.pipeline = build_pipeline(chunks, embedding_mode, model)
    st.session_state.messages = []
    st.session_state.base_label = "Base de demonstração"


def render_sources(answer) -> None:
    if answer.notice:
        st.caption(f"ℹ️ {answer.notice}")
    safe_mode = escape(answer.mode)
    st.markdown(f'<span class="mode-badge">{safe_mode}</span>', unsafe_allow_html=True)
    if not answer.sources:
        return
    with st.expander(f"Ver {len(answer.sources)} trechos consultados"):
        for result in answer.sources:
            excerpt = result.chunk.text
            if len(excerpt) > 360:
                excerpt = excerpt[:357].rsplit(" ", 1)[0] + "…"
            safe_citation = escape(result.chunk.citation)
            safe_excerpt = escape(excerpt)
            st.markdown(
                f'<div class="source-box"><span class="source-meta">{safe_citation} · similaridade {result.score:.0%}</span>{safe_excerpt}</div>',
                unsafe_allow_html=True,
            )


def ask_and_store(question: str, use_ollama: bool, top_k: int) -> None:
    question = question.strip()
    if not question:
        return
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(question)
    with st.chat_message("assistant", avatar="🔎"):
        with st.spinner("Buscando evidências nos documentos…"):
            answer = st.session_state.pipeline.ask(
                question,
                top_k=top_k,
                use_ollama=use_ollama,
            )
        st.markdown(answer.text)
        render_sources(answer)
    st.session_state.messages.append(
        {"role": "assistant", "content": answer.text, "answer": answer}
    )
    st.rerun()


if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "base_label" not in st.session_state:
    st.session_state.base_label = ""

with st.sidebar:
    st.markdown(
        '<div class="nexo-brand"><div class="nexo-mark">◈</div><div class="nexo-name">NexoPDF</div></div><p class="nexo-tagline">conhecimento conectado</p>',
        unsafe_allow_html=True,
    )
    st.markdown("#### Sua base de conhecimento")
    uploaded_files = st.file_uploader(
        "Envie PDFs ou textos",
        type=[extension.lstrip(".") for extension in sorted(SUPPORTED_EXTENSIONS)],
        accept_multiple_files=True,
        help="Limite recomendado: 15 MB por arquivo. PDFs devem conter texto selecionável.",
    )

    with st.expander("Configurações", expanded=False):
        embedding_label = st.selectbox(
            "Tipo de busca",
            ["Leve · TF-IDF", "Semântica · MiniLM"],
            help="MiniLM requer a instalação opcional descrita no README.",
        )
        embedding_mode = "semantic" if embedding_label.startswith("Semântica") else "tfidf"
        model = st.text_input("Modelo Ollama", value=DEFAULT_MODEL)
        top_k = st.slider("Trechos por pergunta", 2, 7, 5)

    if st.button("Indexar meus arquivos", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Selecione pelo menos um arquivo.")
        else:
            try:
                with st.spinner("Lendo e indexando…"):
                    chunks = []
                    for uploaded in uploaded_files:
                        if uploaded.size > 15 * 1024 * 1024:
                            raise ValueError(f"{uploaded.name} ultrapassa o limite de 15 MB.")
                        chunks.extend(process_file(uploaded.getvalue(), uploaded.name))
                    st.session_state.pipeline = build_pipeline(chunks, embedding_mode, model)
                    st.session_state.messages = []
                    st.session_state.base_label = "Meus documentos"
                st.success("Base atualizada.")
            except Exception as exc:
                st.error(f"Não foi possível indexar: {exc}")

    if st.button("Usar base de demonstração", use_container_width=True):
        try:
            with st.spinner("Carregando exemplos…"):
                load_demo(embedding_mode, model)
            st.success("Demonstração carregada.")
        except Exception as exc:
            st.error(f"Falha ao carregar a demonstração: {exc}")

    st.divider()
    ollama_client = OllamaClient(model=model)
    ollama_ready = ollama_client.is_ready()
    if ollama_ready:
        st.markdown('<div class="sidebar-status"><strong>● Ollama conectado</strong><br>Respostas generativas locais ativadas.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-status"><strong>○ Modo extrativo</strong><br>Ollama ou modelo não detectado. A busca vetorial continua funcional.</div>', unsafe_allow_html=True)
    use_ollama = st.toggle("Usar geração local", value=ollama_ready, disabled=not ollama_ready)
    st.caption("Seus arquivos permanecem nesta sessão e não são enviados para APIs externas.")

if st.session_state.pipeline is None:
    try:
        load_demo("tfidf", DEFAULT_MODEL)
    except Exception as exc:
        st.error(f"A base inicial não pôde ser carregada: {exc}")

pipeline = st.session_state.pipeline

st.markdown('<div class="hero-eyebrow">RAG local · privado · rastreável</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Converse com seus <span>documentos.</span></h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-copy">Faça perguntas, recupere os trechos mais relevantes e confira a origem de cada resposta — sem depender de uma API paga.</p>',
    unsafe_allow_html=True,
)
st.markdown('<span class="privacy-pill"><span class="privacy-dot"></span> Processamento local</span>', unsafe_allow_html=True)

if pipeline is not None:
    documents = len(pipeline.store.document_names)
    chunks_count = len(pipeline.store.chunks)
    st.markdown(
        f"""<div class="metric-row">
        <div class="metric-card"><div class="metric-value">{documents}</div><div class="metric-label">Documentos</div></div>
        <div class="metric-card"><div class="metric-value">{chunks_count}</div><div class="metric-label">Trechos indexados</div></div>
        <div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Processamento local</div></div>
        </div>""",
        unsafe_allow_html=True,
    )

    with st.expander(f"Base ativa · {st.session_state.base_label}"):
        for document in pipeline.store.document_names:
            st.markdown(f"- `{document}`")

    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🔎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "answer" in message:
                render_sources(message["answer"])

    suggested_question = None
    if not st.session_state.messages:
        st.markdown('<div class="section-label">Experimente uma pergunta</div>', unsafe_allow_html=True)
        suggestions = [
            "Quais cuidados devo tomar ao usar IA no TCC?",
            "Como garantir rastreabilidade na pesquisa?",
            "Qual é o papel da revisão humana?",
        ]
        columns = st.columns(3)
        for column, suggestion in zip(columns, suggestions, strict=True):
            with column:
                if st.button(suggestion, use_container_width=True):
                    suggested_question = suggestion

    typed_question = st.chat_input("Pergunte algo sobre os documentos…")
    question = typed_question or suggested_question
    if question:
        ask_and_store(question, use_ollama=use_ollama, top_k=top_k)
else:
    st.info("Envie documentos pela barra lateral para começar.")
