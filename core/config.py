"""Central configuration for the application.

Keeping settings in one module prevents model names and retrieval parameters from
being duplicated across the Streamlit UI, CLI, and tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "gita_knowledge_base.txt"

GROQ_MODELS: tuple[str, ...] = (
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
)
DEFAULT_GROQ_MODEL = GROQ_MODELS[0]
DEFAULT_OLLAMA_CHAT_MODEL = "mistral"
DEFAULT_OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_SENTENCE_TRANSFORMER_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


@dataclass(frozen=True, slots=True)
class RetrievalConfig:
    """Parameters that control text splitting and semantic retrieval."""

    chunk_size: int = 1_400
    chunk_overlap: int = 120
    top_k: int = 4

    def validate(self) -> None:
        if self.chunk_size < 200:
            raise ValueError("chunk_size must be at least 200 characters")
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("chunk_overlap must be between 0 and chunk_size - 1")
        if self.top_k < 1:
            raise ValueError("top_k must be at least 1")


DEFAULT_RETRIEVAL_CONFIG = RetrievalConfig()

