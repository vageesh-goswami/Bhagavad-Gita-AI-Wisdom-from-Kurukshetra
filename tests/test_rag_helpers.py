from core.rag_service import _coerce_message_content, _extract_reference


def test_reference_is_extracted_from_chunk() -> None:
    assert _extract_reference("[BG 2.47] Topic: action") == "Bhagavad Gita 2.47"


def test_missing_reference_uses_safe_fallback() -> None:
    assert _extract_reference("General passage") == "Curated Gita passage"


def test_message_content_blocks_are_joined() -> None:
    content = [
        {"type": "text", "text": "First paragraph."},
        {"type": "text", "text": "Second paragraph."},
    ]
    assert _coerce_message_content(content) == "First paragraph.\nSecond paragraph."
