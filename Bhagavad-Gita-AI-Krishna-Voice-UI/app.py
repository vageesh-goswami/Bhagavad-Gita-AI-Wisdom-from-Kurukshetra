"""Streamlit entry point for the Bhagavad Gita AI voice experience."""

from __future__ import annotations

import html
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

import streamlit as st
from dotenv import load_dotenv

from core.config import (
    DEFAULT_GROQ_MODEL,
    DEFAULT_OLLAMA_CHAT_MODEL,
    DEFAULT_RETRIEVAL_CONFIG,
    GROQ_MODELS,
)
from core.prompts import ConversationTurn
from core.rag_service import AnswerResult, answer_question, build_knowledge_base
from core.styles import APP_CSS
from core.voice_experience import narration_for_answer, render_krishna_voice_stage

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
KRISHNA_IMAGE = PROJECT_ROOT / "assets" / "krishna_divine.webp"
KRISHNA_ICON = PROJECT_ROOT / "assets" / "krishna_icon.webp"

st.set_page_config(
    page_title="Bhagavad Gita AI · Shri Krishna Vāṇī",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "A source-grounded Bhagavad Gita RAG assistant with an interactive "
            "Hindi Shri Krishna Vāṇī experience. Narration uses the browser's voice."
        )
    },
)
st.markdown(APP_CSS, unsafe_allow_html=True)

SUGGESTED_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("🏹 कर्तव्य और साहस", "जब मुझे डर लगे तब मैं अपना कर्तव्य कैसे निभाऊँ?"),
    ("🪷 मन की शांति", "चिंतित मन को शांत करने के बारे में गीता क्या सिखाती है?"),
    ("⚔️ कर्म पर ध्यान", "फल की चिंता छोड़कर कर्म पर ध्यान कैसे दूँ?"),
    ("✨ जीवन का उद्देश्य", "मैं अपने जीवन का उद्देश्य और सही दिशा कैसे समझूँ?"),
)


@st.cache_resource(show_spinner="Preparing the sacred knowledge index…")
def get_knowledge_base(embedding_mode: str):
    """Build each embedding index once per Streamlit server process."""

    return build_knowledge_base(embedding_mode)  # type: ignore[arg-type]


def read_secret(name: str) -> str:
    """Read an environment variable first, then optional Streamlit secrets."""

    environment_value = os.getenv(name, "").strip()
    if environment_value:
        return environment_value
    try:
        value = st.secrets.get(name, "")
    except Exception:  # No secrets file or inaccessible secret store.
        return ""
    return str(value).strip() if value else ""


def conversation_pairs(messages: list[dict[str, Any]]) -> list[ConversationTurn]:
    """Convert displayed chat messages into complete user/assistant pairs."""

    turns: list[ConversationTurn] = []
    pending_user: str | None = None
    for message in messages:
        if message.get("role") == "user":
            pending_user = str(message.get("content", ""))
        elif message.get("role") == "assistant" and pending_user is not None:
            turns.append((pending_user, str(message.get("content", ""))))
            pending_user = None
    return turns


def latest_narratable_answer(messages: list[dict[str, Any]]) -> str | None:
    """Return the latest successful assistant answer for Hindi narration."""

    for message in reversed(messages):
        if message.get("role") == "assistant" and message.get("narratable"):
            answer = str(message.get("content", "")).strip()
            if answer:
                return answer
    return None


def _score_percentage(score: float) -> int:
    """Convert a cosine-similarity score into a safe visual percentage."""

    return max(0, min(100, round(score * 100)))


def render_source_cards(sources: Sequence[Any]) -> None:
    """Render retrieval evidence from dataclass or serialised source objects."""

    with st.expander("📜 संदर्भित श्लोक · Retrieved passages"):
        st.caption(
            "The semantic retriever selected these passages before the language "
            "model generated the response."
        )
        for source in sources:
            if isinstance(source, Mapping):
                reference = str(source.get("reference", "Curated Gita passage"))
                text = str(source.get("text", ""))
                score = float(source.get("score", 0.0))
            else:
                reference = str(source.reference)
                text = str(source.text)
                score = float(source.score)

            safe_reference = html.escape(reference)
            safe_text = html.escape(text).replace("\n", "<br>")
            score_percent = _score_percentage(score)
            st.markdown(
                f"""
                <article class="source-card">
                    <div class="source-card-header">
                        <span class="source-reference">{safe_reference}</span>
                        <span class="source-score">MATCH {score:.3f}</span>
                    </div>
                    <div class="score-track" aria-hidden="true">
                        <div class="score-fill" style="width:{score_percent}%"></div>
                    </div>
                    <div class="source-text">{safe_text}</div>
                </article>
                """,
                unsafe_allow_html=True,
            )


def render_hero() -> None:
    """Render the cinematic temple-inspired introduction."""

    st.markdown(
        """
        <header class="temple-hero">
            <div class="hero-stars" aria-hidden="true"></div>
            <div class="hero-arch" aria-hidden="true"></div>
            <div class="hero-topline">
                <span class="living-dot"></span>
                <span>Source-grounded Bhagavad Gita intelligence</span>
                <span class="topline-divider">✦</span>
                <span>हिन्दी वाणी अनुभव</span>
            </div>
            <div class="hero-center">
                <div class="om-mandala"><span>ॐ</span></div>
                <div class="hero-kicker">॥ श्रीमद्भगवद्गीता ॥</div>
                <h1>Wisdom of <span>Shri Krishna</span></h1>
                <p>
                    Ask about duty, fear, action, discipline, devotion, or inner peace.
                    The assistant retrieves relevant Gita passages, explains them in
                    Sanskrit, Hindi, and English—and can now narrate the Hindi teaching.
                </p>
                <div class="hero-actions">
                    <span>📜 Retrieved evidence</span>
                    <span>🧠 Bounded memory</span>
                    <span>🎧 Tap-to-listen Hindi</span>
                </div>
            </div>
            <div class="hero-mantra">
                <span>यदा यदा हि धर्मस्य ग्लानिर्भवति भारत।</span>
                <small>Bhagavad Gita · 4.7</small>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_voice_intro(has_answer: bool) -> None:
    title = "नवीनतम उत्तर को श्रीकृष्ण वाणी में सुनें" if has_answer else "श्रीकृष्ण वाणी का अनुभव करें"
    description = (
        "नीचे चित्र पर स्पर्श करें। दिव्य स्वरूप खुलते ही नवीनतम हिन्दी व्याख्या सुनाई देगी।"
        if has_answer
        else "चित्र पर स्पर्श करें। श्रीकृष्ण का दिव्य स्वरूप खुलेगा और हिन्दी में स्वागत-संदेश सुनाई देगा।"
    )
    st.markdown(
        f"""
        <div class="voice-section-heading">
            <span class="voice-section-icon">🎧</span>
            <div>
                <div class="section-eyebrow">Interactive divine narration</div>
                <h2>{html.escape(title)}</h2>
                <p>{html.escape(description)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats(*, generation_mode: str, model_name: str, memory_window: int, top_k: int) -> None:
    mode_text = "Groq Cloud" if generation_mode == "groq" else "Local Ollama"
    short_model = model_name.split("/")[-1] if model_name else "Default"
    st.markdown(
        f"""
        <section class="sacred-stats" aria-label="Current configuration">
            <div class="sacred-stat"><span class="stat-icon">🔍</span><span class="stat-label">Retrieval</span><span class="stat-value">FAISS · Top {top_k}</span></div>
            <div class="sacred-stat"><span class="stat-icon">🎧</span><span class="stat-label">Hindi voice</span><span class="stat-value">Browser · hi-IN</span></div>
            <div class="sacred-stat"><span class="stat-icon">🧠</span><span class="stat-label">Memory</span><span class="stat-value">Last {memory_window} turns</span></div>
            <div class="sacred-stat"><span class="stat-icon">🪔</span><span class="stat-label">Inference</span><span class="stat-value">{html.escape(mode_text)}</span></div>
            <div class="sacred-stat"><span class="stat-icon">✨</span><span class="stat-label">Model</span><span class="stat-value" title="{html.escape(model_name)}">{html.escape(short_model)}</span></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> tuple[str, str, str, str | None, int, int, bool, bool]:
    """Render controls and return the selected runtime configuration."""

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-mini-seal">ॐ</div>
                <strong>Sādhana Controls</strong>
                <span>Configure your wisdom session</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mode_label = st.radio(
            "Inference mode",
            options=("☁️ Cloud · Groq", "🪔 Local · Ollama"),
            help=(
                "Cloud mode uses local sentence embeddings plus Groq generation. "
                "Local mode uses Ollama for both embeddings and generation."
            ),
        )

        st.markdown('<div class="section-eyebrow">Context & retrieval</div>', unsafe_allow_html=True)
        memory_window = st.slider(
            "Conversation memory",
            min_value=1,
            max_value=10,
            value=5,
            help="Only this many completed question-answer pairs are added to the prompt.",
        )
        top_k = st.slider(
            "Retrieved passages",
            min_value=1,
            max_value=6,
            value=DEFAULT_RETRIEVAL_CONFIG.top_k,
            help="How many semantically relevant Gita passages are supplied as evidence.",
        )
        show_sources = st.toggle("Show retrieved evidence", value=True)
        enable_voice = st.toggle("Enable Shri Krishna Hindi voice", value=True)

        st.markdown('<div class="section-eyebrow">Model provider</div>', unsafe_allow_html=True)
        if mode_label == "☁️ Cloud · Groq":
            generation_mode = "groq"
            embedding_mode = "sentence-transformer"
            model_name = st.selectbox(
                "Groq model",
                options=GROQ_MODELS,
                index=GROQ_MODELS.index(DEFAULT_GROQ_MODEL),
            )
            stored_key = read_secret("GROQ_API_KEY")
            if stored_key:
                groq_api_key = stored_key
                st.success("API key loaded securely")
            else:
                groq_api_key = st.text_input(
                    "Groq API key",
                    type="password",
                    placeholder="gsk_…",
                    help="For local development, place GROQ_API_KEY in a .env file.",
                ).strip()
        else:
            generation_mode = "ollama"
            embedding_mode = "ollama"
            model_name = st.text_input(
                "Ollama chat model",
                value=DEFAULT_OLLAMA_CHAT_MODEL,
            ).strip()
            groq_api_key = None
            st.caption("Required local models: `mistral` and `nomic-embed-text`.")

        st.divider()
        if st.button("🧹 Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("pending_question", None)
            st.rerun()

        st.markdown(
            """
            <div class="voice-side-note">
                <strong>🎧 Shri Krishna Vāṇī</strong>
                <span>Tap the Krishna portrait after an answer to hear only its Hindi explanation. Speech is generated by your browser's installed voice.</span>
            </div>
            <div class="privacy-note">
                🔒 Your API key is read from the local environment or the masked field.
                It is never printed in the conversation.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return (
        generation_mode,
        embedding_mode,
        model_name,
        groq_api_key,
        memory_window,
        top_k,
        show_sources,
        enable_voice,
    )


def render_welcome_prompts() -> None:
    st.markdown(
        """
        <section class="welcome-sanctum">
            <span class="welcome-symbol">🪷</span>
            <div>
                <div class="section-eyebrow">Begin the dialogue</div>
                <h3>आज आप किस विषय पर मार्गदर्शन चाहते हैं?</h3>
                <p>
                    Ask in Hindi or English. Every answer is built from retrieved passages,
                    followed by a practical application—and its Hindi section can be spoken aloud.
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(2)
    for index, (label, prompt) in enumerate(SUGGESTED_QUESTIONS):
        with columns[index % 2]:
            if st.button(label, key=f"suggested_prompt_{index}", use_container_width=True):
                st.session_state.pending_question = prompt
                st.rerun()


def render_architecture() -> None:
    with st.expander("⚙️ यह RAG + Voice अनुभव कैसे काम करता है?"):
        st.markdown(
            """
            **1 · Retrieve** — The question is embedded and matched against curated Gita passages in FAISS.  
            **2 · Ground** — Retrieved evidence and bounded conversation history are inserted into the prompt.  
            **3 · Explain** — Groq or Ollama produces Sanskrit, Hindi, English, and practical sections.  
            **4 · Extract Hindi** — The application safely extracts only the Hindi explanation.  
            **5 · Speak on tap** — The browser's Hindi speech engine narrates it after an explicit click.
            """
        )


def serialise_sources(result: AnswerResult) -> list[dict[str, Any]]:
    return [
        {
            "reference": passage.reference,
            "text": passage.text,
            "score": passage.score,
        }
        for passage in result.sources
    ]


if "messages" not in st.session_state:
    st.session_state.messages = []

(
    generation_mode,
    embedding_mode,
    model_name,
    groq_api_key,
    memory_window,
    top_k,
    show_sources,
    enable_voice,
) = render_sidebar()

render_hero()
render_stats(
    generation_mode=generation_mode,
    model_name=model_name,
    memory_window=memory_window,
    top_k=top_k,
)
render_architecture()

latest_answer = latest_narratable_answer(st.session_state.messages)

if not st.session_state.messages:
    if enable_voice:
        render_voice_intro(has_answer=False)
        render_krishna_voice_stage(
            speech_text=narration_for_answer(None),
            image_path=KRISHNA_IMAGE,
            icon_path=KRISHNA_ICON,
            context_label="स्वागत संदेश · Welcome",
        )
    render_welcome_prompts()

for message in st.session_state.messages:
    role = str(message.get("role", "assistant"))
    avatar = "🧑‍💻" if role == "user" else "🪷"
    with st.chat_message(role, avatar=avatar):
        st.markdown(str(message.get("content", "")))
        sources = message.get("sources")
        if role == "assistant" and sources and show_sources:
            render_source_cards(sources)

if latest_answer and enable_voice:
    render_voice_intro(has_answer=True)
    render_krishna_voice_stage(
        speech_text=narration_for_answer(latest_answer),
        image_path=KRISHNA_IMAGE,
        icon_path=KRISHNA_ICON,
        context_label="नवीनतम उत्तर · Latest answer",
    )

chat_question = st.chat_input(
    "अपना प्रश्न लिखें · Ask about duty, fear, action, discipline, or inner peace…"
)
pending_question = st.session_state.pop("pending_question", None)
question = chat_question or pending_question

if question:
    clean_question = str(question).strip()
    if generation_mode == "groq" and not groq_api_key:
        st.error("Add a valid Groq API key in the sidebar or in your .env file.")
        st.stop()

    history = conversation_pairs(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": clean_question})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(clean_question)

    with st.chat_message("assistant", avatar="🪷"):
        try:
            with st.status("🪷 गीता के प्रासंगिक श्लोक खोजे जा रहे हैं…", expanded=True) as status:
                st.write("Preparing the semantic knowledge index")
                knowledge_base = get_knowledge_base(embedding_mode)
                st.write(f"Searching across {knowledge_base.chunk_count} curated passage chunks")
                st.write("Grounding the answer in the most relevant evidence")
                result = answer_question(
                    question=clean_question,
                    history=history,
                    memory_window=memory_window,
                    knowledge_base=knowledge_base,
                    generation_mode=generation_mode,  # type: ignore[arg-type]
                    model_name=model_name,
                    api_key=groq_api_key,
                    top_k=top_k,
                )
                status.update(label="✨ Grounded wisdom retrieved", state="complete", expanded=False)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result.answer,
                    "sources": serialise_sources(result),
                    "narratable": True,
                }
            )
            st.rerun()
        except Exception as exc:  # UI boundary: useful message plus optional diagnostics.
            technical_message = str(exc)
            if "model_not_found" in technical_message or "does not exist" in technical_message:
                error_message = (
                    "The selected Groq model is not available to this API key. "
                    "Choose an accessible model in Sādhana Controls and try again."
                )
            else:
                error_message = (
                    "The request could not be completed. Check the selected model, API key, "
                    "internet connection, and local Ollama service."
                )
            st.error(error_message)
            with st.expander("Technical details"):
                st.code(f"{type(exc).__name__}: {exc}")
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message, "narratable": False}
            )

st.markdown(
    """
    <footer class="app-footer">
        <span class="lotus-divider">✦ 🪷 ✦</span>
        <span class="footer-mantra">हरे कृष्ण हरे कृष्ण · कृष्ण कृष्ण हरे हरे · हरे राम हरे राम · राम राम हरे हरे</span>
        <small>AI-generated educational interpretation grounded in curated passages. Verify important translations with a trusted edition.</small>
    </footer>
    """,
    unsafe_allow_html=True,
)
