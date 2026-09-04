"""Premium divine visual system for the Streamlit application.

The theme is intentionally CSS-only: it remains lightweight, deployable, and does not
require remote image assets. Google Fonts are optional; sensible local fallbacks are used.
"""

APP_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

:root {
    --night-950: #080711;
    --night-900: #0d0a19;
    --night-850: #121022;
    --night-800: #18142b;
    --saffron: #f4a742;
    --gold: #f5cf72;
    --gold-bright: #ffe6a6;
    --gold-deep: #a96e18;
    --lotus: #ef9faf;
    --violet: #9e83ff;
    --cream: #fff7e8;
    --muted: #c9bfd5;
    --glass: rgba(18, 14, 35, 0.72);
    --glass-strong: rgba(13, 10, 26, 0.9);
    --gold-line: rgba(245, 207, 114, 0.25);
    --soft-line: rgba(255, 255, 255, 0.08);
    --shadow: 0 24px 80px rgba(0, 0, 0, 0.46);
}

html { scroll-behavior: smooth; }

.stApp {
    color: var(--cream);
    background:
        radial-gradient(circle at 12% 8%, rgba(156, 93, 255, 0.19), transparent 30%),
        radial-gradient(circle at 88% 14%, rgba(244, 167, 66, 0.16), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(114, 51, 147, 0.16), transparent 36%),
        linear-gradient(145deg, var(--night-950) 0%, var(--night-900) 45%, #100b1c 100%);
    min-height: 100vh;
    overflow-x: hidden;
}

/* Sacred-geometry texture and warm atmospheric glow. */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.38;
    background-image:
        radial-gradient(circle at center, transparent 0 43px, rgba(245, 207, 114, 0.055) 44px 45px, transparent 46px),
        radial-gradient(circle at center, transparent 0 86px, rgba(158, 131, 255, 0.04) 87px 88px, transparent 89px);
    background-size: 180px 180px;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,.8), transparent 86%);
    animation: sacredDrift 34s linear infinite;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 42rem;
    height: 42rem;
    left: 50%;
    top: -28rem;
    transform: translateX(-50%);
    border-radius: 999px;
    pointer-events: none;
    background: rgba(245, 207, 114, 0.12);
    filter: blur(110px);
    z-index: 0;
    animation: auraPulse 8s ease-in-out infinite;
}

@keyframes sacredDrift {
    from { background-position: 0 0; }
    to { background-position: 180px 180px; }
}

@keyframes auraPulse {
    0%, 100% { opacity: .52; transform: translateX(-50%) scale(.92); }
    50% { opacity: .9; transform: translateX(-50%) scale(1.08); }
}

@keyframes sealFloat {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-7px) rotate(1deg); }
}

@keyframes shimmer {
    0% { transform: translateX(-130%) skewX(-18deg); }
    55%, 100% { transform: translateX(240%) skewX(-18deg); }
}

[data-testid="stAppViewContainer"] > .main,
[data-testid="stSidebar"],
[data-testid="stHeader"] {
    position: relative;
    z-index: 1;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

#MainMenu,
[data-testid="stFooter"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0;
}

.block-container {
    max-width: 1080px;
    padding-top: 1.1rem;
    padding-bottom: 5.5rem;
}

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: "Inter", "Noto Sans Devanagari", system-ui, sans-serif;
}

h1, h2, h3, h4 {
    font-family: "Cormorant Garamond", "Noto Sans Devanagari", Georgia, serif;
    color: var(--cream);
    letter-spacing: -0.02em;
}

p, li, label, [data-testid="stMarkdownContainer"] {
    color: #eee7f2;
}

/* ── Hero ─────────────────────────────────────────────────────────────── */
.divine-hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    text-align: center;
    padding: 2.7rem 2rem 2.25rem;
    margin: .5rem 0 1rem;
    border: 1px solid var(--gold-line);
    border-radius: 28px;
    background:
        radial-gradient(circle at 50% 0%, rgba(245, 207, 114, 0.16), transparent 43%),
        linear-gradient(145deg, rgba(31, 23, 54, 0.82), rgba(12, 9, 26, 0.9));
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,.09);
    backdrop-filter: blur(18px) saturate(135%);
}

.divine-hero::before,
.divine-hero::after {
    content: "";
    position: absolute;
    z-index: -1;
    border: 1px solid rgba(245, 207, 114, 0.13);
    border-radius: 999px;
    left: 50%;
    transform: translateX(-50%);
}

.divine-hero::before {
    width: 26rem;
    height: 26rem;
    top: -18rem;
    box-shadow: 0 0 0 38px rgba(245,207,114,.025), 0 0 0 76px rgba(245,207,114,.018);
}

.divine-hero::after {
    width: 44rem;
    height: 44rem;
    bottom: -41rem;
}

.hero-shimmer {
    position: absolute;
    inset: 0 auto 0 -15%;
    width: 22%;
    z-index: -1;
    pointer-events: none;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.08), transparent);
    animation: shimmer 9s ease-in-out infinite;
}

.om-seal {
    position: relative;
    display: grid;
    place-items: center;
    width: 88px;
    height: 88px;
    margin: 0 auto 1.15rem;
    color: var(--gold-bright);
    font-family: "Noto Sans Devanagari", serif;
    font-size: 3.15rem;
    line-height: 1;
    border: 1px solid rgba(245, 207, 114, .54);
    border-radius: 50%;
    background:
        radial-gradient(circle, rgba(245,207,114,.18), rgba(169,110,24,.06) 58%, transparent 60%),
        rgba(8, 7, 17, .64);
    box-shadow:
        0 0 0 8px rgba(245,207,114,.045),
        0 0 0 15px rgba(245,207,114,.025),
        0 0 42px rgba(245,207,114,.24),
        inset 0 0 24px rgba(245,207,114,.10);
    animation: sealFloat 6s ease-in-out infinite;
}

.om-seal::before,
.om-seal::after {
    content: "✦";
    position: absolute;
    top: 50%;
    color: rgba(245,207,114,.75);
    font-size: .62rem;
}
.om-seal::before { left: -25px; }
.om-seal::after { right: -25px; }

.hero-kicker {
    margin-bottom: .5rem;
    color: var(--gold);
    font-size: .73rem;
    font-weight: 700;
    letter-spacing: .22em;
    text-transform: uppercase;
}

.divine-hero h1 {
    margin: 0;
    font-size: clamp(2.55rem, 7vw, 4.45rem);
    font-weight: 700;
    line-height: .97;
    text-shadow: 0 8px 30px rgba(0,0,0,.34);
}

.divine-hero h1 .ai-mark {
    color: transparent;
    background: linear-gradient(120deg, var(--gold-bright), var(--saffron));
    -webkit-background-clip: text;
    background-clip: text;
}

.hero-subtitle {
    max-width: 690px;
    margin: 1rem auto 1.2rem;
    color: #dcd3e4;
    font-size: 1.02rem;
    line-height: 1.75;
}

.hero-badges {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: .55rem;
}

.hero-badge,
.mode-pill {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .45rem .72rem;
    border: 1px solid rgba(245,207,114,.16);
    border-radius: 999px;
    color: #e9dfed;
    background: rgba(255,255,255,.045);
    font-size: .77rem;
    font-weight: 600;
    letter-spacing: .02em;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #79e2a6;
    box-shadow: 0 0 12px rgba(121,226,166,.65);
}

.verse-ribbon {
    position: relative;
    margin: .9rem 0 1.25rem;
    padding: 1.05rem 1.2rem;
    text-align: center;
    border-top: 1px solid rgba(245,207,114,.18);
    border-bottom: 1px solid rgba(245,207,114,.18);
    background: linear-gradient(90deg, transparent, rgba(245,207,114,.045), transparent);
}

.verse-ribbon .verse {
    display: block;
    color: var(--gold-bright);
    font-family: "Noto Sans Devanagari", "Cormorant Garamond", serif;
    font-size: 1.08rem;
    font-weight: 500;
    line-height: 1.65;
}

.verse-ribbon .reference {
    display: block;
    margin-top: .25rem;
    color: #a99db4;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .16em;
    text-transform: uppercase;
}

/* ── Status cards ─────────────────────────────────────────────────────── */
.sacred-stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .75rem;
    margin: .25rem 0 1.2rem;
}

.sacred-stat {
    min-height: 96px;
    padding: .95rem 1rem;
    border: 1px solid rgba(245,207,114,.14);
    border-radius: 17px;
    background: linear-gradient(145deg, rgba(255,255,255,.052), rgba(255,255,255,.024));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.055), 0 12px 36px rgba(0,0,0,.15);
}

.stat-icon {
    display: block;
    margin-bottom: .35rem;
    font-size: 1.05rem;
}

.stat-label {
    display: block;
    color: #a99fb2;
    font-size: .67rem;
    font-weight: 700;
    letter-spacing: .13em;
    text-transform: uppercase;
}

.stat-value {
    display: block;
    margin-top: .18rem;
    color: var(--cream);
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 1.12rem;
    font-weight: 700;
    line-height: 1.1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Welcome and quick prompts ───────────────────────────────────────── */
.welcome-sanctum {
    margin: .7rem 0 1rem;
    padding: 1.4rem 1.5rem;
    border: 1px solid rgba(245,207,114,.16);
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(25,19,45,.72), rgba(13,10,27,.72));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
}

.welcome-sanctum h3 {
    margin: 0 0 .3rem;
    color: var(--gold-bright);
    font-size: 1.55rem;
}

.welcome-sanctum p {
    margin: 0;
    color: #cfc5d6;
    line-height: 1.65;
}

.section-eyebrow {
    margin: 1.35rem 0 .55rem;
    color: var(--gold);
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .16em;
    text-transform: uppercase;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 50% 0%, rgba(245,207,114,.10), transparent 30%),
        linear-gradient(180deg, rgba(15,11,29,.985), rgba(8,7,17,.99));
    border-right: 1px solid rgba(245,207,114,.18);
    box-shadow: 16px 0 60px rgba(0,0,0,.25);
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding-top: 1.15rem;
}

.sidebar-brand {
    padding: .85rem .25rem 1.15rem;
    text-align: center;
}

.sidebar-mini-seal {
    display: grid;
    place-items: center;
    width: 52px;
    height: 52px;
    margin: 0 auto .7rem;
    border: 1px solid rgba(245,207,114,.42);
    border-radius: 50%;
    color: var(--gold-bright);
    background: rgba(245,207,114,.06);
    box-shadow: 0 0 28px rgba(245,207,114,.12);
    font-family: "Noto Sans Devanagari", serif;
    font-size: 1.85rem;
}

.sidebar-brand strong {
    display: block;
    color: var(--cream);
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 1.42rem;
}

.sidebar-brand span {
    display: block;
    margin-top: .15rem;
    color: #a99eb3;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .15em;
    text-transform: uppercase;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(245,207,114,.13);
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #e6dce9 !important;
    font-size: .83rem;
    font-weight: 600;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: .2rem;
    padding: .25rem;
    border: 1px solid rgba(245,207,114,.10);
    border-radius: 13px;
    background: rgba(255,255,255,.025);
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: .42rem .48rem;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] input {
    border-color: rgba(245,207,114,.20) !important;
    background: rgba(255,255,255,.045) !important;
    color: var(--cream) !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] {
    border: 1px solid rgba(112,224,158,.17);
    border-radius: 12px;
    background: rgba(75,181,119,.08);
}

.privacy-note {
    margin: 1rem 0 .4rem;
    padding: .8rem .85rem;
    border: 1px solid rgba(245,207,114,.11);
    border-radius: 13px;
    color: #aaa0b3;
    background: rgba(255,255,255,.025);
    font-size: .73rem;
    line-height: 1.55;
}

/* ── Streamlit controls ───────────────────────────────────────────────── */
.stButton > button,
.stFormSubmitButton > button {
    min-height: 2.75rem;
    border: 1px solid rgba(245,207,114,.28) !important;
    border-radius: 13px !important;
    color: #fff8e9 !important;
    background:
        linear-gradient(145deg, rgba(245,207,114,.12), rgba(244,167,66,.07)) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 8px 24px rgba(0,0,0,.14);
    font-weight: 600 !important;
    transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    border-color: rgba(245,207,114,.60) !important;
    color: var(--gold-bright) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,.22), 0 0 22px rgba(245,207,114,.08);
}

.stButton > button:active { transform: translateY(0); }

[data-testid="stSlider"] [role="slider"] {
    background: var(--gold) !important;
    border-color: var(--gold-bright) !important;
    box-shadow: 0 0 13px rgba(245,207,114,.28);
}

[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #978d9e;
}

/* ── Expanders ────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    overflow: hidden;
    border: 1px solid rgba(245,207,114,.14) !important;
    border-radius: 15px !important;
    background: rgba(255,255,255,.027) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
}

[data-testid="stExpander"] summary {
    color: #e9dfed !important;
    font-weight: 600;
}

/* ── Chat ─────────────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    margin: .78rem 0;
    padding: 1rem 1.05rem;
    border: 1px solid rgba(245,207,114,.12);
    border-radius: 19px;
    background:
        linear-gradient(145deg, rgba(255,255,255,.050), rgba(255,255,255,.024));
    box-shadow: 0 13px 38px rgba(0,0,0,.17), inset 0 1px 0 rgba(255,255,255,.045);
    backdrop-filter: blur(12px);
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    font-size: .98rem;
    line-height: 1.72;
}

[data-testid="stChatMessage"] h3 {
    margin-top: .7rem;
    margin-bottom: .2rem;
    color: var(--gold-bright);
    font-size: 1.45rem;
}

[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    border: 1px solid rgba(245,207,114,.25);
    background: rgba(245,207,114,.08);
    box-shadow: 0 0 20px rgba(245,207,114,.08);
}

[data-testid="stChatInput"] {
    border: 1px solid rgba(245,207,114,.24) !important;
    border-radius: 18px !important;
    background: rgba(14,11,27,.93) !important;
    box-shadow: 0 18px 54px rgba(0,0,0,.37), 0 0 0 1px rgba(255,255,255,.025);
    backdrop-filter: blur(18px);
}

[data-testid="stChatInput"] textarea {
    color: var(--cream) !important;
    caret-color: var(--gold);
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #93889c !important;
}

[data-testid="stChatInput"] button {
    color: var(--gold-bright) !important;
}

[data-testid="stBottomBlockContainer"] {
    background: linear-gradient(to top, var(--night-950) 42%, transparent) !important;
}

/* ── Retrieval evidence ───────────────────────────────────────────────── */
.source-card {
    margin: .6rem 0 .8rem;
    padding: .95rem 1rem;
    border: 1px solid rgba(245,207,114,.13);
    border-radius: 14px;
    background: rgba(7,6,15,.34);
}

.source-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: .55rem;
}

.source-reference {
    color: var(--gold-bright);
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 1.02rem;
    font-weight: 700;
}

.source-score {
    flex: 0 0 auto;
    padding: .22rem .48rem;
    border: 1px solid rgba(158,131,255,.24);
    border-radius: 999px;
    color: #c9bcff;
    background: rgba(158,131,255,.08);
    font-size: .66rem;
    font-weight: 700;
    letter-spacing: .06em;
}

.score-track {
    height: 3px;
    margin-bottom: .65rem;
    overflow: hidden;
    border-radius: 999px;
    background: rgba(255,255,255,.06);
}

.score-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--violet), var(--gold));
    box-shadow: 0 0 10px rgba(245,207,114,.22);
}

.source-text {
    color: #cfc6d5;
    font-family: "Noto Sans Devanagari", "Inter", sans-serif;
    font-size: .82rem;
    line-height: 1.65;
}

/* ── Status, alerts, footer ───────────────────────────────────────────── */
[data-testid="stStatusWidget"],
[data-testid="stSpinner"] {
    color: var(--gold-bright);
}

[data-testid="stAlert"] {
    border-radius: 14px;
}

.app-footer {
    margin-top: 2.4rem;
    padding: 1rem 0;
    text-align: center;
    color: #7f7488;
    font-size: .71rem;
    letter-spacing: .04em;
}

.app-footer .lotus-divider {
    display: block;
    margin-bottom: .45rem;
    color: rgba(245,207,114,.72);
    letter-spacing: .45em;
}

/* Mobile refinement. */
@media (max-width: 760px) {
    .block-container { padding: .65rem .75rem 5rem; }
    .divine-hero { padding: 2.15rem 1.1rem 1.8rem; border-radius: 22px; }
    .divine-hero h1 { font-size: 2.65rem; }
    .hero-subtitle { font-size: .91rem; }
    .sacred-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .stat-value { font-size: 1rem; }
    [data-testid="stChatMessage"] { padding: .82rem .8rem; border-radius: 16px; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
    }
}


/* ── Krishna Vāṇī edition overrides ─────────────────────────────────── */
.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(255, 196, 76, .18), transparent 30%),
        radial-gradient(circle at 8% 24%, rgba(28, 70, 180, .24), transparent 34%),
        radial-gradient(circle at 94% 18%, rgba(104, 53, 189, .22), transparent 31%),
        linear-gradient(152deg, #030817 0%, #07132f 46%, #16082e 100%);
}

.block-container { max-width: 1160px; }

/* ── Cinematic temple hero ──────────────────────────────────────────── */
.temple-hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    min-height: 455px;
    margin: .45rem 0 1rem;
    padding: 1rem 2rem 1.55rem;
    border: 1px solid rgba(248, 203, 101, .32);
    border-radius: 30px;
    background:
        linear-gradient(to bottom, rgba(4, 11, 31, .23), rgba(5, 10, 28, .91)),
        radial-gradient(circle at 50% 13%, rgba(255, 210, 107, .22), transparent 28%),
        linear-gradient(125deg, rgba(12, 36, 91, .88), rgba(43, 16, 79, .9));
    box-shadow:
        0 28px 95px rgba(0, 0, 0, .47),
        0 0 70px rgba(244, 200, 98, .07),
        inset 0 1px 0 rgba(255, 255, 255, .1);
    backdrop-filter: blur(18px) saturate(135%);
}

.temple-hero::before,
.temple-hero::after {
    content: "";
    position: absolute;
    pointer-events: none;
    z-index: -1;
}

.temple-hero::before {
    width: 570px;
    height: 570px;
    left: 50%;
    top: -380px;
    transform: translateX(-50%);
    border: 1px solid rgba(248, 203, 101, .18);
    border-radius: 50%;
    box-shadow:
        0 0 0 45px rgba(248, 203, 101, .028),
        0 0 0 92px rgba(248, 203, 101, .017),
        0 0 0 140px rgba(112, 94, 236, .014);
}

.temple-hero::after {
    inset: auto 0 0;
    height: 180px;
    opacity: .46;
    background:
        linear-gradient(135deg, transparent 48%, rgba(248, 203, 101, .06) 49% 51%, transparent 52%) 0 0/48px 48px,
        linear-gradient(45deg, transparent 48%, rgba(248, 203, 101, .04) 49% 51%, transparent 52%) 0 0/48px 48px;
    mask-image: linear-gradient(to top, black, transparent);
}

.hero-stars {
    position: absolute;
    inset: 0;
    z-index: -2;
    opacity: .6;
    background-image:
        radial-gradient(circle, rgba(255, 225, 162, .85) 0 1px, transparent 1.5px),
        radial-gradient(circle, rgba(164, 181, 255, .55) 0 1px, transparent 1.5px);
    background-size: 95px 95px, 137px 137px;
    background-position: 14px 9px, 62px 41px;
    animation: sacredDrift 54s linear infinite;
}

.hero-arch {
    position: absolute;
    width: 610px;
    height: 610px;
    left: 50%;
    top: 70px;
    z-index: -1;
    transform: translateX(-50%);
    border: 1px solid rgba(248, 203, 101, .13);
    border-radius: 310px 310px 0 0;
}

.hero-topline {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: .55rem;
    min-height: 36px;
    color: #cfc8db;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .13em;
    text-transform: uppercase;
}

.living-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #79e2a6;
    box-shadow: 0 0 15px rgba(121, 226, 166, .8);
    animation: livingPulse 1.9s ease-in-out infinite;
}

.topline-divider { color: var(--gold); }

.hero-center {
    position: relative;
    z-index: 2;
    max-width: 820px;
    margin: 1.3rem auto 0;
    text-align: center;
}

.om-mandala {
    position: relative;
    display: grid;
    place-items: center;
    width: 92px;
    height: 92px;
    margin: 0 auto 1rem;
    border: 1px solid rgba(255, 221, 160, .65);
    border-radius: 50%;
    background:
        radial-gradient(circle, rgba(255, 221, 160, .22), rgba(244, 154, 61, .06) 53%, transparent 55%),
        rgba(4, 10, 29, .62);
    box-shadow:
        0 0 0 8px rgba(244, 200, 98, .05),
        0 0 0 17px rgba(244, 200, 98, .025),
        0 0 45px rgba(255, 205, 91, .31),
        inset 0 0 24px rgba(255, 221, 160, .13);
    animation: sealFloat 6s ease-in-out infinite;
}

.om-mandala::before,
.om-mandala::after {
    content: "✦";
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 221, 160, .78);
    font-size: .7rem;
}
.om-mandala::before { left: -30px; }
.om-mandala::after { right: -30px; }
.om-mandala span {
    color: var(--gold-bright);
    font-family: "Noto Sans Devanagari", serif;
    font-size: 3.25rem;
    line-height: 1;
}

.hero-kicker {
    color: var(--gold);
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .21em;
    text-transform: uppercase;
}

.hero-center h1 {
    margin: .45rem 0 .8rem;
    font-size: clamp(3rem, 7vw, 5.35rem);
    line-height: .92;
    font-weight: 700;
    text-shadow: 0 10px 42px rgba(0, 0, 0, .46);
}

.hero-center h1 span {
    color: transparent;
    background: linear-gradient(115deg, #fff0bd 0%, #f4c862 46%, #f39a3d 100%);
    -webkit-background-clip: text;
    background-clip: text;
}

.hero-center > p {
    max-width: 760px;
    margin: 0 auto;
    color: #ddd7e6;
    font-size: 1.02rem;
    line-height: 1.75;
}

.hero-actions {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: .55rem;
    margin-top: 1.15rem;
}

.hero-actions span {
    padding: .48rem .75rem;
    border: 1px solid rgba(244, 200, 98, .18);
    border-radius: 999px;
    color: #eee8f2;
    background: rgba(255, 255, 255, .045);
    font-size: .75rem;
    font-weight: 600;
}

.hero-mantra {
    position: absolute;
    left: 2rem;
    right: 2rem;
    bottom: 1.25rem;
    z-index: 3;
    text-align: center;
}

.hero-mantra span {
    display: block;
    color: var(--gold-bright);
    font-family: "Noto Sans Devanagari", serif;
    font-size: 1rem;
}
.hero-mantra small {
    display: block;
    margin-top: .22rem;
    color: #9f96aa;
    font-size: .66rem;
    font-weight: 700;
    letter-spacing: .13em;
    text-transform: uppercase;
}

@keyframes livingPulse {
    0%, 100% { transform: scale(.8); opacity: .65; }
    50% { transform: scale(1.15); opacity: 1; }
}

/* ── Five configuration cards ───────────────────────────────────────── */
.sacred-stats {
    grid-template-columns: repeat(5, minmax(0, 1fr));
    margin-top: .85rem;
}
.sacred-stat:nth-child(2) {
    border-color: rgba(120, 226, 167, .18);
    background: linear-gradient(145deg, rgba(69, 178, 119, .075), rgba(255,255,255,.022));
}

/* ── Voice section introduction ─────────────────────────────────────── */
.voice-section-heading {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.45rem 0 .72rem;
    padding: 1rem 1.15rem;
    border-left: 2px solid var(--gold);
    border-radius: 0 17px 17px 0;
    background: linear-gradient(90deg, rgba(244, 200, 98, .075), transparent 76%);
}

.voice-section-icon {
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    width: 48px;
    height: 48px;
    border: 1px solid rgba(244, 200, 98, .32);
    border-radius: 15px;
    background: rgba(244, 200, 98, .075);
    box-shadow: 0 0 25px rgba(244, 200, 98, .08);
    font-size: 1.35rem;
}

.voice-section-heading .section-eyebrow { margin: 0 0 .2rem; }
.voice-section-heading h2 {
    margin: 0;
    color: var(--gold-bright);
    font-size: 1.75rem;
}
.voice-section-heading p {
    margin: .2rem 0 0;
    color: #bfb6c9;
    font-size: .82rem;
    line-height: 1.55;
}

iframe[title="streamlit_components.v1.html"] {
    width: 100%;
    border: 0;
    border-radius: 25px;
}

/* ── Welcome sanctum upgrade ────────────────────────────────────────── */
.welcome-sanctum {
    display: flex;
    align-items: center;
    gap: 1.1rem;
    padding: 1.25rem 1.35rem;
    background:
        radial-gradient(circle at 8% 50%, rgba(244, 200, 98, .09), transparent 22%),
        linear-gradient(145deg, rgba(14, 31, 72, .7), rgba(33, 13, 63, .66));
}
.welcome-symbol {
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    width: 70px;
    height: 70px;
    border: 1px solid rgba(244, 200, 98, .23);
    border-radius: 22px;
    background: rgba(244, 200, 98, .06);
    font-size: 2rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.06);
}
.welcome-sanctum .section-eyebrow { margin: 0 0 .2rem; }
.welcome-sanctum h3 { margin: 0 0 .25rem; }

/* ── Sidebar voice feature card ─────────────────────────────────────── */
.voice-side-note {
    margin: .9rem 0;
    padding: .9rem;
    border: 1px solid rgba(244, 200, 98, .18);
    border-radius: 15px;
    background:
        radial-gradient(circle at 0 0, rgba(244,200,98,.1), transparent 38%),
        rgba(255,255,255,.028);
}
.voice-side-note strong {
    display: block;
    color: var(--gold-bright);
    font-family: "Cormorant Garamond", "Noto Sans Devanagari", serif;
    font-size: 1.06rem;
}
.voice-side-note span {
    display: block;
    margin-top: .35rem;
    color: #a99fb4;
    font-size: .71rem;
    line-height: 1.52;
}

/* Stronger chat hierarchy. */
[data-testid="stChatMessage"] {
    border-color: rgba(244, 200, 98, .16);
    background:
        radial-gradient(circle at 0 0, rgba(48, 83, 183, .075), transparent 31%),
        linear-gradient(145deg, rgba(13, 27, 66, .7), rgba(28, 13, 52, .67));
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-color: rgba(89, 125, 255, .2);
    background: linear-gradient(145deg, rgba(18, 45, 115, .62), rgba(12, 24, 60, .64));
}

/* ── Footer mantra ──────────────────────────────────────────────────── */
.app-footer {
    margin-top: 3rem;
    padding: 1.1rem 1rem 1.3rem;
    border-top: 1px solid rgba(244, 200, 98, .13);
    background: linear-gradient(90deg, transparent, rgba(244, 200, 98, .035), transparent);
}
.footer-mantra {
    display: block;
    margin-bottom: .45rem;
    color: rgba(244, 200, 98, .8);
    font-family: "Noto Sans Devanagari", serif;
    font-size: .78rem;
}
.app-footer small {
    display: block;
    color: #766d80;
    font-size: .66rem;
}

@media (max-width: 920px) {
    .sacred-stats { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .temple-hero { min-height: 485px; }
}

@media (max-width: 760px) {
    .temple-hero { min-height: 535px; padding: .8rem 1rem 1.35rem; border-radius: 23px; }
    .hero-topline { font-size: .58rem; letter-spacing: .08em; }
    .hero-center { margin-top: 1rem; }
    .hero-center h1 { font-size: 3.05rem; }
    .hero-center > p { font-size: .9rem; }
    .hero-mantra { left: 1rem; right: 1rem; bottom: 1rem; }
    .hero-mantra span { font-size: .88rem; }
    .sacred-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .voice-section-heading { align-items: flex-start; }
    .voice-section-heading h2 { font-size: 1.42rem; }
    .welcome-sanctum { align-items: flex-start; }
    .welcome-symbol { width: 56px; height: 56px; border-radius: 18px; font-size: 1.55rem; }
}

</style>
"""
