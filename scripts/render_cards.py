#!/usr/bin/env python3
"""Render the animated SVG cards for the GitHub profile README.

Usage:
    python scripts/render_cards.py           # animated cards -> cards/
    STATIC=1 python scripts/render_cards.py  # every animation at its final frame

Cards use CSS keyframes and SMIL only, so they keep working when GitHub
shows them through <img>. Fonts are Pretendard (SIL OFL 1.1), subset to
ASCII plus a few symbols and embedded as base64 WOFF2.
"""
import base64
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cards"
FONTS = ROOT / "fonts"
STATIC = os.environ.get("STATIC") == "1"

# Colours taken from the SportiQue YC / US pitch deck (R10).
INK = "#10234a"
BLUE = "#0746c7"
MUTED = "#526174"
LINE = "#e3e8f2"


def font_face(family: str, file: str, weight: int) -> str:
    data = base64.b64encode((FONTS / file).read_bytes()).decode()
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};"
        f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
    )


FONT_CSS = "".join(
    [
        font_face("PT", "Pretendard-Regular.subset.woff2", 400),
        font_face("PT", "Pretendard-SemiBold.subset.woff2", 600),
        font_face("PT", "Pretendard-ExtraBold.subset.woff2", 800),
    ]
)

BASE_CSS = f"""
:root{{--paper:#ffffff;--ink:{INK};--blue:{BLUE};--muted:{MUTED};--line:{LINE};--soft:#f3f6fc;}}
@media (prefers-color-scheme: dark){{
  :root{{--paper:#0d1424;--ink:#e8eefc;--blue:#5b8cff;--muted:#9aa6bf;--line:#223154;--soft:#14203a;}}
}}
text{{font-family:'PT',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;fill:var(--ink);}}
.paper{{fill:var(--paper);stroke:var(--line);stroke-width:1;}}
.ink{{fill:var(--ink);}} .blue{{fill:var(--blue);}} .muted{{fill:var(--muted);}}
.soft{{fill:var(--soft);}}
[data-s=line]{{stroke:var(--line);}} [data-s=blue]{{stroke:var(--blue);}} [data-f=blue]{{fill:var(--blue);}}
.w4{{font-weight:400;}} .w6{{font-weight:600;}} .w8{{font-weight:800;}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.4)}}70%{{opacity:1;transform:scale(1.12)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes draw{{from{{stroke-dashoffset:var(--len,600)}}to{{stroke-dashoffset:0}}}}
@keyframes pulse{{0%{{opacity:.55;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
@keyframes swing{{0%{{opacity:0;transform:translateY(40px) rotate(-6deg)}}65%{{opacity:1;transform:translateY(-4px) rotate(1.5deg)}}100%{{opacity:1;transform:none}}}}
@keyframes nudge{{0%,100%{{transform:none}}50%{{transform:translateX(4px)}}}}
@keyframes halo{{0%{{opacity:.5;transform:scale(1)}}100%{{opacity:0;transform:scale(1.18)}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.a{{animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.7,.2,1);transform-box:fill-box;transform-origin:center;}}
.rise{{animation-name:rise;animation-duration:.7s;}}
.fade{{animation-name:fade;animation-duration:.8s;}}
.pop{{animation-name:pop;animation-duration:.5s;}}
.draw{{animation-name:draw;animation-duration:1.1s;stroke-dasharray:var(--len,600);}}
.swing{{animation-name:swing;animation-duration:1s;transform-origin:bottom left;}}
.pulse{{animation:pulse 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center;}}
.halo{{animation:halo 3s ease-out infinite;transform-box:fill-box;transform-origin:center;}}
.nudge{{animation:nudge 1.6s ease-in-out infinite;}}
.blink{{animation:blink 1.8s ease-in-out infinite;}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important;}}}}
"""

STATIC_CSS = "*{animation:none!important;}.pulse,.halo{opacity:0;}"


def svg(width: int, height: int, body: str, title: str) -> str:
    css = FONT_CSS + BASE_CSS + (STATIC_CSS if STATIC else "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{title}">'
        f"<title>{title}</title><style>{css}</style>"
        f'<rect class="paper" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="14"/>'
        f"{body}</svg>"
    )


def d(seconds: float) -> str:
    return f"animation-delay:{seconds:.2f}s;"


def smil(markup: str) -> str:
    return "" if STATIC else markup


def pixel_mark(x: int, y: int, s: int = 4) -> str:
    """Original pixel badge: a speech bubble holding a pulse line."""
    rows = [
        "0111111110",
        "1000000001",
        "1000000001",
        "1000100001",
        "1101010101",
        "1000001001",
        "1000000001",
        "0111111110",
        "0001100000",
        "0001000000",
    ]
    rects = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "1":
                rects.append(
                    f'<rect x="{x + c*s}" y="{y + r*s}" width="{s}" height="{s}" class="blue"/>'
                )
    return "".join(rects)


# ---------------------------------------------------------------- hero
def hero() -> str:
    w, h = 880, 300
    lines = [
        "Control your health data.",
        "Choose which studies to join.",
        "Get rewarded for taking part.",
    ]
    shine = smil(
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'values="-1 0;1.4 0;1.4 0" keyTimes="0;0.45;1" dur="5s" begin="1.4s" repeatCount="indefinite"/>'
    )
    body = f"""
<defs>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" style="stop-color:var(--ink)"/>
    <stop offset="0.42" style="stop-color:var(--ink)"/>
    <stop offset="0.5" style="stop-color:var(--blue)"/>
    <stop offset="0.58" style="stop-color:var(--ink)"/>
    <stop offset="1" style="stop-color:var(--ink)"/>
    {shine}
  </linearGradient>
</defs>
<g class="a pop" style="{d(.05)}">{pixel_mark(40, 34)}</g>
<text x="92" y="64" class="w8 blue a rise" style="font-size:26px;{d(.15)}">SportiQue</text>
<text x="840" y="58" text-anchor="end" class="w6 muted a fade" style="font-size:14px;{d(.3)}">Seunghun (Daniel) Lee · Founder &amp; CEO</text>
<text x="40" y="138" class="w8 a rise" style="font-size:44px;fill:url(#shine);{d(.35)}">A personal health database</text>
<text x="40" y="190" class="w8 a rise" style="font-size:44px;fill:url(#shine);{d(.5)}">and research marketplace</text>
"""
    for i, line in enumerate(lines):
        body += (
            f'<text x="40" y="{232 + i*24}" class="w4 blue a rise" '
            f'style="font-size:18px;{d(.9 + i*.18)}">{line}</text>'
        )
    # heartbeat line on the right
    body += f"""
<polyline points="600,250 660,250 676,222 690,272 706,232 718,250 840,250"
  fill="none" data-s="blue" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"
  class="a draw" style="--len:330;{d(1.2)}animation-duration:1.6s;"/>
<circle cx="840" cy="250" r="5" class="blue a pop" style="{d(2.6)}"/>
<circle cx="840" cy="250" r="5" class="blue pulse" style="{d(2.8)}"/>
"""
    return svg(w, h, body, "SportiQue: a personal health database and research marketplace")


# ---------------------------------------------------------------- flow
def flow() -> str:
    w, h = 880, 280
    sources = ["Wearables", "Hospital records", "Checkups", "Fitness tests"]
    targets = [("UniQLab", "research teams"), ("Apps", "through the SDK")]
    body = f'<text x="40" y="44" class="w8 a rise" style="font-size:20px;{d(.05)}">How data moves</text>'
    body += f'<text x="840" y="44" text-anchor="end" class="w4 muted a fade" style="font-size:13px;{d(.2)}">nothing leaves without your consent</text>'
    cx, cy = 440, 160
    # sources
    for i, name in enumerate(sources):
        y = 86 + i * 46
        body += (
            f'<g class="a rise" style="{d(.2 + i*.1)}">'
            f'<rect x="40" y="{y-18}" width="170" height="32" rx="8" class="soft"/>'
            f'<text x="56" y="{y+3}" class="w6" style="font-size:14px">{name}</text></g>'
        )
        path = f"M210,{y-2} C320,{y-2} 330,{cy} {cx-78},{cy}"
        body += (
            f'<path id="s{i}" d="{path}" fill="none" data-s="line" stroke-width="2" '
            f'class="a draw" style="--len:300;{d(.5 + i*.1)}"/>'
        )
        body += smil(
            f'<circle r="4" class="blue"><animateMotion dur="2.6s" begin="{1.4 + i*.45}s" '
            f'repeatCount="indefinite"><mpath href="#s{i}"/></animateMotion></circle>'
        )
    # centre
    body += f"""
<g class="a pop" style="{d(1.0)}">
  <rect x="{cx-78}" y="{cy-40}" width="156" height="80" rx="14" data-f="blue"/>
  <text x="{cx}" y="{cy-6}" text-anchor="middle" class="w8" style="font-size:20px;fill:#fff">UniQdata</text>
  <text x="{cx}" y="{cy+18}" text-anchor="middle" class="w4" style="font-size:13px;fill:#dbe6ff">your personal health DB</text>
</g>
<rect x="{cx-78}" y="{cy-40}" width="156" height="80" rx="14" fill="none" data-s="blue" stroke-width="2" class="halo" style="{d(2.2)}"/>
"""
    # targets
    for i, (name, sub) in enumerate(targets):
        y = 118 + i * 84
        path = f"M{cx+78},{cy} C{cx+170},{cy} {cx+150},{y} 650,{y}"
        body += (
            f'<path id="t{i}" d="{path}" fill="none" data-s="line" stroke-width="2" '
            f'class="a draw" style="--len:260;{d(1.3 + i*.1)}"/>'
        )
        body += smil(
            f'<circle r="4" class="blue"><animateMotion dur="2.2s" begin="{2.2 + i*.6}s" '
            f'repeatCount="indefinite"><mpath href="#t{i}"/></animateMotion></circle>'
        )
        body += (
            f'<g class="a rise" style="{d(1.5 + i*.12)}">'
            f'<rect x="650" y="{y-26}" width="190" height="52" rx="10" class="soft"/>'
            f'<text x="666" y="{y-3}" class="w8" style="font-size:16px">{name}</text>'
            f'<text x="666" y="{y+16}" class="w4 muted" style="font-size:12px">{sub}</text></g>'
        )
    body += (
        f'<text x="{cx}" y="258" text-anchor="middle" class="w6 blue a fade" '
        f'style="font-size:13px;{d(2.4)}">← rewards go back to the person who shared</text>'
    )
    return svg(w, h, body, "How data moves: sources to UniQdata, then with consent to UniQLab and apps")


# ---------------------------------------------------------------- tiles
TILES = {
    "uniqdata": ("PERSONAL", "UniQdata", ["Your health records in one", "place. You decide who", "sees them and for how long."], "app.uniqdata.io"),
    "uniqlab": ("RESEARCH", "UniQLab", ["A research workspace with", "consent-scoped access to", "participants' records."], "web.uniqlab.io"),
    "console": ("TEAMS", "Business Console", ["Workspaces, services and", "roles for organisations.", "One bill per company."], "org.sportique.biz"),
}


def tile(key: str, order: int) -> str:
    w, h = 286, 210
    tag, name, lines, url = TILES[key]
    base = .2 + order * .25
    shine = smil(
        '<animateTransform attributeName="gradientTransform" type="translate" '
        f'values="-1.2 0;1.2 0;1.2 0" keyTimes="0;0.3;1" dur="6s" begin="{2 + order*.5}s" repeatCount="indefinite"/>'
    )
    body = f"""
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0.35" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#fff" stop-opacity="0.18"/>
    <stop offset="0.65" stop-color="#fff" stop-opacity="0"/>
    {shine}
  </linearGradient>
</defs>
<g class="a swing" style="{d(base)}">
  <rect x="12" y="12" width="{w-24}" height="{h-24}" rx="12" data-f="blue"/>
  <rect x="12" y="12" width="{w-24}" height="{h-24}" rx="12" fill="url(#g)"/>
  <text x="32" y="46" class="w6" style="font-size:11px;letter-spacing:2px;fill:#cfdcff">{tag}</text>
  <text x="32" y="84" class="w8" style="font-size:26px;fill:#fff">{name}</text>
"""
    for i, line in enumerate(lines):
        body += f'<text x="32" y="{114 + i*19}" class="w4" style="font-size:13.5px;fill:#e6edff">{line}</text>'
    body += f"""
  <text x="32" y="{h-30}" class="w6" style="font-size:13px;fill:#fff">{url}</text>
  <g class="nudge" style="{d(base + 1.2)}"><text x="{w-36}" y="{h-30}" text-anchor="end" class="w8" style="font-size:16px;fill:#fff">→</text></g>
</g>
<circle cx="{w-34}" cy="34" r="5" fill="#fff" class="a pop" style="{d(base + .8)}"/>
<circle cx="{w-34}" cy="34" r="5" fill="#fff" class="pulse" style="{d(base + 1)}"/>
"""
    return svg(w, h, body, f"{name}: {' '.join(lines)}")


# ---------------------------------------------------------------- journey
def journey() -> str:
    w, h = 880, 230
    steps = [
        ("2022", "Started coding", "AI Expert certificate (KSA)"),
        ("2024", "Purdue IoT research", "First author, ICCAS 2024"),
        ("2025", "XRPL prototype", "Consent scopes, auto rewards"),
        ("2026", "UniQdata · UniQLab", "YAKSON device · ACK 2026"),
    ]
    body = f'<text x="40" y="44" class="w8 a rise" style="font-size:20px;{d(.05)}">Things I built</text>'
    body += f'<text x="840" y="44" text-anchor="end" class="w4 muted a fade" style="font-size:13px;{d(.2)}">founder, building the product myself</text>'
    y = 100
    body += (
        f'<line x1="60" y1="{y}" x2="820" y2="{y}" data-s="line" stroke-width="3" '
        f'stroke-linecap="round" class="a draw" style="--len:760;{d(.3)}animation-duration:1.8s;"/>'
    )
    for i, (year, title, sub) in enumerate(steps):
        x = 60 + i * 200
        t = .5 + i * .38
        last = i == len(steps) - 1
        body += f'<circle cx="{x}" cy="{y}" r="9" class="blue a pop" style="{d(t)}"/>'
        if last:
            body += f'<circle cx="{x}" cy="{y}" r="9" class="blue pulse" style="{d(t + .6)}"/>'
        anchor = "start"
        tx = x - 8
        body += (
            f'<g class="a rise" style="{d(t + .1)}">'
            f'<text x="{tx}" y="{y + 44}" text-anchor="{anchor}" class="w8 blue" style="font-size:22px">{year}</text>'
            f'<text x="{tx}" y="{y + 70}" text-anchor="{anchor}" class="w6" style="font-size:15px">{title}</text>'
            f'<text x="{tx}" y="{y + 92}" text-anchor="{anchor}" class="w4 muted" style="font-size:12.5px">{sub}</text></g>'
        )
    return svg(w, h, body, "Things I built: 2022 to 2026")


# ---------------------------------------------------------------- now
def now() -> str:
    w, h = 880, 110
    stack = ["Flutter", "FastAPI", "Spring Boot", "React", "PostgreSQL", "XRPL", "Azure"]
    body = f"""
<circle cx="48" cy="55" r="6" fill="#18a957" class="blink"/>
<circle cx="48" cy="55" r="6" fill="#18a957" class="pulse"/>
<text x="66" y="50" class="w8 a rise" style="font-size:17px;{d(.05)}">Now building</text>
<text x="66" y="72" class="w4 muted a rise" style="font-size:13px;{d(.15)}">Seoul, Korea</text>
"""
    x = 260
    for i, name in enumerate(stack):
        width = 18 + len(name) * 8.2
        body += (
            f'<g class="a pop" style="{d(.3 + i*.08)}">'
            f'<rect x="{x:.0f}" y="38" width="{width:.0f}" height="34" rx="17" class="soft"/>'
            f'<text x="{x + width/2:.0f}" y="60" text-anchor="middle" class="w6" style="font-size:13px">{name}</text></g>'
        )
        x += width + 8
    return svg(w, h, body, "Now building with " + ", ".join(stack))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    cards = {
        "hero.svg": hero(),
        "flow.svg": flow(),
        "tile-uniqdata.svg": tile("uniqdata", 0),
        "tile-uniqlab.svg": tile("uniqlab", 1),
        "tile-console.svg": tile("console", 2),
        "journey.svg": journey(),
        "now.svg": now(),
    }
    for name, content in cards.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content)//1024} KB")


if __name__ == "__main__":
    main()
