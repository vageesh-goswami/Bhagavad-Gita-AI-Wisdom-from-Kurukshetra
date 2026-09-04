"""Cinematic navy-and-gold interface styling for the Streamlit dashboard."""

APP_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

:root {
    --void: #020716;
    --navy: #050d24;
    --navy-2: #081735;
    --indigo: #111d4d;
    --violet: #27124d;
    --gold: #efb94a;
    --gold-bright: #ffe19a;
    --saffron: #f28c36;
    --cream: #fff7e5;
    --soft: #d8d1df;
    --muted: #9891a8;
    --line: rgba(239, 185, 74, .25);
    --glass: rgba(6, 14, 39, .80);
    --green: #72e6a0;
}

html, body, [class*="css"] {
    font-family: Inter, "Noto Sans Devanagari", sans-serif;
}

html { scroll-behavior: smooth; }

.stApp {
    color: var(--cream);
    background:
        radial-gradient(circle at 50% -10%, rgba(61, 78, 171, .22), transparent 38%),
        radial-gradient(circle at 85% 30%, rgba(92, 35, 119, .17), transparent 33%),
        radial-gradient(circle at 14% 72%, rgba(217, 123, 38, .09), transparent 30%),
        linear-gradient(160deg, #020716 0%, #04102b 46%, #030817 100%);
    overflow-x: hidden;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: .55;
    background-image:
        radial-gradient(circle at 7% 12%, rgba(255, 226, 154, .8) 0 1px, transparent 1.8px),
        radial-gradient(circle at 19% 36%, rgba(160, 175, 255, .62) 0 1px, transparent 1.9px),
        radial-gradient(circle at 30% 8%, rgba(255, 226, 154, .72) 0 1px, transparent 1.7px),
        radial-gradient(circle at 44% 22%, rgba(255, 226, 154, .55) 0 1px, transparent 1.8px),
        radial-gradient(circle at 59% 7%, rgba(160, 175, 255, .64) 0 1px, transparent 1.8px),
        radial-gradient(circle at 71% 34%, rgba(255, 226, 154, .64) 0 1px, transparent 1.9px),
        radial-gradient(circle at 84% 12%, rgba(255, 226, 154, .76) 0 1px, transparent 1.8px),
        radial-gradient(circle at 93% 43%, rgba(143, 159, 255, .70) 0 1px, transparent 1.9px);
    background-size: 310px 260px, 420px 390px, 360px 310px, 480px 420px,
                     330px 300px, 390px 350px, 520px 460px, 450px 390px;
    animation: starDrift 55s linear infinite;
}

.stApp::after {
    content: "";
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 33vh;
    z-index: 0;
    pointer-events: none;
    opacity: .58;
    background:
        linear-gradient(180deg, transparent, rgba(3, 8, 25, .55) 45%, rgba(2, 7, 20, .95)),
        radial-gradient(ellipse at 50% 100%, rgba(20, 51, 108, .46), transparent 68%);
}

[data-testid="stHeader"] {
    background: transparent;
    height: .2rem;
}

[data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; }

[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"] {
    position: relative;
    z-index: 2;
}

.block-container {
    max-width: 1580px;
    padding: .65rem 1.05rem 5.2rem;
}

/* ── Ambient animated world ───────────────────────────────────────────── */
.ambient-world {
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    overflow: hidden;
}

.ambient-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(45px);
    opacity: .22;
    animation: orbWander 17s ease-in-out infinite alternate;
}
.orb-one { width: 330px; height: 330px; left: 8%; top: 12%; background: #694dc0; }
.orb-two { width: 390px; height: 390px; right: 6%; top: 24%; background: #b46a26; animation-delay: -6s; }
.orb-three { width: 280px; height: 280px; left: 46%; bottom: -6%; background: #164b98; animation-delay: -11s; }

.falling-petal {
    position: absolute;
    top: -8vh;
    color: #f9a2bd;
    font-size: 22px;
    opacity: .66;
    filter: drop-shadow(0 0 9px rgba(255, 142, 176, .42));
    animation: petalFall 17s linear infinite;
}
.petal-one { left: 7%; animation-delay: -3s; animation-duration: 18s; }
.petal-two { left: 23%; animation-delay: -11s; animation-duration: 22s; font-size: 15px; }
.petal-three { left: 47%; animation-delay: -7s; animation-duration: 19s; }
.petal-four { left: 67%; animation-delay: -15s; animation-duration: 24s; font-size: 18px; }
.petal-five { left: 83%; animation-delay: -5s; animation-duration: 20s; }
.petal-six { left: 94%; animation-delay: -12s; animation-duration: 23s; font-size: 14px; }

.firefly {
    position: absolute;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--gold-bright);
    box-shadow: 0 0 13px var(--gold);
    animation: firefly 8s ease-in-out infinite;
}
.fly-one { left: 18%; top: 20%; }
.fly-two { left: 57%; top: 17%; animation-delay: -2s; }
.fly-three { left: 77%; top: 65%; animation-delay: -4s; }
.fly-four { left: 35%; top: 76%; animation-delay: -6s; }

/* ── Top navigation ───────────────────────────────────────────────────── */
.temple-nav {
    position: sticky;
    top: .55rem;
    z-index: 20;
    min-height: 58px;
    margin: .1rem 0 .75rem;
    padding: .48rem .72rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: .18rem;
    border: 1px solid rgba(239, 185, 74, .24);
    border-radius: 18px;
    background: linear-gradient(100deg, rgba(5, 13, 36, .65), rgba(6, 14, 39, .93));
    box-shadow: 0 14px 45px rgba(0, 0, 0, .29), inset 0 1px 0 rgba(255,255,255,.05);
    backdrop-filter: blur(18px);
}

.temple-nav a {
    min-height: 42px;
    padding: .68rem .9rem;
    display: inline-flex;
    align-items: center;
    gap: .48rem;
    color: #c8c1d1 !important;
    border-radius: 11px;
    text-decoration: none !important;
    font-size: .78rem;
    font-weight: 700;
    transition: color .2s ease, background .2s ease, transform .2s ease;
}
.temple-nav a:hover,
.temple-nav a.active {
    color: var(--gold-bright) !important;
    background: rgba(239, 185, 74, .075);
    transform: translateY(-1px);
}
.temple-nav a.active { box-shadow: inset 0 -2px 0 var(--gold); }
.nav-spacer { flex: 1; order: -1; }
.nav-sun, .nav-om {
    width: 41px;
    height: 41px;
    display: grid;
    place-items: center;
    margin-left: .25rem;
    border: 1px solid rgba(239, 185, 74, .33);
    border-radius: 50%;
    color: var(--gold-bright);
    background: rgba(239,185,74,.05);
    box-shadow: 0 0 22px rgba(239,185,74,.11);
}
.nav-om { font-family: "Noto Sans Devanagari", serif; font-size: 1.35rem; }

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    width: 292px !important;
    min-width: 292px !important;
    background:
        radial-gradient(circle at 50% 0%, rgba(78, 69, 164, .17), transparent 30%),
        linear-gradient(180deg, rgba(5, 13, 36, .99), rgba(3, 9, 26, .995));
    border-right: 1px solid rgba(239, 185, 74, .27);
    box-shadow: 18px 0 60px rgba(0,0,0,.30);
}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding-top: .7rem; }
[data-testid="stSidebar"] .block-container { padding-left: .75rem; padding-right: .75rem; }

.sidebar-brand {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: .8rem;
    padding: .55rem .2rem .7rem;
}
.sidebar-om {
    width: 62px;
    height: 62px;
    display: grid;
    place-items: center;
    color: var(--gold-bright);
    font-family: "Noto Sans Devanagari", serif;
    font-size: 2.2rem;
    border: 1px solid rgba(239,185,74,.42);
    border-radius: 50%;
    background: radial-gradient(circle, rgba(239,185,74,.16), rgba(239,185,74,.03) 63%, transparent 65%);
    box-shadow: 0 0 0 7px rgba(239,185,74,.035), 0 0 34px rgba(239,185,74,.17);
    animation: sealPulse 5.5s ease-in-out infinite;
}
.sidebar-brand h2 {
    margin: 0;
    color: var(--gold-bright);
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 1.7rem;
    line-height: .88;
}
.sidebar-brand p {
    margin: .35rem 0 0;
    color: #aaa3b7;
    font-size: .62rem;
}
.sidebar-divider {
    position: relative;
    height: 20px;
    margin-bottom: .15rem;
    text-align: center;
}
.sidebar-divider::before {
    content: "";
    position: absolute;
    left: 5%; right: 5%; top: 50%;
    border-top: 1px solid rgba(239,185,74,.22);
}
.sidebar-divider span {
    position: relative;
    padding: 0 .5rem;
    color: var(--gold);
    background: #050d24;
    font-size: .7rem;
}
.sidebar-section-title {
    margin: 0 0 .65rem;
    padding: .68rem .75rem;
    color: var(--gold-bright);
    font-family: "Cormorant Garamond", "Noto Sans Devanagari", serif;
    font-size: 1.12rem;
    font-weight: 700;
    border: 1px solid rgba(239,185,74,.15);
    border-radius: 12px;
    background: linear-gradient(100deg, rgba(239,185,74,.08), transparent);
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #eee6f0 !important;
    font-size: .75rem;
    font-weight: 700;
}
[data-testid="stSidebar"] [role="radiogroup"] {
    padding: .3rem;
    gap: .2rem;
    border: 1px solid rgba(239,185,74,.12);
    border-radius: 12px;
    background: rgba(255,255,255,.025);
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: .42rem .45rem;
    border-radius: 8px;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] input {
    color: var(--cream) !important;
    border-color: rgba(239,185,74,.22) !important;
    background: rgba(255,255,255,.045) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(239,185,74,.14); }
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: var(--gold) !important;
    border-color: var(--gold-bright) !important;
    box-shadow: 0 0 13px rgba(239,185,74,.28);
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] { margin-bottom: .6rem; }

.api-card {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: .7rem;
    align-items: center;
    margin: .65rem 0 .7rem;
    padding: .8rem;
    border: 1px solid rgba(114,230,160,.28);
    border-radius: 13px;
    background: rgba(24, 112, 69, .08);
}
.api-card.missing { border-color: rgba(255,126,126,.28); background: rgba(138,38,58,.09); }
.api-card.local { border-color: rgba(239,185,74,.25); background: rgba(239,185,74,.06); }
.api-shield {
    width: 41px; height: 41px;
    display: grid; place-items: center;
    border-radius: 50%;
    color: #061424;
    background: var(--green);
    font-weight: 900;
    box-shadow: 0 0 20px rgba(114,230,160,.25);
}
.api-card.missing .api-shield { background: #ff8d99; }
.api-card.local .api-shield { background: var(--gold); }
.api-card strong, .api-card small, .api-card b { display: block; }
.api-card strong { color: var(--gold-bright); font-size: .72rem; }
.api-card small { margin-top: .2rem; color: #bbb4c4; font-size: .62rem; }
.api-card b { margin-top: .3rem; color: var(--green); font-size: .65rem; }
.api-card.missing b { color: #ff9eaa; }
.api-card.local b { color: var(--gold); }

[data-testid="stSidebar"] .stButton > button {
    border-color: rgba(227,74,133,.55) !important;
    color: #ffdbe8 !important;
    background: linear-gradient(135deg, rgba(125,17,74,.6), rgba(80,15,52,.62)) !important;
}

.daily-card, .chant-card {
    position: relative;
    margin-top: .75rem;
    padding: .9rem;
    overflow: hidden;
    border: 1px solid rgba(239,185,74,.20);
    border-radius: 15px;
    background: linear-gradient(145deg, rgba(255,255,255,.042), rgba(255,255,255,.018));
}
.daily-title, .chant-title { color: var(--gold-bright); font-size: .75rem; font-weight: 800; }
.daily-title span { color: #b9b1c1; font-size: .62rem; }
.daily-card p { margin: .75rem 0 .45rem; color: var(--gold); font-family: "Noto Sans Devanagari", serif; font-size: .76rem; line-height: 1.7; }
.daily-card small, .chant-card small { color: #aaa2b3; font-size: .6rem; }
.lotus-mark { position: absolute; right: -5px; bottom: -23px; color: rgba(239,185,74,.14); font-size: 4rem; transform: rotate(28deg); }
.chant-card { background: linear-gradient(145deg, rgba(29,49,111,.52), rgba(9,20,55,.57)); }
.chant-card p { margin: .45rem 0 .6rem; color: #b8b3c6; font-size: .64rem; }
.chant-row { display: flex; align-items: center; gap: .6rem; }
.chant-play { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 50%; color: white; background: #244c9d; box-shadow: 0 0 23px rgba(57,101,192,.25); }
.chant-wave { color: #6d8dd2; font-size: .7rem; letter-spacing: .1em; animation: chantWave 2.2s ease-in-out infinite; }

/* ── Animated Krishna hero ────────────────────────────────────────────── */
.krishna-hero {
    position: relative;
    height: 570px;
    overflow: hidden;
    isolation: isolate;
    border: 1px solid rgba(239,185,74,.24);
    border-radius: 24px;
    background:
        radial-gradient(circle at 54% 27%, rgba(255,202,89,.20), transparent 28%),
        radial-gradient(circle at 12% 55%, rgba(173,86,43,.20), transparent 31%),
        linear-gradient(145deg, #06112d 0%, #11153b 47%, #071126 100%);
    box-shadow: 0 28px 90px rgba(0,0,0,.40), inset 0 1px 0 rgba(255,255,255,.055);
}
.krishna-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -3;
    opacity: .65;
    background:
        linear-gradient(180deg, transparent 45%, rgba(2,7,22,.82)),
        radial-gradient(circle at 72% 26%, rgba(255,208,99,.09), transparent 25%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='190' height='150'%3E%3Cg fill='%23ffe19a' fill-opacity='.18'%3E%3Ccircle cx='12' cy='19' r='1'/%3E%3Ccircle cx='72' cy='41' r='.8'/%3E%3Ccircle cx='155' cy='27' r='1'/%3E%3Ccircle cx='119' cy='101' r='.7'/%3E%3Ccircle cx='38' cy='125' r='.8'/%3E%3C/g%3E%3C/svg%3E");
    animation: heroStars 36s linear infinite;
}
.hero-nebula {
    position: absolute;
    left: 16%; top: -34%;
    width: 78%; height: 100%;
    z-index: -2;
    border-radius: 50%;
    background: conic-gradient(from 70deg, transparent, rgba(239,185,74,.09), transparent 18%, rgba(75,84,195,.10), transparent 41%, rgba(239,185,74,.08), transparent 72%);
    filter: blur(22px);
    animation: nebulaRotate 40s linear infinite;
}
.hero-rays {
    position: absolute;
    left: 57%; top: 43%;
    width: 540px; height: 540px;
    z-index: -1;
    transform: translate(-50%,-50%);
    border-radius: 50%;
    opacity: .34;
    background: repeating-conic-gradient(from 0deg, rgba(255,225,147,.18) 0 1deg, transparent 1deg 10deg);
    mask-image: radial-gradient(circle, transparent 0 24%, #000 37%, transparent 69%);
    animation: raySpin 55s linear infinite;
}
.hero-verse {
    position: absolute;
    left: 24px;
    top: 80px;
    z-index: 6;
    width: 205px;
    padding: 1rem .9rem;
    color: var(--gold-bright);
    font-family: "Noto Sans Devanagari", serif;
    text-shadow: 0 3px 13px rgba(0,0,0,.72);
}
.hero-verse::before {
    content: "✦";
    position: absolute;
    left: -2px; top: -6px;
    color: var(--gold);
    font-size: .7rem;
}
.hero-verse span { display: block; font-size: 1.04rem; font-weight: 600; line-height: 1.63; }
.hero-verse small { display: block; margin-top: .7rem; color: #d0c7d5; font-family: Inter, sans-serif; font-size: .68rem; }

.krishna-aura {
    position: absolute;
    left: 57%; top: 44%;
    z-index: 1;
    transform: translate(-50%,-50%);
    border-radius: 50%;
    pointer-events: none;
}
.aura-a {
    width: 410px; height: 410px;
    background: radial-gradient(circle, rgba(255,224,142,.30), rgba(239,185,74,.09) 42%, transparent 69%);
    filter: blur(2px);
    animation: auraPulse 5.2s ease-in-out infinite;
}
.aura-b {
    width: 475px; height: 475px;
    border: 1px solid rgba(239,185,74,.20);
    box-shadow: 0 0 60px rgba(239,185,74,.12), inset 0 0 60px rgba(239,185,74,.06);
    animation: auraRing 11s ease-in-out infinite;
}
.krishna-figure {
    position: absolute;
    left: 57%;
    top: 49%;
    z-index: 3;
    width: 455px;
    height: 620px;
    transform: translate(-50%,-50%);
    object-fit: cover;
    object-position: 50% 34%;
    border-radius: 45% 45% 10% 10% / 15% 15% 6% 6%;
    filter: saturate(1.08) contrast(1.04) drop-shadow(0 24px 35px rgba(0,0,0,.56));
    mask-image: linear-gradient(to bottom, transparent 0%, #000 5%, #000 84%, transparent 100%), linear-gradient(to right, transparent 0%, #000 9%, #000 91%, transparent 100%);
    mask-composite: intersect;
    animation: krishnaBreath 7.5s ease-in-out infinite;
    transform-origin: 50% 82%;
}
.chakra-rotor {
    position: absolute;
    left: calc(57% - 198px);
    top: 186px;
    z-index: 5;
    width: 95px;
    height: 95px;
    display: grid;
    place-items: center;
    border: 2px solid rgba(255,222,139,.72);
    border-radius: 50%;
    color: var(--gold-bright);
    box-shadow: 0 0 20px rgba(239,185,74,.42), inset 0 0 20px rgba(239,185,74,.25);
    animation: chakraOrbit 12s linear infinite;
}
.chakra-rotor::before, .chakra-rotor::after {
    content: "";
    position: absolute;
    inset: 11px;
    border: 1px dashed rgba(255,225,154,.70);
    border-radius: 50%;
}
.chakra-rotor::after { inset: 28px; border-style: solid; }
.chakra-rotor span { font-size: 2.2rem; }

.hero-petal {
    position: absolute;
    z-index: 7;
    color: #f8a6c0;
    filter: drop-shadow(0 0 9px rgba(248,166,192,.4));
    animation: heroPetal 9s ease-in-out infinite;
}
.hp-one { left: 26%; top: 16%; font-size: 18px; }
.hp-two { right: 7%; top: 36%; animation-delay: -2s; font-size: 22px; }
.hp-three { left: 14%; bottom: 20%; animation-delay: -5s; }
.hp-four { right: 18%; bottom: 14%; animation-delay: -7s; font-size: 14px; }

.hero-counts {
    position: absolute;
    left: 25px;
    bottom: 76px;
    z-index: 7;
    display: flex;
    gap: .4rem;
}
.hero-counts div {
    min-width: 64px;
    padding: .55rem .55rem .48rem;
    text-align: center;
    border: 1px solid rgba(239,185,74,.23);
    border-radius: 10px;
    background: rgba(5,11,31,.73);
    backdrop-filter: blur(9px);
}
.hero-counts b, .hero-counts span { display: block; }
.hero-counts b { color: var(--gold-bright); font-family: "Cormorant Garamond", serif; font-size: 1.2rem; }
.hero-counts span { color: #d3c8d3; font-size: .58rem; }
.hero-config {
    position: absolute;
    right: 21px;
    bottom: 80px;
    z-index: 7;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: .34rem;
}
.hero-config span {
    padding: .38rem .58rem;
    color: #d8cfda;
    border: 1px solid rgba(239,185,74,.16);
    border-radius: 999px;
    background: rgba(4,10,29,.66);
    font-size: .62rem;
    backdrop-filter: blur(8px);
}
.hero-mantra {
    position: absolute;
    left: 20px; right: 20px; bottom: 19px;
    z-index: 8;
    padding: .62rem .8rem;
    text-align: center;
    color: #e5c77e;
    border: 1px solid rgba(239,185,74,.31);
    border-radius: 999px;
    background: rgba(4,9,27,.73);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
    font-family: "Cormorant Garamond", "Noto Sans Devanagari", serif;
    font-size: .72rem;
    letter-spacing: .025em;
    backdrop-filter: blur(12px);
}

/* ── Section headings and buttons ────────────────────────────────────── */
.section-heading {
    margin: .8rem 0 .55rem;
    padding: .78rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    border: 1px solid rgba(239,185,74,.20);
    border-radius: 15px;
    background: linear-gradient(100deg, rgba(239,185,74,.065), rgba(7,15,42,.72));
}
.section-heading div span, .section-heading div strong { display: block; }
.section-heading div span { color: var(--gold-bright); font-family: "Noto Sans Devanagari", serif; font-size: .94rem; font-weight: 700; }
.section-heading div strong { margin-top: .08rem; color: #c7bfce; font-size: .65rem; letter-spacing: .07em; text-transform: uppercase; }
.section-heading small { color: #8e869c; font-size: .64rem; }
.chat-heading { margin-top: .75rem; }

.stButton > button,
.stFormSubmitButton > button {
    min-height: 2.65rem;
    border: 1px solid rgba(239,185,74,.25) !important;
    border-radius: 12px !important;
    color: #f9eedf !important;
    background: linear-gradient(135deg, rgba(239,185,74,.09), rgba(92,36,114,.12)) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045), 0 8px 24px rgba(0,0,0,.16);
    font-size: .75rem !important;
    font-weight: 700 !important;
    transition: transform .18s ease, border-color .18s ease, color .18s ease, box-shadow .18s ease !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    color: var(--gold-bright) !important;
    border-color: rgba(239,185,74,.65) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,.24), 0 0 22px rgba(239,185,74,.09);
}
.stFormSubmitButton > button {
    color: #171024 !important;
    background: linear-gradient(135deg, var(--gold-bright), var(--gold)) !important;
}

/* ── Chat ─────────────────────────────────────────────────────────────── */
.welcome-message {
    position: relative;
    margin: .2rem 0 .7rem;
    padding: .85rem 3.1rem .85rem .85rem;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: .8rem;
    align-items: center;
    border: 1px solid rgba(239,185,74,.22);
    border-radius: 17px;
    background: linear-gradient(130deg, rgba(42,24,76,.80), rgba(12,20,52,.78));
    box-shadow: 0 14px 38px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.05);
}
.welcome-message img {
    width: 54px; height: 54px;
    object-fit: cover;
    border: 2px solid var(--gold);
    border-radius: 50%;
    box-shadow: 0 0 0 5px rgba(239,185,74,.06), 0 0 22px rgba(239,185,74,.18);
}
.welcome-message small { color: var(--gold); font-size: .65rem; font-weight: 800; }
.welcome-message p { margin: .25rem 0 0; color: #e2d9e4; font-family: "Noto Sans Devanagari", Inter, sans-serif; font-size: .82rem; line-height: 1.65; }
.voice-dot { position: absolute; right: 16px; top: 50%; transform: translateY(-50%); width: 29px; height: 29px; display: grid; place-items: center; border-radius: 50%; color: var(--gold-bright); background: rgba(239,185,74,.08); }

[data-testid="stChatMessage"] {
    margin: .55rem 0;
    padding: .82rem .9rem;
    border: 1px solid rgba(239,185,74,.13);
    border-radius: 17px;
    background: linear-gradient(135deg, rgba(18,23,58,.76), rgba(10,15,39,.76));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 12px 34px rgba(0,0,0,.14);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    margin-left: 18%;
    border-color: rgba(69,108,231,.31);
    background: linear-gradient(135deg, rgba(18,45,117,.65), rgba(11,25,69,.72));
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { color: #ded7e3; line-height: 1.65; }
[data-testid="stChatMessage"] h3 { color: var(--gold-bright); font-family: "Cormorant Garamond", "Noto Sans Devanagari", serif; }
[data-testid="stChatMessage"] img { border: 1px solid rgba(239,185,74,.30); }

[data-testid="stForm"] {
    margin-top: .65rem;
    padding: .65rem;
    border: 1px solid rgba(239,185,74,.22);
    border-radius: 17px;
    background: rgba(4,11,32,.78);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 15px 38px rgba(0,0,0,.18);
}
[data-testid="stForm"] [data-testid="stTextInput"] { margin-bottom: 0; }
[data-testid="stForm"] input {
    min-height: 44px;
    color: var(--cream) !important;
    border: 1px solid rgba(239,185,74,.18) !important;
    border-radius: 11px !important;
    background: rgba(255,255,255,.035) !important;
}
[data-testid="stForm"] input:focus {
    border-color: rgba(239,185,74,.58) !important;
    box-shadow: 0 0 0 1px rgba(239,185,74,.16), 0 0 24px rgba(239,185,74,.08) !important;
}

/* ── Right retrieved-passages panel ───────────────────────────────────── */
.right-panel-title {
    margin: .75rem 0 .5rem;
    padding: .78rem .85rem;
    display: flex;
    align-items: center;
    gap: .65rem;
    border: 1px solid rgba(239,185,74,.23);
    border-radius: 14px;
    background: linear-gradient(100deg, rgba(239,185,74,.07), rgba(7,15,43,.74));
}
.right-panel-title > span { font-size: 1.1rem; }
.right-panel-title strong, .right-panel-title small { display: block; }
.right-panel-title strong { color: var(--gold-bright); font-family: "Noto Sans Devanagari", serif; font-size: .85rem; }
.right-panel-title small { margin-top: .05rem; color: #aaa2b4; font-size: .6rem; letter-spacing: .09em; text-transform: uppercase; }

.retrieval-card {
    margin-bottom: .45rem;
    padding: .72rem .78rem;
    border: 1px solid rgba(239,185,74,.18);
    border-radius: 13px;
    background: linear-gradient(135deg, rgba(12,22,56,.84), rgba(7,15,39,.84));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035);
}
.retrieval-card header { display: flex; align-items: center; justify-content: space-between; gap: .5rem; }
.retrieval-card header strong { color: var(--gold-bright); font-size: .68rem; }
.retrieval-card header span { color: #bcb5c7; font-size: .56rem; white-space: nowrap; }
.retrieval-card p { margin: .48rem 0 .55rem; color: #cec6d2; font-family: "Noto Sans Devanagari", Inter, sans-serif; font-size: .62rem; line-height: 1.55; }
.similarity-track { height: 4px; overflow: hidden; border-radius: 999px; background: rgba(255,255,255,.07); }
.similarity-track i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--gold), var(--gold-bright)); box-shadow: 0 0 10px rgba(239,185,74,.35); }
.sources-empty {
    min-height: 132px;
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    border: 1px dashed rgba(239,185,74,.20);
    border-radius: 14px;
    background: rgba(255,255,255,.018);
}
.sources-empty b { color: var(--gold-bright); font-size: .78rem; }
.sources-empty span { margin-top: .45rem; color: #9790a4; font-size: .62rem; line-height: 1.55; }
[data-testid="stExpander"] {
    border-color: rgba(239,185,74,.16) !important;
    background: rgba(255,255,255,.018) !important;
}

.about-strip {
    margin-top: .8rem;
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap: .5rem;
}
.about-strip div {
    padding: .75rem;
    border: 1px solid rgba(239,185,74,.13);
    border-radius: 13px;
    background: rgba(255,255,255,.018);
}
.about-strip span, .about-strip strong, .about-strip small { display: block; }
.about-strip span { color: var(--gold); font-family: "Cormorant Garamond", serif; font-size: 1.3rem; }
.about-strip strong { margin-top: .18rem; color: var(--gold-bright); font-size: .68rem; }
.about-strip small { margin-top: .2rem; color: #90899a; font-size: .56rem; line-height: 1.45; }

.temple-footer {
    position: relative;
    z-index: 4;
    margin-top: 1rem;
    padding: .75rem 1rem;
    text-align: center;
    color: #c8a964;
    border-top: 1px solid rgba(239,185,74,.18);
    background: linear-gradient(90deg, transparent, rgba(239,185,74,.025), transparent);
    font-family: "Cormorant Garamond", "Noto Sans Devanagari", serif;
    font-size: .75rem;
    letter-spacing: .025em;
}

/* ── Animation definitions ────────────────────────────────────────────── */
@keyframes starDrift { to { background-position: 310px 260px, -420px 390px, 360px -310px, -480px -420px, 330px 300px, -390px 350px, 520px -460px, -450px 390px; } }
@keyframes orbWander { 0% { transform: translate3d(-5%, -3%, 0) scale(.92); } 100% { transform: translate3d(8%, 7%, 0) scale(1.12); } }
@keyframes petalFall { 0% { transform: translate3d(0,-12vh,0) rotate(0deg); opacity:0; } 8%{opacity:.65} 50% { transform: translate3d(45px,52vh,0) rotate(190deg); } 100% { transform: translate3d(-35px,112vh,0) rotate(410deg); opacity:0; } }
@keyframes firefly { 0%,100% { transform: translate(0,0) scale(.65); opacity:.2; } 32% { transform: translate(34px,-21px) scale(1.5); opacity:1; } 67% { transform: translate(-19px,27px) scale(.9); opacity:.5; } }
@keyframes sealPulse { 0%,100% { transform: scale(.96); box-shadow:0 0 0 7px rgba(239,185,74,.035),0 0 30px rgba(239,185,74,.13);} 50% {transform:scale(1.04);box-shadow:0 0 0 10px rgba(239,185,74,.045),0 0 42px rgba(239,185,74,.25);} }
@keyframes chantWave { 0%,100% { transform: scaleY(.7); opacity:.55; } 50% { transform: scaleY(1.25); opacity:1; } }
@keyframes heroStars { to { background-position: 0 0, 0 0, 190px 150px; } }
@keyframes nebulaRotate { to { transform: rotate(360deg); } }
@keyframes raySpin { from { transform: translate(-50%,-50%) rotate(0deg); } to { transform: translate(-50%,-50%) rotate(360deg); } }
@keyframes auraPulse { 0%,100% { transform:translate(-50%,-50%) scale(.92); opacity:.58; } 50% { transform:translate(-50%,-50%) scale(1.09); opacity:1; } }
@keyframes auraRing { 0%,100% { transform:translate(-50%,-50%) scale(.95) rotate(0deg); opacity:.48; } 50% { transform:translate(-50%,-50%) scale(1.04) rotate(7deg); opacity:.86; } }
@keyframes krishnaBreath { 0%,100% { transform:translate(-50%,-50%) translateY(3px) scale(1); } 50% { transform:translate(-50%,-50%) translateY(-8px) scale(1.012); } }
@keyframes chakraOrbit { to { transform: rotate(360deg); } }
@keyframes heroPetal { 0%,100% { transform:translate(0,0) rotate(-15deg); opacity:.42; } 50% { transform:translate(15px,-22px) rotate(28deg); opacity:.9; } }

/* ── Responsive layout ───────────────────────────────────────────────── */
@media (max-width: 1250px) {
    .krishna-hero { height: 530px; }
    .krishna-figure { width: 405px; height: 570px; left: 59%; }
    .krishna-aura, .hero-rays { left: 59%; }
    .chakra-rotor { left: calc(59% - 180px); }
    .hero-verse { width: 180px; left: 14px; }
    .hero-verse span { font-size: .9rem; }
    .temple-nav a { padding-left: .6rem; padding-right: .6rem; }
}

@media (max-width: 980px) {
    .temple-nav a span { display:none; }
    .krishna-hero { height: 510px; }
    .hero-verse { display:none; }
    .krishna-figure { left:50%; width:390px; }
    .krishna-aura, .hero-rays { left:50%; }
    .chakra-rotor { left: calc(50% - 175px); }
    .hero-config { display:none; }
    .about-strip { grid-template-columns: repeat(2,1fr); }
}

@media (max-width: 720px) {
    .block-container { padding-left:.55rem; padding-right:.55rem; }
    .temple-nav { position:relative; top:0; justify-content:center; }
    .nav-spacer { display:none; }
    .nav-sun, .nav-om { width:35px;height:35px; }
    .krishna-hero { height:470px; border-radius:18px; }
    .krishna-figure { top:47%; width:345px; height:510px; }
    .aura-a { width:330px;height:330px; }
    .aura-b { width:380px;height:380px; }
    .chakra-rotor { width:72px;height:72px; left:calc(50% - 145px); top:166px; }
    .hero-counts { left:50%; transform:translateX(-50%); bottom:66px; }
    .hero-config { display:none; }
    .hero-mantra { left:10px;right:10px;bottom:12px;font-size:.58rem; }
    .section-heading { align-items:flex-start; flex-direction:column; }
    .section-heading small { display:none; }
    .about-strip { grid-template-columns:1fr 1fr; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { margin-left:5%; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: .01ms !important;
    }
}
</style>
"""
