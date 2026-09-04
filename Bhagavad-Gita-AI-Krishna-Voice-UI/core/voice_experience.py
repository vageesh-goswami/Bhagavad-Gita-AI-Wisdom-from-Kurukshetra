"""Interactive Hindi narration experience for the Streamlit frontend.

The component uses the browser's Web Speech API. This keeps the feature optional,
requires no additional paid service, and ensures that speech starts only after an
explicit user gesture.
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path
from uuid import uuid4

import streamlit.components.v1 as components

DEFAULT_WELCOME_HINDI = (
    "नमस्ते। मैं श्रीकृष्ण के स्वरूप में, भगवद्गीता के उपलब्ध श्लोकों के आधार पर "
    "आपके प्रश्न को सरल हिन्दी में समझाऊँगा। नीचे अपना प्रश्न लिखिए। उत्तर मिलने के "
    "बाद मेरे चित्र पर स्पर्श करके हिन्दी व्याख्या सुनिए।"
)


def _normalise_heading(line: str) -> str:
    """Return a markdown heading as plain, lower-case text."""

    cleaned = re.sub(r"^[\s#>*_`~-]+|[\s#>*_`~:-]+$", "", line).strip()
    return re.sub(r"\s+", " ", cleaned).casefold()


def markdown_to_speech_text(markdown_text: str) -> str:
    """Convert a small markdown response section into browser-friendly speech text."""

    text = html.unescape(markdown_text.strip())
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", text)
    text = text.replace("**", "").replace("__", "").replace("~~", "")
    text = re.sub(r"(?<!\w)[*_](?!\w)|(?<=\w)[*_](?!\w)", "", text)
    text = re.sub(r"[\t\r ]+", " ", text)
    text = re.sub(r"\n{2,}", "। ", text)
    text = re.sub(r"\s*\n\s*", "। ", text)
    text = re.sub(r"।{2,}", "।", text)
    text = re.sub(r"\s+", " ", text).strip(" ।")
    return text


def extract_hindi_explanation(answer_markdown: str) -> str:
    """Extract the Hindi section produced by the project's grounded prompt.

    The parser accepts both the English heading from ``core.prompts`` and common
    Devanagari heading variants, then stops at the English or practical section.
    If no dedicated Hindi section is found, an empty string is returned instead of
    narrating unrelated Sanskrit/English content.
    """

    lines = answer_markdown.splitlines()
    start_index: int | None = None
    end_index: int | None = None

    start_headings = {
        "hindi explanation",
        "hindi",
        "हिंदी व्याख्या",
        "हिन्दी व्याख्या",
        "हिंदी में व्याख्या",
        "हिन्दी में व्याख्या",
    }
    end_headings = {
        "english explanation",
        "english",
        "practical application",
        "practical applications",
        "अंग्रेज़ी व्याख्या",
        "व्यावहारिक उपयोग",
        "व्यावहारिक अनुप्रयोग",
    }

    for index, line in enumerate(lines):
        heading = _normalise_heading(line)
        if start_index is None:
            if heading in start_headings:
                start_index = index + 1
            continue

        if heading in end_headings:
            end_index = index
            break

    if start_index is None:
        return ""

    section = "\n".join(lines[start_index:end_index]).strip()
    return markdown_to_speech_text(section)


def narration_for_answer(answer_markdown: str | None) -> str:
    """Return the latest Hindi explanation, or a respectful welcome narration."""

    if not answer_markdown:
        return DEFAULT_WELCOME_HINDI
    hindi = extract_hindi_explanation(answer_markdown)
    if hindi:
        return hindi
    return (
        "इस उत्तर में अलग हिन्दी व्याख्या नहीं मिली। कृपया प्रश्न को दोबारा पूछें, "
        "ताकि मैं उपलब्ध गीता श्लोकों के आधार पर हिन्दी में समझा सकूँ।"
    )


def _image_data_uri(image_path: Path) -> str:
    suffix = image_path.suffix.casefold()
    mime_by_suffix = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    mime = mime_by_suffix.get(suffix, "application/octet-stream")
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_krishna_voice_stage(
    *,
    speech_text: str,
    image_path: Path,
    icon_path: Path | None = None,
    context_label: str = "भगवद्गीता की हिन्दी व्याख्या",
) -> None:
    """Render a tap-to-expand Krishna narration stage.

    The first click both expands the avatar and starts Hindi speech. Because the
    click and speech invocation happen inside the same browser component, it works
    with browser autoplay protections instead of trying to start audio on page load.
    """

    if not image_path.exists():
        raise FileNotFoundError(f"Krishna avatar asset not found: {image_path}")
    launcher_icon = icon_path or image_path
    if not launcher_icon.exists():
        raise FileNotFoundError(f"Krishna icon asset not found: {launcher_icon}")

    clean_speech = speech_text.strip() or DEFAULT_WELCOME_HINDI
    preview = clean_speech if len(clean_speech) <= 330 else f"{clean_speech[:327].rstrip()}…"
    template = _VOICE_COMPONENT_TEMPLATE
    replacements = {
        "__IMAGE_URI__": _image_data_uri(image_path),
        "__ICON_URI__": _image_data_uri(launcher_icon),
        "__SPEECH_JSON__": json.dumps(clean_speech, ensure_ascii=False),
        "__PREVIEW_HTML__": html.escape(preview),
        "__CONTEXT_HTML__": html.escape(context_label),
        "__INSTANCE_JSON__": json.dumps(f"krishna-voice-{uuid4().hex}"),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    components.html(template, height=172, scrolling=False)


_VOICE_COMPONENT_TEMPLATE = r"""
<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
:root {
  --ink:#071020; --navy:#07152f; --blue:#112760; --violet:#29135b;
  --gold:#f4c862; --gold2:#ffdda0; --saffron:#f39a3d; --cream:#fff8e8;
  --muted:#c9c4d6; --line:rgba(244,200,98,.28); --glass:rgba(8,15,38,.76);
}
*{box-sizing:border-box}
html,body{margin:0;background:transparent;color:var(--cream);font-family:Inter,'Noto Sans Devanagari',sans-serif;overflow:hidden}
button,select{font:inherit}
.voice-widget{width:100%;position:relative}
.voice-launcher{
  width:100%;height:154px;padding:15px 18px;border:1px solid var(--line);border-radius:24px;
  display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:center;text-align:left;
  color:var(--cream);cursor:pointer;overflow:hidden;position:relative;
  background:radial-gradient(circle at 16% 30%,rgba(244,200,98,.17),transparent 28%),
             linear-gradient(125deg,rgba(13,29,69,.96),rgba(22,12,53,.96));
  box-shadow:0 20px 58px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.08);
  transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;
}
.voice-launcher::after{content:"";position:absolute;inset:-120% auto -120% -22%;width:24%;transform:rotate(16deg);background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);animation:shine 7s ease-in-out infinite}
.voice-launcher:hover{transform:translateY(-3px);border-color:rgba(255,221,160,.7);box-shadow:0 24px 66px rgba(0,0,0,.4),0 0 34px rgba(244,200,98,.12)}
.mini-avatar{position:relative;width:104px;height:104px;border-radius:50%;padding:4px;background:linear-gradient(145deg,var(--gold2),var(--saffron));box-shadow:0 0 0 7px rgba(244,200,98,.08),0 0 34px rgba(244,200,98,.26)}
.mini-avatar img{width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:50% 34%;display:block;border:3px solid #111735}
.mini-avatar .pulse{position:absolute;inset:-10px;border:1px solid rgba(244,200,98,.46);border-radius:50%;animation:pulse 2.5s ease-out infinite}
.launcher-copy small{display:block;margin-bottom:5px;color:var(--gold);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.launcher-copy strong{display:block;font-family:'Cormorant Garamond','Noto Sans Devanagari',serif;font-size:clamp(23px,3vw,32px);line-height:1.04;color:var(--gold2)}
.launcher-copy span{display:block;margin-top:7px;color:#d9d4e2;font-size:13px;line-height:1.5}
.launcher-action{min-width:154px;padding:13px 17px;border:1px solid rgba(244,200,98,.42);border-radius:999px;text-align:center;color:#171121;background:linear-gradient(135deg,var(--gold2),var(--gold));font-weight:800;box-shadow:0 8px 24px rgba(244,200,98,.18)}
.voice-stage{display:none;position:relative;min-height:592px;border:1px solid rgba(244,200,98,.44);border-radius:28px;overflow:hidden;background:linear-gradient(135deg,#07152f 0%,#111840 48%,#28104d 100%);box-shadow:0 28px 90px rgba(0,0,0,.5),0 0 60px rgba(244,200,98,.11);isolation:isolate}
.voice-stage::before{content:"";position:absolute;inset:0;z-index:-3;background:radial-gradient(circle at 27% 42%,rgba(244,200,98,.2),transparent 31%),radial-gradient(circle at 78% 20%,rgba(101,117,255,.18),transparent 35%)}
.voice-stage::after{content:"ॐ";position:absolute;right:-35px;bottom:-135px;z-index:-2;color:rgba(244,200,98,.035);font-family:'Noto Sans Devanagari',serif;font-size:390px;line-height:1}
.voice-widget.open .voice-launcher{display:none}
.voice-widget.open .voice-stage{display:grid;grid-template-columns:minmax(320px,46%) 1fr}
.close-button{position:absolute;right:16px;top:16px;z-index:20;width:40px;height:40px;border:1px solid rgba(255,255,255,.14);border-radius:50%;color:var(--cream);background:rgba(2,8,23,.58);cursor:pointer;backdrop-filter:blur(10px);font-size:19px}
.avatar-zone{position:relative;min-height:592px;display:flex;align-items:flex-end;justify-content:center;padding:28px 20px 0;overflow:hidden;background:linear-gradient(to top,rgba(2,8,23,.95),transparent 42%)}
.avatar-zone::before{content:"";position:absolute;width:430px;height:430px;left:50%;top:38%;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,218,128,.27),rgba(244,153,61,.07) 48%,transparent 69%);filter:blur(2px);animation:aura 4s ease-in-out infinite}
.avatar-frame{position:relative;width:min(100%,470px);height:554px;border-radius:240px 240px 34px 34px;overflow:hidden;border:1px solid rgba(255,221,160,.42);box-shadow:0 0 0 9px rgba(244,200,98,.04),0 0 56px rgba(244,200,98,.25);transform-origin:center bottom;animation:float 5s ease-in-out infinite}
.avatar-frame img{width:100%;height:100%;display:block;object-fit:cover;object-position:center top;filter:saturate(1.08) contrast(1.03)}
.avatar-frame::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(3,8,24,.76),transparent 30%,rgba(255,211,113,.05));pointer-events:none}
.voice-widget.speaking .avatar-frame{box-shadow:0 0 0 10px rgba(244,200,98,.08),0 0 90px rgba(255,203,82,.46);animation:speakingFloat 1.8s ease-in-out infinite}
.divine-symbol{position:absolute;z-index:6;padding:7px 11px;border:1px solid rgba(244,200,98,.32);border-radius:999px;color:var(--gold2);background:rgba(5,13,35,.72);font-size:11px;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,.2);backdrop-filter:blur(10px)}
.sym-chakra{left:15px;top:76px}.sym-shankha{right:14px;top:112px}.sym-padma{left:14px;bottom:62px}.sym-gada{right:14px;bottom:72px}.sym-shesh{left:50%;top:19px;transform:translateX(-50%)}
.stage-copy{padding:58px 48px 38px 42px;display:flex;flex-direction:column;justify-content:center;min-width:0}
.eyebrow{color:var(--gold);font-size:11px;font-weight:800;letter-spacing:.17em;text-transform:uppercase}
.stage-copy h2{margin:9px 0 5px;font-family:'Cormorant Garamond','Noto Sans Devanagari',serif;font-size:clamp(35px,5vw,55px);line-height:.98;color:var(--gold2)}
.stage-copy .subtitle{margin:0;color:#e2dce9;font-family:'Noto Sans Devanagari',Inter,sans-serif;font-size:16px;line-height:1.7}
.ai-note{display:inline-flex;align-items:center;gap:8px;width:max-content;margin-top:13px;padding:7px 10px;border:1px solid rgba(113,219,166,.2);border-radius:999px;color:#94e1b9;background:rgba(67,171,119,.08);font-size:11px;font-weight:700}
.narration-card{margin-top:22px;padding:18px 18px 16px;border:1px solid rgba(244,200,98,.2);border-radius:18px;background:rgba(5,10,29,.45);box-shadow:inset 0 1px 0 rgba(255,255,255,.05)}
.narration-card p{margin:0;color:#f1edf4;font-family:'Noto Sans Devanagari',Inter,sans-serif;font-size:14px;line-height:1.72}
.voice-status{display:flex;align-items:center;gap:9px;margin-top:15px;color:#c7bed1;font-size:12px;font-weight:600}
.status-orb{width:9px;height:9px;border-radius:50%;background:#8f87a5;box-shadow:0 0 0 5px rgba(143,135,165,.08)}
.voice-widget.speaking .status-orb{background:#78e2a7;box-shadow:0 0 0 6px rgba(120,226,167,.1),0 0 18px rgba(120,226,167,.6);animation:pulse 1.3s ease-out infinite}
.wave{height:42px;margin:14px 0 17px;display:flex;align-items:center;gap:5px;overflow:hidden}
.wave i{display:block;width:4px;height:8px;border-radius:99px;background:linear-gradient(to top,var(--saffron),var(--gold2));opacity:.42;transform-origin:center}
.voice-widget.speaking .wave i{opacity:1;animation:wave 1s ease-in-out infinite}
.wave i:nth-child(2n){animation-delay:-.35s}.wave i:nth-child(3n){animation-delay:-.6s}.wave i:nth-child(5n){animation-delay:-.15s}
.controls{display:flex;align-items:center;flex-wrap:wrap;gap:9px}
.control{min-height:42px;padding:10px 14px;border:1px solid rgba(244,200,98,.24);border-radius:12px;color:var(--cream);background:rgba(255,255,255,.045);cursor:pointer;font-weight:700;transition:.18s ease}
.control:hover{border-color:rgba(244,200,98,.65);color:var(--gold2);transform:translateY(-1px)}
.control.primary{min-width:150px;color:#171121;border-color:transparent;background:linear-gradient(135deg,var(--gold2),var(--gold));box-shadow:0 9px 25px rgba(244,200,98,.18)}
.rate-select{height:42px;padding:0 10px;border:1px solid rgba(244,200,98,.22);border-radius:12px;color:var(--cream);background:#11183b;cursor:pointer}
.voice-help{margin-top:14px;color:#978da5;font-size:11px;line-height:1.55}
@keyframes shine{0%,50%{transform:translateX(-120%) rotate(16deg)}78%,100%{transform:translateX(610%) rotate(16deg)}}
@keyframes pulse{0%{transform:scale(.88);opacity:.8}100%{transform:scale(1.2);opacity:0}}
@keyframes aura{0%,100%{transform:translate(-50%,-50%) scale(.94);opacity:.62}50%{transform:translate(-50%,-50%) scale(1.07);opacity:1}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes speakingFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-4px) scale(1.008)}}
@keyframes wave{0%,100%{transform:scaleY(.55)}50%{transform:scaleY(4)}}
@media(max-width:720px){
 .voice-launcher{height:164px;grid-template-columns:auto 1fr;padding:13px}.mini-avatar{width:88px;height:88px}.launcher-action{grid-column:1/-1;min-width:0;padding:8px 12px}.launcher-copy strong{font-size:24px}.launcher-copy span{font-size:12px}
 .voice-widget.open .voice-stage{grid-template-columns:1fr;min-height:744px}.avatar-zone{min-height:370px;padding-top:25px}.avatar-frame{height:390px;width:350px}.stage-copy{padding:32px 23px 28px}.stage-copy h2{font-size:39px}.divine-symbol{font-size:9px}.sym-chakra{top:62px}.sym-shankha{top:88px}
}
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
</style>
</head>
<body>
<div class="voice-widget" id="voiceRoot">
  <button class="voice-launcher" id="voiceLauncher" type="button" aria-label="श्रीकृष्ण की हिन्दी वाणी सुनें">
    <span class="mini-avatar"><img src="__ICON_URI__" alt="श्रीकृष्ण का कलात्मक चित्र" /><span class="pulse"></span></span>
    <span class="launcher-copy">
      <small>Interactive Krishna Vāṇī</small>
      <strong>श्रीकृष्ण को सुनें</strong>
      <span>चित्र पर स्पर्श करें—दिव्य स्वरूप खुलेगा और हिन्दी व्याख्या आरम्भ होगी।</span>
    </span>
    <span class="launcher-action">🎧 हिन्दी वाणी सुनें</span>
  </button>

  <section class="voice-stage" id="voiceStage" aria-live="polite">
    <button class="close-button" id="closeButton" type="button" aria-label="बंद करें">×</button>
    <div class="avatar-zone">
      <span class="divine-symbol sym-shesh">🐍 शेषनाग</span>
      <span class="divine-symbol sym-chakra">☀ सुदर्शन चक्र</span>
      <span class="divine-symbol sym-shankha">🐚 शंख</span>
      <span class="divine-symbol sym-padma">🪷 पद्म</span>
      <span class="divine-symbol sym-gada">♜ गदा</span>
      <div class="avatar-frame"><img src="__IMAGE_URI__" alt="शंख, चक्र, गदा, पद्म और शेषनाग सहित श्रीकृष्ण का कलात्मक स्वरूप" /></div>
    </div>
    <div class="stage-copy">
      <div class="eyebrow">__CONTEXT_HTML__</div>
      <h2>श्रीकृष्ण वाणी</h2>
      <p class="subtitle">गीता के उपलब्ध श्लोकों पर आधारित सरल हिन्दी मार्गदर्शन</p>
      <span class="ai-note">● AI द्वारा प्रस्तुत शैक्षिक हिन्दी narration</span>
      <div class="narration-card"><p>__PREVIEW_HTML__</p></div>
      <div class="voice-status"><span class="status-orb"></span><span id="statusText">हिन्दी आवाज़ तैयार है</span></div>
      <div class="wave" aria-hidden="true">
        <i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
      </div>
      <div class="controls">
        <button class="control primary" id="mainControl" type="button">⏸ विराम</button>
        <button class="control" id="replayButton" type="button">↻ फिर सुनें</button>
        <button class="control" id="stopButton" type="button">■ रोकें</button>
        <select class="rate-select" id="rateSelect" aria-label="वाणी गति">
          <option value="0.78">शांत</option><option value="0.9" selected>सामान्य</option><option value="1.03">तेज़</option>
        </select>
      </div>
      <div class="voice-help">आवाज़ आपके ब्राउज़र की उपलब्ध हिन्दी voice का उपयोग करती है। सर्वोत्तम अनुभव के लिए Chrome या Edge में सिस्टम की Hindi voice enabled रखें।</div>
    </div>
  </section>
</div>
<script>
(() => {
  const speechText = __SPEECH_JSON__;
  const instanceId = __INSTANCE_JSON__;
  const root = document.getElementById('voiceRoot');
  const launcher = document.getElementById('voiceLauncher');
  const closeButton = document.getElementById('closeButton');
  const mainControl = document.getElementById('mainControl');
  const replayButton = document.getElementById('replayButton');
  const stopButton = document.getElementById('stopButton');
  const rateSelect = document.getElementById('rateSelect');
  const statusText = document.getElementById('statusText');
  let state = 'idle';
  let runToken = 0;
  let chunks = [];
  let chunkIndex = 0;
  let activeUtterance = null;

  const setHeight = (height) => window.parent.postMessage({
    isStreamlitMessage: true,
    type: 'streamlit:setFrameHeight',
    height: height
  }, '*');

  const expandedHeight = () => window.innerWidth <= 720 ? 764 : 612;
  const collapsedHeight = () => window.innerWidth <= 720 ? 174 : 164;

  const setState = (next, message) => {
    state = next;
    root.classList.toggle('speaking', next === 'speaking');
    statusText.textContent = message;
    if (next === 'speaking') mainControl.textContent = '⏸ विराम';
    else if (next === 'paused') mainControl.textContent = '▶ आगे सुनें';
    else mainControl.textContent = '▶ वाणी सुनें';
  };

  const chooseVoice = () => {
    const voices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
    const preferredNames = ['Hemant', 'Madhur', 'Hindi Male', 'Google हिन्दी', 'Kalpana'];
    for (const name of preferredNames) {
      const match = voices.find(v => v.name.toLowerCase().includes(name.toLowerCase()) && v.lang.toLowerCase().startsWith('hi'));
      if (match) return match;
    }
    return voices.find(v => v.lang.toLowerCase() === 'hi-in') ||
           voices.find(v => v.lang.toLowerCase().startsWith('hi')) ||
           voices.find(v => v.lang.toLowerCase() === 'en-in') || null;
  };

  const buildChunks = (text) => {
    const parts = text.match(/[^।.!?]+[।.!?]?/g) || [text];
    const output = [];
    let current = '';
    for (const raw of parts) {
      const part = raw.trim();
      if (!part) continue;
      if ((current + ' ' + part).trim().length > 220 && current) {
        output.push(current.trim());
        current = part;
      } else current = (current + ' ' + part).trim();
    }
    if (current) output.push(current);
    return output.length ? output : [text];
  };

  const playChime = () => {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const context = new AudioContext();
      const gain = context.createGain();
      gain.gain.setValueAtTime(0.0001, context.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.045, context.currentTime + 0.035);
      gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.65);
      gain.connect(context.destination);
      [432, 648].forEach((frequency, index) => {
        const oscillator = context.createOscillator();
        oscillator.type = 'sine'; oscillator.frequency.value = frequency;
        oscillator.connect(gain); oscillator.start(context.currentTime + index * 0.04); oscillator.stop(context.currentTime + 0.7);
      });
      setTimeout(() => context.close(), 900);
    } catch (_) { /* Chime is optional. */ }
  };

  const speakNext = (token) => {
    if (token !== runToken || chunkIndex >= chunks.length) {
      if (token === runToken) setState('ended', 'हिन्दी व्याख्या पूर्ण हुई');
      return;
    }
    const utterance = new SpeechSynthesisUtterance(chunks[chunkIndex]);
    activeUtterance = utterance;
    utterance.lang = 'hi-IN';
    utterance.rate = Number(rateSelect.value || 0.9);
    utterance.pitch = 0.82;
    utterance.volume = 1;
    const voice = chooseVoice();
    if (voice) utterance.voice = voice;
    utterance.onend = () => { if (token === runToken) { chunkIndex += 1; speakNext(token); } };
    utterance.onerror = (event) => {
      if (event.error === 'interrupted' || event.error === 'canceled') return;
      setState('error', 'ब्राउज़र आवाज़ आरम्भ नहीं कर सका');
    };
    window.speechSynthesis.speak(utterance);
  };

  const startSpeech = () => {
    if (!('speechSynthesis' in window)) {
      setState('error', 'इस ब्राउज़र में speech synthesis उपलब्ध नहीं है');
      return;
    }
    runToken += 1;
    window.speechSynthesis.cancel();
    chunks = buildChunks(speechText);
    chunkIndex = 0;
    setState('speaking', 'श्रीकृष्ण वाणी चल रही है…');
    speakNext(runToken);
  };

  const stopSpeech = (message='वाणी रोक दी गई') => {
    runToken += 1;
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    activeUtterance = null;
    setState('stopped', message);
  };

  launcher.addEventListener('click', () => {
    root.classList.add('open');
    setHeight(expandedHeight());
    playChime();
    startSpeech();
  });
  closeButton.addEventListener('click', () => {
    stopSpeech('वाणी बंद की गई');
    root.classList.remove('open');
    setHeight(collapsedHeight());
  });
  mainControl.addEventListener('click', () => {
    if (!('speechSynthesis' in window)) return;
    if (state === 'speaking') {
      window.speechSynthesis.pause(); setState('paused', 'वाणी विराम पर है');
    } else if (state === 'paused') {
      window.speechSynthesis.resume(); setState('speaking', 'श्रीकृष्ण वाणी चल रही है…');
    } else startSpeech();
  });
  replayButton.addEventListener('click', startSpeech);
  stopButton.addEventListener('click', () => stopSpeech());
  rateSelect.addEventListener('change', () => { if (state === 'speaking' || state === 'paused') startSpeech(); });
  window.addEventListener('resize', () => setHeight(root.classList.contains('open') ? expandedHeight() : collapsedHeight()));
  if ('speechSynthesis' in window) window.speechSynthesis.onvoiceschanged = () => chooseVoice();
  window.addEventListener('beforeunload', () => stopSpeech(''));
  setHeight(collapsedHeight());
  void instanceId;
})();
</script>
</body>
</html>
"""
