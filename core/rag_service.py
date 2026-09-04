"""Retrieval and generation services for the Bhagavad Gita assistant.

The module deliberately uses FAISS directly. This keeps the vector-search behaviour
visible and avoids coupling the project to a vector-store wrapper.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, Sequence

import numpy as np

from core.config import (
    DATA_FILE,
    DEFAULT_OLLAMA_CHAT_MODEL,
    DEFAULT_OLLAMA_EMBEDDING_MODEL,
    DEFAULT_RETRIEVAL_CONFIG,
    DEFAULT_SENTENCE_TRANSFORMER_MODEL,
    RetrievalConfig,
)
from core.prompts import ConversationTurn, build_rag_prompt

EmbeddingMode = Literal["sentence-transformer", "ollama"]
GenerationMode = Literal["groq", "ollama"]


class EmbeddingBackend(Protocol):
    """Small interface shared by local SentenceTransformer and Ollama embeddings."""

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...


@dataclass(frozen=True, slots=True)
class RetrievedPassage:
    reference: str
    text: str
    score: float
    chunk_id: int


@dataclass(frozen=True, slots=True)
class AnswerResult:
    answer: str
    sources: tuple[RetrievedPassage, ...]


class SentenceTransformerBackend:
    """Adapter exposing SentenceTransformer through the project's embedding interface."""

    def __init__(self, model_name: str = DEFAULT_SENTENCE_TRANSFORMER_MODEL) -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        vectors = self._model.encode(
            list(texts),
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vectors.astype("float32").tolist()

    def embed_query(self, text: str) -> list[float]:
        vector = self._model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vector.astype("float32").tolist()


class OllamaEmbeddingBackend:
    """Adapter for an Ollama embedding model running on the user's machine."""

    def __init__(self, model_name: str = DEFAULT_OLLAMA_EMBEDDING_MODEL) -> None:
        from langchain_ollama import OllamaEmbeddings

        self._embeddings = OllamaEmbeddings(model=model_name)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return self._embeddings.embed_documents(list(texts))

    def embed_query(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)


class FaissKnowledgeBase:
    """In-memory cosine-similarity index over curated Gita passages."""

    def __init__(self, chunks: Sequence[str], embeddings: EmbeddingBackend) -> None:
        if not chunks:
            raise ValueError("Cannot build an index without text chunks")

        import faiss

        self._chunks = tuple(chunks)
        self._embeddings = embeddings

        vectors = np.asarray(embeddings.embed_documents(self._chunks), dtype="float32")
        if vectors.ndim != 2 or vectors.shape[0] != len(self._chunks):
            raise ValueError("Embedding backend returned an invalid document matrix")

        # Inner product over L2-normalised vectors is cosine similarity.
        faiss.normalize_L2(vectors)
        self._index = faiss.IndexFlatIP(vectors.shape[1])
        self._index.add(vectors)

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    def search(self, query: str, *, top_k: int) -> tuple[RetrievedPassage, ...]:
        import faiss

        clean_query = query.strip()
        if not clean_query:
            raise ValueError("Search query cannot be empty")

        query_vector = np.asarray(
            [self._embeddings.embed_query(clean_query)], dtype="float32"
        )
        if query_vector.ndim != 2:
            raise ValueError("Embedding backend returned an invalid query vector")

        faiss.normalize_L2(query_vector)
        result_count = min(max(top_k, 1), len(self._chunks))
        scores, indices = self._index.search(query_vector, result_count)

        results: list[RetrievedPassage] = []
        for score, index in zip(scores[0], indices[0], strict=True):
            if index < 0:
                continue
            text = self._chunks[int(index)]
            results.append(
                RetrievedPassage(
                    reference=_extract_reference(text),
                    text=text,
                    score=float(score),
                    chunk_id=int(index),
                )
            )
        return tuple(results)


def load_knowledge_chunks(
    data_file: Path = DATA_FILE,
    config: RetrievalConfig = DEFAULT_RETRIEVAL_CONFIG,
) -> list[str]:
    """Load curated entries and split any unusually long entry safely."""

    config.validate()
    if not data_file.exists():
        raise FileNotFoundError(f"Knowledge-base file not found: {data_file}")

    raw_text = data_file.read_text(encoding="utf-8").strip()
    if not raw_text:
        raise ValueError(f"Knowledge-base file is empty: {data_file}")

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=["\n\n", "\n", "।", ". ", " "],
    )

    # Entries are separated intentionally, so a verse and its translations usually stay
    # in the same retrieval unit. The splitter is a fallback for larger entries.
    entries = [entry.strip() for entry in raw_text.split("\n---\n") if entry.strip()]
    chunks: list[str] = []
    for entry in entries:
        chunks.extend(part.strip() for part in splitter.split_text(entry) if part.strip())
    return chunks


def build_knowledge_base(
    embedding_mode: EmbeddingMode,
    *,
    data_file: Path = DATA_FILE,
    config: RetrievalConfig = DEFAULT_RETRIEVAL_CONFIG,
) -> FaissKnowledgeBase:
    """Create the embedding backend and FAISS index for one application mode."""

    chunks = load_knowledge_chunks(data_file=data_file, config=config)
    if embedding_mode == "sentence-transformer":
        backend: EmbeddingBackend = SentenceTransformerBackend()
    elif embedding_mode == "ollama":
        backend = OllamaEmbeddingBackend()
    else:  # Defensive branch for callers outside static type checking.
        raise ValueError(f"Unsupported embedding mode: {embedding_mode}")
    return FaissKnowledgeBase(chunks, backend)


def answer_question(
    *,
    question: str,
    history: Sequence[ConversationTurn],
    memory_window: int,
    knowledge_base: FaissKnowledgeBase,
    generation_mode: GenerationMode,
    model_name: str,
    api_key: str | None = None,
    top_k: int = DEFAULT_RETRIEVAL_CONFIG.top_k,
) -> AnswerResult:
    """Retrieve evidence, construct a grounded prompt, and invoke the selected model."""

    passages = knowledge_base.search(question, top_k=top_k)
    context = "\n\n".join(
        f"[Retrieved source {position}: {passage.reference}]\n{passage.text}"
        for position, passage in enumerate(passages, start=1)
    )
    prompt = build_rag_prompt(
        question=question,
        context=context,
        history=history,
        memory_window=memory_window,
    )

    if generation_mode == "groq":
        if not api_key or not api_key.strip():
            raise ValueError("A Groq API key is required for cloud mode")
        from langchain_groq import ChatGroq

        model = ChatGroq(
            api_key=api_key.strip(),
            model=model_name,
            temperature=0.2,
            max_retries=2,
        )
    elif generation_mode == "ollama":
        from langchain_ollama import ChatOllama

        model = ChatOllama(
            model=model_name or DEFAULT_OLLAMA_CHAT_MODEL,
            temperature=0.2,
        )
    else:
        raise ValueError(f"Unsupported generation mode: {generation_mode}")

    response = model.invoke(prompt)
    answer = _coerce_message_content(getattr(response, "content", response)).strip()
    if not answer:
        raise RuntimeError("The model returned an empty response")
    return AnswerResult(answer=answer, sources=passages)


def _extract_reference(text: str) -> str:
    match = re.search(r"\[BG\s+([^\]]+)\]", text, flags=re.IGNORECASE)
    return f"Bhagavad Gita {match.group(1)}" if match else "Curated Gita passage"


def _coerce_message_content(content: object) -> str:
    """Handle both string and block-list message formats from chat providers."""

    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces: list[str] = []
        for block in content:
            if isinstance(block, str):
                pieces.append(block)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                pieces.append(block["text"])
        return "\n".join(pieces)
    return str(content)
