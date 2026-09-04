"""Cinematic Streamlit dashboard for the Bhagavad Gita AI assistant."""

from __future__ import annotations

import base64
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
from core.voice_experience import narration_for_answer, render_krishna_voice_console

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
KRISHNA_HERO = PROJECT_ROOT / "assets" / "krishna_dashboard.webp"
KRISHNA_VOICE = PROJECT_ROOT / "assets" / "krishna_symbols.webp"
KRISHNA_ICON = PROJECT_ROOT / "assets" / "krishna_icon.webp"

# These model IDs were shut down by Groq in August 2026.  Filtering them here keeps
# the UI safe even when an older config.py is still present in an existing checkout.
_DEPRECATED_GROQ_MODELS = {
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
}
_FALLBACK_GROQ_MODELS = (
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
)

SUGGESTED_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("🏹 कर्म योग क्या है?", "कर्म योग क्या है और इसे रोज़मर्रा के जीवन में कैसे अपनाएँ?"),
    ("🧘 मन को शांत कैसे करें?", "चिंतित और अशांत मन को शांत करने के बारे में गीता क्या सिखाती है?"),
    ("⭐ सफलता का रहस्य?", "फल की चिंता छोड़कर सफलता के लिए सही कर्म कैसे करूँ?"),
    ("🏛️ जीवन का उद्देश्य?", "मैं अपने जीवन का उद्देश्य और सही कर्तव्य कैसे समझूँ?"),
)

st.set_page_config(
    page_title="Bhagavad Gita AI · Shri Krishna Vāṇī",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "A source-grounded Bhagavad Gita RAG assistant with an interactive "
            "Hindi Shri Krishna narration experience."
        )
    },
)
st.markdown(APP_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Preparing the sacred knowledge index…")
def get_knowledge_base(embedding_mode: str):
    """Build each embedding index once per Streamlit server process."""

    return build_knowledge_base(embedding_mode)  # type: ignore[arg-type]


@st.cache_data(show_spinner=False)
def image_data_uri(path_string: str) -> str:
    """Return one local image as a browser-safe data URI."""

    path = Path(path_string)
    if not path.exists():
        raise FileNotFoundError(f"Interface asset not found: {path}")
    mime = {
        ".webp": "image/webp",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(path.suffix.casefold(), "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def read_secret(name: str) -> str:
    """Read an environment variable first, then optional Streamlit secrets."""

    environment_value = os.getenv(name, "").strip()
    if environment_value:
        return environment_value
    try:
        value = st.secrets.get(name, "")
    except Exception:
        return ""
    return str(value).strip() if value else ""


def conversation_pairs(messages: list[dict[str, Any]]) -> list[ConversationTurn]:
    """Convert displayed messages into complete user/assistant pairs."""

    turns: list[ConversationTurn] = []
    pending_user: str | None = None
    for message in messages:
        if message.get("role") == "user":
            pending_user = str(message.get("content", ""))
        elif message.get("role") == "assistant" and pending_user is not None:
            if message.get("narratable", True):
                turns.append((pending_user, str(message.get("content", ""))))
            pending_user = None
    return turns


def latest_answer(messages: list[dict[str, Any]]) -> str | None:
    for message in reversed(messages):
        if message.get("role") == "assistant" and message.get("narratable", True):
            content = str(message.get("content", "")).strip()
            if content:
                return content
    return None


def latest_sources(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for message in reversed(messages):
        if message.get("role") == "assistant" and message.get("sources"):
            return list(message["sources"])
    return []


def score_percentage(score: float) -> int:
    return max(0, min(100, round(score * 100)))


def render_ambient_world() -> None:
    """Add fixed, pointer-safe petals, light orbs, and star motion."""

    st.markdown(
        """
        <div class="ambient-world" aria-hidden="true">
            <span class="ambient-orb orb-one"></span>
            <span class="ambient-orb orb-two"></span>
            <span class="ambient-orb orb-three"></span>
            <i class="falling-petal petal-one">❀</i>
            <i class="falling-petal petal-two">❀</i>
            <i class="falling-petal petal-three">❀</i>
            <i class="falling-petal petal-four">❀</i>
            <i class="falling-petal petal-five">❀</i>
            <i class="falling-petal petal-six">❀</i>
            <b class="firefly fly-one"></b><b class="firefly fly-two"></b>
            <b class="firefly fly-three"></b><b class="firefly fly-four"></b>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_navigation() -> None:
    st.markdown(
        """
        <nav class="temple-nav" aria-label="Primary navigation">
            <a class="active" href="#home">⌂ <span>Home</span></a>
            <a href="#about-gita">▤ <span>About Gita</span></a>
            <a href="#how-it-works">⛓ <span>How it Works</span></a>
            <a href="#wisdom-library">✺ <span>Wisdom Library</span></a>
            <span class="nav-spacer"></span>
            <span class="nav-sun">☀</span>
            <span class="nav-om">ॐ</span>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> tuple[str, str, str, str | None, int, int, bool]:
    """Render sādhana controls and return runtime selections."""

    with st.sidebar:
        st.markdown(
            """
            <section class="sidebar-brand">
                <div class="sidebar-om">ॐ</div>
                <div>
                    <h2>Bhagavad<br>Gita AI</h2>
                    <p>AI Wisdom from Kurukshetra</p>
                </div>
            </section>
            <div class="sidebar-divider"><span>✦</span></div>
            <div class="sidebar-section-title">❀ Sādhana Controls</div>
            """,
            unsafe_allow_html=True,
        )

        mode_label = st.radio(
            "Inference Mode",
            options=("☁️ Cloud (Groq)", "▣ Local (Ollama)"),
            horizontal=True,
            help=(
                "Cloud mode uses local sentence embeddings plus Groq generation. "
                "Local mode uses Ollama for both embeddings and generation."
            ),
        )

        if mode_label == "☁️ Cloud (Groq)":
            generation_mode = "groq"
            embedding_mode = "sentence-transformer"
            configured_models = tuple(
                model for model in GROQ_MODELS if model not in _DEPRECATED_GROQ_MODELS
            )
            model_options = configured_models or _FALLBACK_GROQ_MODELS
            default_model = (
                DEFAULT_GROQ_MODEL
                if DEFAULT_GROQ_MODEL in model_options
                else model_options[0]
            )
            model_name = st.selectbox(
                "Model",
                options=model_options,
                index=model_options.index(default_model),
            )
            stored_key = read_secret("GROQ_API_KEY")
            if stored_key:
                groq_api_key: str | None = stored_key
                key_status = "connected"
            else:
                entered_key = st.text_input(
                    "Groq API key",
                    type="password",
                    placeholder="gsk_…",
                    help="Place GROQ_API_KEY in .env for local development.",
                ).strip()
                groq_api_key = entered_key or None
                key_status = "connected" if entered_key else "missing"
        else:
            generation_mode = "ollama"
            embedding_mode = "ollama"
            model_name = st.text_input(
                "Ollama chat model",
                value=DEFAULT_OLLAMA_CHAT_MODEL,
            ).strip()
            groq_api_key = None
            key_status = "local"

        memory_window = st.slider(
            "Conversation Memory",
            min_value=1,
            max_value=10,
            value=5,
            help="Only this many completed Q&A pairs are included in the next prompt.",
        )
        top_k = st.slider(
            "Retrieved Passages",
            min_value=1,
            max_value=6,
            value=DEFAULT_RETRIEVAL_CONFIG.top_k,
        )
        show_sources = st.toggle("Show Retrieved Passages", value=True)

        if key_status == "connected":
            st.markdown(
                """
                <div class="api-card connected">
                    <span class="api-shield">✓</span>
                    <div><strong>API Key Status</strong><small>Groq key loaded securely.</small><b>✓ Connected</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif key_status == "local":
            st.markdown(
                """
                <div class="api-card local">
                    <span class="api-shield">⌂</span>
                    <div><strong>Local Runtime</strong><small>Ollama must be running.</small><b>Local mode selected</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="api-card missing">
                    <span class="api-shield">!</span>
                    <div><strong>API Key Status</strong><small>Add GROQ_API_KEY in .env.</small><b>Key required</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("♙ Clear Conversation", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            """
            <section class="daily-card">
                <div class="daily-title">✺ प्रेरणा <span>(Daily Inspiration)</span></div>
                <p>कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।<br>मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥</p>
                <small>— Bhagavad Gita 2.47</small>
                <div class="lotus-mark">⌘</div>
            </section>
            <section class="chant-card">
                <div class="chant-title">♫ Gita Chant</div>
                <p>Pause for one breath before asking.</p>
                <div class="chant-row"><span class="chant-play">▶</span><span class="chant-wave">▂▅▃▆▂▇▃▅▂▆▃▇▂</span></div>
                <small>हरे कृष्ण · हरे राम</small>
            </section>
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
    )


def render_hero(*, memory_window: int, top_k: int) -> None:
    """Render the animated Krishna hero used in the requested dashboard."""

    hero_uri = image_data_uri(str(KRISHNA_HERO))
    st.markdown(
        f"""
        <section class="krishna-hero" id="home">
            <div class="hero-nebula"></div>
            <div class="hero-rays"></div>
            <div class="hero-verse">
                <span>यदा यदा हि धर्मस्य</span>
                <span>ग्लानिर्भवति भारत।</span>
                <span>अभ्युत्थानमधर्मस्य</span>
                <span>तदात्मानं सृजाम्यहम्॥</span>
                <small>— Bhagavad Gita 4.7</small>
            </div>
            <div class="chakra-rotor" aria-hidden="true"><span>✺</span></div>
            <div class="krishna-aura aura-a"></div>
            <div class="krishna-aura aura-b"></div>
            <img class="krishna-figure" src="{hero_uri}" alt="शेषनाग, शंख, चक्र, गदा और पद्म सहित श्रीकृष्ण का कलात्मक स्वरूप">
            <span class="hero-petal hp-one">❀</span><span class="hero-petal hp-two">❀</span>
            <span class="hero-petal hp-three">❀</span><span class="hero-petal hp-four">❀</span>
            <div class="hero-counts">
                <div><b>18</b><span>अध्याय</span></div>
                <div><b>700</b><span>श्लोक</span></div>
                <div><b>∞</b><span>ज्ञान</span></div>
            </div>
            <div class="hero-config">
                <span>🔍 Top {top_k} passages</span>
                <span>🧠 {memory_window} turns</span>
            </div>
            <div class="hero-mantra">ॐ &nbsp; Hare Krishna Hare Krishna, Krishna Krishna Hare Hare, Hare Rama Hare Rama &nbsp; ॐ</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_quick_questions() -> str | None:
    st.markdown(
        """
        <section class="section-heading" id="wisdom-library">
            <div><span>पूछें कुछ भी</span><strong>Ask anything from the Gita</strong></div>
            <small>Choose a path or write your own question</small>
        </section>
        """,
        unsafe_allow_html=True,
    )
    selected: str | None = None
    columns = st.columns(4)
    for column, (label, question) in zip(columns, SUGGESTED_QUESTIONS, strict=True):
        with column:
            if st.button(label, use_container_width=True, key=f"quick-{label}"):
                selected = question
    return selected


def render_chat_history(*, show_sources: bool) -> None:
    st.markdown(
        """
        <section class="section-heading chat-heading">
            <div><span>संवाद</span><strong>Chat with Shri Krishna wisdom</strong></div>
            <small>Answers remain grounded in retrieved passages</small>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:
        icon_uri = image_data_uri(str(KRISHNA_ICON))
        st.markdown(
            f"""
            <article class="welcome-message">
                <img src="{icon_uri}" alt="Krishna avatar">
                <div><small>श्रीकृष्ण कहते हैं</small><p>आपका स्वागत है। आप जो भी प्रश्न पूछेंगे, यह सहायक उपलब्ध गीता श्लोकों को खोजकर सरल हिन्दी और English में समझाएगा। ✨</p></div>
                <span class="voice-dot">♪</span>
            </article>
            """,
            unsafe_allow_html=True,
        )
        return

    for index, message in enumerate(st.session_state.messages):
        role = str(message.get("role", "assistant"))
        avatar: str = "👤" if role == "user" else str(KRISHNA_ICON)
        with st.chat_message(role, avatar=avatar):
            st.markdown(str(message.get("content", "")))
            if role == "assistant" and message.get("sources"):
                st.caption(f"📜 {len(message['sources'])} retrieved passages grounded this answer")
                if show_sources:
                    with st.expander("Show this answer's evidence"):
                        for source in message["sources"]:
                            st.markdown(
                                f"**{source['reference']}** · similarity `{source['score']:.3f}`"
                            )
                            st.text(source["text"])
            if role == "assistant" and message.get("technical_error"):
                with st.expander("Technical details"):
                    st.code(str(message["technical_error"]))


def render_question_form() -> str | None:
    with st.form("ask-gita-form", clear_on_submit=True):
        input_column, submit_column = st.columns([6, 1.15], vertical_alignment="bottom")
        with input_column:
            typed_question = st.text_input(
                "Ask your question",
                placeholder="अपने प्रश्न यहाँ लिखें…  (Ask your question here…)",
                label_visibility="collapsed",
            )
        with submit_column:
            submitted = st.form_submit_button("➤ पूछें", use_container_width=True)
    if submitted and typed_question.strip():
        return typed_question.strip()
    return None


def render_source_panel(sources: Sequence[Mapping[str, Any]], *, enabled: bool) -> None:
    st.markdown(
        """
        <section class="right-panel-title" id="how-it-works">
            <span>📜</span><div><strong>संदर्भित श्लोक</strong><small>Retrieved Passages</small></div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if not enabled:
        st.markdown(
            """
            <div class="sources-empty"><b>Retrieval evidence is hidden</b><span>Enable “Show Retrieved Passages” in Sādhana Controls.</span></div>
            """,
            unsafe_allow_html=True,
        )
        return

    if not sources:
        st.markdown(
            """
            <div class="sources-empty"><b>Ask your first question</b><span>The most relevant Gita passages and similarity scores will appear here before the answer is narrated.</span></div>
            """,
            unsafe_allow_html=True,
        )
        return

    for source in sources[:4]:
        reference = html.escape(str(source.get("reference", "Curated Gita passage")))
        source_text = str(source.get("text", "")).strip()
        preview = source_text if len(source_text) <= 315 else f"{source_text[:312].rstrip()}…"
        safe_text = html.escape(preview).replace("\n", "<br>")
        score = float(source.get("score", 0.0))
        percentage = score_percentage(score)
        st.markdown(
            f"""
            <article class="retrieval-card">
                <header><strong>{reference}</strong><span>Similarity: {score:.2f}</span></header>
                <p>{safe_text}</p>
                <div class="similarity-track"><i style="width:{percentage}%"></i></div>
            </article>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("View full retrieved passages"):
        for source in sources:
            st.markdown(
                f"**{source.get('reference', 'Curated Gita passage')}** · "
                f"similarity `{float(source.get('score', 0.0)):.3f}`"
            )
            st.text(str(source.get("text", "")))


def render_about_strip() -> None:
    st.markdown(
        """
        <section class="about-strip" id="about-gita">
            <div><span>①</span><strong>Retrieve</strong><small>FAISS finds relevant passages.</small></div>
            <div><span>②</span><strong>Ground</strong><small>The prompt receives only retrieved evidence.</small></div>
            <div><span>③</span><strong>Explain</strong><small>Hindi and English guidance is generated.</small></div>
            <div><span>④</span><strong>Listen</strong><small>Tap Krishna for Hindi narration.</small></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def process_question(
    *,
    question: str,
    generation_mode: str,
    embedding_mode: str,
    model_name: str,
    api_key: str | None,
    memory_window: int,
    top_k: int,
) -> None:
    clean_question = question.strip()
    if not clean_question:
        return
    if generation_mode == "groq" and not api_key:
        st.error("Add a valid Groq API key in the sidebar or in your .env file.")
        return

    history = conversation_pairs(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": clean_question})

    try:
        with st.spinner("Relevant श्लोक खोजे जा रहे हैं और उत्तर तैयार हो रहा है…"):
            knowledge_base = get_knowledge_base(embedding_mode)
            result: AnswerResult = answer_question(
                question=clean_question,
                history=history,
                memory_window=memory_window,
                knowledge_base=knowledge_base,
                generation_mode=generation_mode,  # type: ignore[arg-type]
                model_name=model_name,
                api_key=api_key,
                top_k=top_k,
            )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result.answer,
                "narratable": True,
                "sources": [
                    {
                        "reference": passage.reference,
                        "text": passage.text,
                        "score": passage.score,
                    }
                    for passage in result.sources
                ],
            }
        )
    except Exception as exc:
        error_message = (
            "The request could not be completed. Check the selected model, API key, "
            "internet connection, and local Ollama service."
        )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
                "narratable": False,
                "technical_error": f"{type(exc).__name__}: {exc}",
            }
        )
    st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []

render_ambient_world()
(
    generation_mode,
    embedding_mode,
    model_name,
    groq_api_key,
    memory_window,
    top_k,
    show_sources,
) = render_sidebar()

render_top_navigation()

main_column, right_column = st.columns([1.72, 0.72], gap="medium")
question_to_process: str | None = None

with main_column:
    render_hero(memory_window=memory_window, top_k=top_k)
    quick_question = render_quick_questions()
    render_chat_history(show_sources=show_sources)
    typed_question = render_question_form()
    question_to_process = typed_question or quick_question
    render_about_strip()

with right_column:
    current_answer = latest_answer(st.session_state.messages)
    narration = narration_for_answer(current_answer)
    context_label = (
        "नवीनतम उत्तर की हिन्दी व्याख्या"
        if current_answer
        else "स्वागत संदेश · हिन्दी वाणी"
    )
    render_krishna_voice_console(
        speech_text=narration,
        image_path=KRISHNA_VOICE,
        icon_path=KRISHNA_ICON,
        context_label=context_label,
    )
    render_source_panel(latest_sources(st.session_state.messages), enabled=show_sources)

st.markdown(
    """
    <footer class="temple-footer">ॐ &nbsp; Hare Krishna Hare Krishna, Krishna Krishna Hare Hare, Hare Rama Hare Rama, Rama Rama Hare Hare &nbsp; ॐ</footer>
    """,
    unsafe_allow_html=True,
)

if question_to_process:
    process_question(
        question=question_to_process,
        generation_mode=generation_mode,
        embedding_mode=embedding_mode,
        model_name=model_name,
        api_key=groq_api_key,
        memory_window=memory_window,
        top_k=top_k,
    )
