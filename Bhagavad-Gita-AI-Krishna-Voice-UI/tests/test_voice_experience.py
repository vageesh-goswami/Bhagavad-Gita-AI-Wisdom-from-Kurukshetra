from core.voice_experience import (
    DEFAULT_WELCOME_HINDI,
    extract_hindi_explanation,
    markdown_to_speech_text,
    narration_for_answer,
)


def test_extracts_hindi_section_from_project_response_format() -> None:
    answer = """### Sanskrit Shloka
कर्मण्येवाधिकारस्ते।

### Hindi Explanation
**कर्म पर ध्यान दें।** फल की चिंता मन को अशांत करती है।

### English Explanation
Focus on action.

### Practical Application
- Prepare a checklist.
"""

    narration = extract_hindi_explanation(answer)

    assert "कर्म पर ध्यान दें" in narration
    assert "फल की चिंता" in narration
    assert "Focus on action" not in narration


def test_accepts_devanagari_hindi_heading() -> None:
    answer = """## हिन्दी व्याख्या
अपने मन को अभ्यास और वैराग्य से स्थिर करें।

## अंग्रेज़ी व्याख्या
Steady the mind.
"""

    assert extract_hindi_explanation(answer) == (
        "अपने मन को अभ्यास और वैराग्य से स्थिर करें"
    )


def test_markdown_is_removed_for_natural_speech() -> None:
    text = "- **पहला कदम:** आज का कर्तव्य लिखें।\n- [दूसरा कदम](https://example.com): शांत रहें।"

    spoken = markdown_to_speech_text(text)

    assert "**" not in spoken
    assert "https://" not in spoken
    assert "पहला कदम" in spoken
    assert "दूसरा कदम" in spoken


def test_narration_uses_welcome_before_first_answer() -> None:
    assert narration_for_answer(None) == DEFAULT_WELCOME_HINDI


def test_missing_hindi_section_returns_clear_fallback() -> None:
    narration = narration_for_answer("### English Explanation\nOnly English is present.")

    assert "हिन्दी व्याख्या नहीं मिली" in narration
