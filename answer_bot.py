"""Command-line client that reuses the same RAG service as the Streamlit app."""

from __future__ import annotations

import argparse
import getpass
import os

from dotenv import load_dotenv

from core.config import DEFAULT_GROQ_MODEL, DEFAULT_OLLAMA_CHAT_MODEL
from core.rag_service import answer_question, build_knowledge_base


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask a grounded Bhagavad Gita question")
    parser.add_argument("question", help="Question to ask")
    parser.add_argument("--mode", choices=("groq", "ollama"), default="groq")
    parser.add_argument("--model", help="Override the default generation model")
    parser.add_argument("--top-k", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    if args.mode == "groq":
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            api_key = getpass.getpass("Groq API key: ").strip()
        embedding_mode = "sentence-transformer"
        model_name = args.model or DEFAULT_GROQ_MODEL
    else:
        api_key = None
        embedding_mode = "ollama"
        model_name = args.model or DEFAULT_OLLAMA_CHAT_MODEL

    knowledge_base = build_knowledge_base(embedding_mode)  # type: ignore[arg-type]
    result = answer_question(
        question=args.question,
        history=[],
        memory_window=1,
        knowledge_base=knowledge_base,
        generation_mode=args.mode,
        model_name=model_name,
        api_key=api_key,
        top_k=args.top_k,
    )

    print("\n" + result.answer)
    print("\nRetrieved sources:")
    for passage in result.sources:
        print(f"- {passage.reference} (similarity={passage.score:.3f})")


if __name__ == "__main__":
    main()
