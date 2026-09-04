from core.prompts import build_rag_prompt, format_history


def test_history_respects_memory_window() -> None:
    history = [
        ("first question", "first answer"),
        ("second question", "second answer"),
        ("third question", "third answer"),
    ]

    rendered = format_history(history, window=2)

    assert "first question" not in rendered
    assert "second question" in rendered
    assert "third question" in rendered


def test_zero_window_omits_history() -> None:
    assert format_history([("question", "answer")], window=0) == (
        "(No previous conversation.)"
    )


def test_prompt_contains_question_context_and_guardrails() -> None:
    prompt = build_rag_prompt(
        question="How should I prepare for an interview?",
        context="[BG 2.47] Focus on action rather than results.",
        history=[("What is karma?", "Karma means action.")],
        memory_window=1,
    )

    assert "How should I prepare for an interview?" in prompt
    assert "[BG 2.47]" in prompt
    assert "What is karma?" in prompt
    assert "Never invent" in prompt


def test_blank_question_is_rejected() -> None:
    try:
        build_rag_prompt(
            question="   ",
            context="some context",
            history=[],
            memory_window=1,
        )
    except ValueError as exc:
        assert "Question cannot be empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError for a blank question")
