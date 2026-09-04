# Shri Krishna Vāṇī — Interactive Hindi Narration

This frontend upgrade adds an immersive, tap-to-listen Hindi narration experience to the existing source-grounded Bhagavad Gita RAG application.

## User experience

1. Before the first question, the user sees a compact **“श्रीकृष्ण को सुनें”** portrait card.
2. Tapping the portrait expands a large divine avatar featuring **Sheshnag, Sudarshan Chakra, Shankha, Gada, and Padma**.
3. The same tap starts a short welcome narration in Hindi.
4. After a successful answer, the card moves below the conversation and narrates only the answer's **Hindi Explanation** section.
5. The user can pause, resume, replay, stop, close the stage, and select a slower or faster speaking rate.

## Technical design

- `core/voice_experience.py` extracts the Hindi response section, removes Markdown for natural speech, and renders the interactive component.
- Narration uses the browser's Web Speech API with `lang="hi-IN"` and prioritises an installed Hindi voice.
- Long responses are divided into sentence-sized chunks to avoid browser speech truncation.
- Audio starts only after an explicit tap, respecting browser autoplay rules.
- The model response is embedded into JavaScript through JSON encoding, while visible text is HTML-escaped.
- No additional TTS API key, paid service, or Python dependency is required.
- A small AI narration label avoids presenting the browser-generated voice as an authentic historical or divine recording.

## Files added or changed

```text
app.py
core/styles.py
core/voice_experience.py
assets/krishna_divine.webp
assets/krishna_icon.webp
tests/test_voice_experience.py
KRISHNA_VOICE_FEATURE.md
```

The update does not replace `core/config.py`, `.env`, the FAISS retrieval code, the curated knowledge base, or the existing Groq/Ollama provider implementation.

## Browser requirement

Chrome or Edge is recommended. The browser and operating system must expose a Hindi voice for the best pronunciation. When no Hindi voice is installed, the component falls back to an available Indian or default system voice and shows a status message if speech cannot start.

## Demonstration flow

Ask:

```text
फल की चिंता छोड़कर कर्म पर ध्यान कैसे दूँ?
```

After the answer appears, tap **“श्रीकृष्ण को सुनें”**. The avatar expands and narrates the Hindi section. Pause once, resume, then show the retrieved passages to demonstrate that the narration is based on the source-grounded answer.
