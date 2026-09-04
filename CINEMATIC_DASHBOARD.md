# Cinematic Shri Krishna Dashboard

## Implemented interface

The dashboard follows the supplied concept image rather than using a generic Streamlit
chat layout:

- left **Sādhana Controls** sidebar for inference, model, memory, retrieval, API status,
  daily inspiration, and a chant card;
- sticky temple-style navigation;
- a large central Krishna hero with Sheshnag, Shankha, Chakra, Gada, and Padma imagery;
- animated aura rings, rotating Sudarshan Chakra overlay, slowly breathing/floating
  Krishna image, moving stars, light orbs, fireflies, and falling petals;
- quick Hindi question cards;
- source-grounded chat and evidence count;
- a right-side **Shri Krishna Vāṇī** console;
- retrieved passage cards with similarity bars;
- responsive mobile layout and `prefers-reduced-motion` accessibility.

## Hindi voice behaviour

The voice panel uses the browser Web Speech API. A user gesture is required: tap the
Krishna artwork or the सुनें button. After a successful AI answer, only the dedicated
`### Hindi Explanation` section is narrated. Before the first answer, a welcome message
is spoken.

Controls include play/pause, replay, stop, and narration speed. Chrome or Microsoft Edge
with a Hindi system voice gives the best result. This feature does not upload speech or
require another API key.

## Motion implementation

The interface does not pretend to perform lip-synchronised avatar video. Instead, it
uses presentation-safe motion:

- subtle figure breathing and vertical float;
- pulsing gold aura and rotating sacred rings;
- animated waveform only while narration is active;
- a rotating Chakra treatment;
- drifting petals, moving stars, and fireflies in the page background.

This is visually convincing for a five-minute engineering walkthrough while remaining
fast and reliable on an ordinary laptop.

## Run

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Then use `Ctrl + F5` in Chrome or Edge after applying the update.
