"""Hindi narration helpers and the interactive Shri Krishna voice console.

The browser's Web Speech API is used intentionally: narration begins only after the
user clicks the Krishna avatar, no additional paid TTS key is required, and the
feature remains separate from the RAG backend.
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path
from uuid import uuid4

DEFAULT_WELCOME_HINDI = (
    "नमस्ते। मैं श्रीकृष्ण के स्वरूप में, इस अनुप्रयोग में उपलब्ध भगवद्गीता के "
    "श्लोकों के आधार पर आपके प्रश्न को सरल हिन्दी में समझाऊँगा। अपना प्रश्न पूछिए, "
    "और उत्तर मिलने के बाद मेरे चित्र पर स्पर्श करके हिन्दी व्याख्या सुनिए।"
)


def _normalise_heading(line: str) -> str:
    cleaned = re.sub(r"^[\s#>*_`~-]+|[\s#>*_`~:-]+$", "", line).strip()
    return re.sub(r"\s+", " ", cleaned).casefold()


def markdown_to_speech_text(markdown_text: str) -> str:
    """Turn a small Markdown section into natural browser-speech text."""

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
    return re.sub(r"\s+", " ", text).strip(" ।")


def extract_hindi_explanation(answer_markdown: str) -> str:
    """Extract the dedicated Hindi section from the project's response format."""

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
    return markdown_to_speech_text("\n".join(lines[start_index:end_index]).strip())


def narration_for_answer(answer_markdown: str | None) -> str:
    """Return the latest Hindi explanation, or a respectful welcome message."""

    if not answer_markdown:
        return DEFAULT_WELCOME_HINDI
    hindi = extract_hindi_explanation(answer_markdown)
    if hindi:
        return hindi
    return (
        "इस उत्तर में अलग हिन्दी व्याख्या नहीं मिली। कृपया प्रश्न को दोबारा पूछें, "
        "ताकि उपलब्ध गीता श्लोकों के आधार पर हिन्दी में समझाया जा सके।"
    )


def _image_data_uri(image_path: Path) -> str:
    suffix = image_path.suffix.casefold()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "application/octet-stream")
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_krishna_voice_console(
    *,
    speech_text: str,
    image_path: Path,
    icon_path: Path,
    context_label: str = "भगवद्गीता की हिन्दी व्याख्या",
) -> None:
    """Render the right-side, tap-to-listen Krishna voice console."""

    if not image_path.exists():
        raise FileNotFoundError(f"Krishna image not found: {image_path}")
    if not icon_path.exists():
        raise FileNotFoundError(f"Krishna icon not found: {icon_path}")

    import streamlit.components.v1 as components

    clean_speech = speech_text.strip() or DEFAULT_WELCOME_HINDI
    preview = clean_speech if len(clean_speech) <= 270 else f"{clean_speech[:267].rstrip()}…"
    template = _VOICE_CONSOLE_TEMPLATE
    replacements = {
        "__IMAGE_URI__": _image_data_uri(image_path),
        "__ICON_URI__": _image_data_uri(icon_path),
        "__SPEECH_JSON__": json.dumps(clean_speech, ensure_ascii=False),
        "__PREVIEW_HTML__": html.escape(preview),
        "__CONTEXT_HTML__": html.escape(context_label),
        "__INSTANCE_JSON__": json.dumps(f"krishna-console-{uuid4().hex}"),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    components.html(template, height=535, scrolling=False)


_VOICE_CONSOLE_TEMPLATE = r"""
<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
:root{--navy:#040b20;--navy2:#071633;--violet:#211048;--gold:#f4c45d;--gold2:#ffe2a1;--cream:#fff8e8;--muted:#c2bdd1;--line:rgba(244,196,93,.33)}
*{box-sizing:border-box}
html,body{margin:0;background:transparent;color:var(--cream);font-family:Inter,'Noto Sans Devanagari',sans-serif;overflow:hidden}
button,select{font:inherit}
.console{position:relative;height:520px;border:1px solid var(--line);border-radius:25px;overflow:hidden;isolation:isolate;background:radial-gradient(circle at 50% 24%,rgba(244,196,93,.17),transparent 31%),linear-gradient(145deg,rgba(5,13,36,.98),rgba(14,12,43,.98));box-shadow:0 20px 70px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,255,255,.07)}
.console::before{content:"";position:absolute;inset:-35%;z-index:-3;background:conic-gradient(from 0deg,transparent 0 10%,rgba(244,196,93,.06) 12%,transparent 15% 27%,rgba(109,117,255,.06) 30%,transparent 34% 100%);animation:cosmos 34s linear infinite}
.console::after{content:"ॐ";position:absolute;right:-35px;bottom:-95px;z-index:-2;color:rgba(244,196,93,.035);font-family:'Noto Sans Devanagari',serif;font-size:265px;line-height:1}
.spark{position:absolute;width:4px;height:4px;border-radius:50%;background:var(--gold2);box-shadow:0 0 12px var(--gold);opacity:.7;animation:twinkle 3s ease-in-out infinite}
.s1{left:9%;top:21%}.s2{left:82%;top:16%;animation-delay:.7s}.s3{left:75%;top:55%;animation-delay:1.4s}.s4{left:16%;top:64%;animation-delay:2.1s}
.header{padding:20px 20px 7px;text-align:center}
.eyebrow{color:var(--gold);font-size:10px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
h2{margin:7px 0 3px;color:var(--gold2);font-family:'Noto Sans Devanagari','Cormorant Garamond',serif;font-size:30px;line-height:1.05;text-shadow:0 0 28px rgba(244,196,93,.17)}
.sub{margin:0;color:var(--muted);font-size:12px;line-height:1.5}
.avatar-button{position:relative;display:block;width:100%;height:270px;padding:0;border:0;background:transparent;cursor:pointer}
.aura{position:absolute;left:50%;top:48%;width:235px;height:235px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,226,161,.34),rgba(244,196,93,.10) 48%,transparent 69%);filter:blur(2px);animation:aura 4.4s ease-in-out infinite}
.ring,.ring2{position:absolute;left:50%;top:48%;width:216px;height:216px;transform:translate(-50%,-50%);border:1px solid rgba(244,196,93,.44);border-radius:50%;box-shadow:0 0 30px rgba(244,196,93,.12)}
.ring::before{content:"✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧";position:absolute;inset:-16px;color:rgba(255,226,161,.6);font-size:9px;letter-spacing:10px;animation:spin 18s linear infinite}
.ring2{width:248px;height:248px;border-style:dashed;border-color:rgba(244,196,93,.18);animation:spinReverse 28s linear infinite}
.avatar{position:absolute;left:50%;top:49%;width:270px;height:270px;transform:translate(-50%,-50%);object-fit:contain;object-position:50% 50%;border-radius:22px;mask-image:linear-gradient(to bottom,transparent 0%,#000 5%,#000 93%,transparent 100%),linear-gradient(to right,transparent 0%,#000 5%,#000 95%,transparent 100%);mask-composite:intersect;filter:drop-shadow(0 18px 28px rgba(0,0,0,.48)) saturate(1.08);transition:transform .35s ease,filter .35s ease;animation:float 6.2s ease-in-out infinite}
.avatar-icon{position:absolute;right:21px;bottom:26px;width:62px;height:62px;border:3px solid var(--gold2);border-radius:50%;object-fit:cover;box-shadow:0 0 0 7px rgba(244,196,93,.08),0 0 30px rgba(244,196,93,.3)}
.tap{position:absolute;left:50%;bottom:9px;transform:translateX(-50%);min-width:205px;padding:10px 16px;border:1px solid rgba(244,196,93,.55);border-radius:999px;color:#1a1223;background:linear-gradient(135deg,var(--gold2),var(--gold));font-size:13px;font-weight:800;box-shadow:0 10px 30px rgba(244,196,93,.18)}
.console.speaking .avatar{animation:speaking 1.75s ease-in-out infinite;filter:drop-shadow(0 18px 32px rgba(0,0,0,.5)) drop-shadow(0 0 22px rgba(244,196,93,.35)) saturate(1.16)}
.console.speaking .aura{animation:auraFast 1.45s ease-in-out infinite}
.console.speaking .tap{background:linear-gradient(135deg,#ffe9b7,#ffbe4f)}
.preview{margin:0 16px 10px;padding:10px 13px;border:1px solid rgba(244,196,93,.16);border-radius:14px;color:#ddd6e4;background:rgba(3,9,28,.52);font-family:'Noto Sans Devanagari',Inter,sans-serif;font-size:11px;line-height:1.55;max-height:58px;overflow:hidden}
.status{display:flex;align-items:center;justify-content:center;gap:7px;color:#d7cedd;font-size:11px}.orb{width:7px;height:7px;border-radius:50%;background:#7ee5a8;box-shadow:0 0 13px rgba(126,229,168,.72)}
.console.speaking .orb{background:var(--gold2);box-shadow:0 0 14px var(--gold)}
.wave{height:27px;margin:5px 20px 6px;display:flex;align-items:center;justify-content:center;gap:3px}
.wave i{display:block;width:3px;height:5px;border-radius:5px;background:linear-gradient(var(--gold2),var(--gold));opacity:.55}
.console.speaking .wave i{animation:wave .85s ease-in-out infinite}.wave i:nth-child(2n){animation-delay:.1s}.wave i:nth-child(3n){animation-delay:.22s}.wave i:nth-child(5n){animation-delay:.35s}
.controls{display:grid;grid-template-columns:1.25fr 1fr 1fr .85fr;gap:7px;padding:0 16px}
.control,.rate{height:34px;border:1px solid rgba(244,196,93,.22);border-radius:10px;color:var(--cream);background:rgba(255,255,255,.045);cursor:pointer;font-size:11px;font-weight:700}.control:hover,.rate:hover{border-color:rgba(244,196,93,.58);color:var(--gold2)}.control.primary{color:#181021;background:linear-gradient(135deg,var(--gold2),var(--gold));border-color:transparent}.rate{padding:0 6px}
.note{text-align:center;margin:7px 12px 0;color:#817b93;font-size:9px;line-height:1.35}
@keyframes cosmos{to{transform:rotate(360deg)}}
@keyframes twinkle{0%,100%{opacity:.25;transform:scale(.7)}50%{opacity:1;transform:scale(1.5)}}
@keyframes aura{0%,100%{transform:translate(-50%,-50%) scale(.93);opacity:.65}50%{transform:translate(-50%,-50%) scale(1.08);opacity:1}}
@keyframes auraFast{0%,100%{transform:translate(-50%,-50%) scale(.95);opacity:.65}50%{transform:translate(-50%,-50%) scale(1.13);opacity:1}}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes spinReverse{to{transform:translate(-50%,-50%) rotate(-360deg)}}
@keyframes float{0%,100%{transform:translate(-50%,-50%) translateY(0)}50%{transform:translate(-50%,-50%) translateY(-7px)}}
@keyframes speaking{0%,100%{transform:translate(-50%,-50%) scale(1) translateY(0)}50%{transform:translate(-50%,-50%) scale(1.018) translateY(-5px)}}
@keyframes wave{0%,100%{height:5px;opacity:.45}50%{height:24px;opacity:1}}
@media(max-width:420px){.console{height:520px}.header{padding-left:10px;padding-right:10px}h2{font-size:26px}.avatar-button{height:270px}.avatar{width:240px;height:260px}.controls{grid-template-columns:1.2fr 1fr 1fr}.rate{grid-column:1/-1}.preview{font-size:10px}}
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
</style>
</head>
<body>
<section class="console" id="console">
  <i class="spark s1"></i><i class="spark s2"></i><i class="spark s3"></i><i class="spark s4"></i>
  <header class="header">
    <div class="eyebrow">__CONTEXT_HTML__</div>
    <h2>श्री कृष्ण की वाणी सुनें</h2>
    <p class="sub">Tap Shri Krishna to hear the Hindi explanation</p>
  </header>
  <button class="avatar-button" id="avatarButton" type="button" aria-label="श्रीकृष्ण की हिन्दी वाणी सुनें">
    <span class="aura"></span><span class="ring"></span><span class="ring2"></span>
    <img class="avatar" src="__IMAGE_URI__" alt="शंख, चक्र, गदा, पद्म और शेषनाग सहित श्रीकृष्ण का कलात्मक स्वरूप" />
    <img class="avatar-icon" src="__ICON_URI__" alt="श्रीकृष्ण" />
    <span class="tap" id="tapLabel">🎧 मैं सुनना चाहता हूँ</span>
  </button>
  <div class="preview">__PREVIEW_HTML__</div>
  <div class="status"><span class="orb"></span><span id="statusText">हिन्दी आवाज़ तैयार है</span></div>
  <div class="wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="controls">
    <button class="control primary" id="mainControl" type="button">▶ सुनें</button>
    <button class="control" id="replayButton" type="button">↻ फिर</button>
    <button class="control" id="stopButton" type="button">■ रोकें</button>
    <select class="rate" id="rateSelect" aria-label="वाणी गति"><option value="0.78">शांत</option><option value="0.9" selected>1×</option><option value="1.04">तेज़</option></select>
  </div>
  <div class="note">AI-generated educational narration · Chrome/Edge में उपलब्ध Hindi system voice का उपयोग</div>
</section>
<script>
(() => {
  const text = __SPEECH_JSON__;
  const instanceId = __INSTANCE_JSON__;
  const root = document.getElementById('console');
  const avatarButton = document.getElementById('avatarButton');
  const mainControl = document.getElementById('mainControl');
  const replayButton = document.getElementById('replayButton');
  const stopButton = document.getElementById('stopButton');
  const rateSelect = document.getElementById('rateSelect');
  const statusText = document.getElementById('statusText');
  const tapLabel = document.getElementById('tapLabel');
  let state = 'idle', token = 0, chunks = [], index = 0;

  const setState = (next, label) => {
    state = next; root.classList.toggle('speaking', next === 'speaking'); statusText.textContent = label;
    mainControl.textContent = next === 'speaking' ? '⏸ विराम' : next === 'paused' ? '▶ आगे' : '▶ सुनें';
    tapLabel.textContent = next === 'speaking' ? '✨ श्रीकृष्ण वाणी चल रही है' : '🎧 मैं सुनना चाहता हूँ';
  };
  const voices = () => window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
  const chooseVoice = () => voices().find(v => v.lang.toLowerCase() === 'hi-in') || voices().find(v => v.lang.toLowerCase().startsWith('hi')) || voices().find(v => v.lang.toLowerCase() === 'en-in') || null;
  const split = (value) => {
    const parts = value.match(/[^।.!?]+[।.!?]?/g) || [value]; const out=[]; let current='';
    for(const raw of parts){const part=raw.trim();if(!part)continue;if((current+' '+part).trim().length>210&&current){out.push(current.trim());current=part}else current=(current+' '+part).trim()}
    if(current)out.push(current);return out.length?out:[value];
  };
  const chime = () => {try{const C=window.AudioContext||window.webkitAudioContext;if(!C)return;const c=new C(),g=c.createGain();g.gain.setValueAtTime(.0001,c.currentTime);g.gain.exponentialRampToValueAtTime(.04,c.currentTime+.03);g.gain.exponentialRampToValueAtTime(.0001,c.currentTime+.65);g.connect(c.destination);[432,648].forEach((f,i)=>{const o=c.createOscillator();o.type='sine';o.frequency.value=f;o.connect(g);o.start(c.currentTime+i*.04);o.stop(c.currentTime+.7)});setTimeout(()=>c.close(),850)}catch(_){}};
  const speakNext = active => {
    if(active!==token||index>=chunks.length){if(active===token)setState('ended','हिन्दी व्याख्या पूर्ण हुई');return}
    const u=new SpeechSynthesisUtterance(chunks[index]);u.lang='hi-IN';u.rate=Number(rateSelect.value||.9);u.pitch=.84;u.volume=1;const v=chooseVoice();if(v)u.voice=v;
    u.onend=()=>{if(active===token){index+=1;speakNext(active)}};u.onerror=e=>{if(!['interrupted','canceled'].includes(e.error))setState('error','ब्राउज़र आवाज़ आरम्भ नहीं कर सका')};window.speechSynthesis.speak(u);
  };
  const start = () => {if(!('speechSynthesis'in window)){setState('error','इस ब्राउज़र में हिन्दी आवाज़ उपलब्ध नहीं है');return}token+=1;window.speechSynthesis.cancel();chunks=split(text);index=0;setState('speaking','श्रीकृष्ण वाणी चल रही है…');chime();speakNext(token)};
  const stop = (label='वाणी रोक दी गई') => {token+=1;if('speechSynthesis'in window)window.speechSynthesis.cancel();setState('stopped',label)};
  avatarButton.addEventListener('click',start);
  mainControl.addEventListener('click',()=>{if(!('speechSynthesis'in window))return;if(state==='speaking'){window.speechSynthesis.pause();setState('paused','वाणी विराम पर है')}else if(state==='paused'){window.speechSynthesis.resume();setState('speaking','श्रीकृष्ण वाणी चल रही है…')}else start()});
  replayButton.addEventListener('click',start);stopButton.addEventListener('click',()=>stop());rateSelect.addEventListener('change',()=>{if(state==='speaking'||state==='paused')start()});
  if('speechSynthesis'in window)window.speechSynthesis.onvoiceschanged=chooseVoice;window.addEventListener('beforeunload',()=>stop(''));void instanceId;
})();
</script>
</body>
</html>
"""
