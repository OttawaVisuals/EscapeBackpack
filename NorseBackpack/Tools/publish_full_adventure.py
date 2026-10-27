"""Copy Full_Adventure.html and every local file it links to into escapepack-site/design/norse-box/.

Relative paths are kept, so the page works unchanged. Run after build_full_adventure.py:
    python NorseBackpack/Tools/publish_full_adventure.py
Nothing is committed or pushed; the site repo does that.
"""
import os
import re
import shutil
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, ".."))
SITE = os.path.abspath(os.path.join(PROJECT, "..", "..", "escapepack-site"))
DEST = os.path.join(SITE, "design", "norse-box")
PAGE = os.path.join(PROJECT, "Full_Adventure.html")

SITE_HEAD = """<meta name="theme-color" content="#17372d">
<link rel="icon" type="image/png" href="../../assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Inter+Tight:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../site.css?v=4"><link rel="stylesheet" href="../../site-pages.css?v=4"><link rel="stylesheet" href="../../site-dark.css?v=4">
<script>try{var t=localStorage.getItem("ebp-theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}</script><script src="/theme.js?v=4" defer></script>"""
SITE_HEADER = """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="../../index.html" aria-label="Escape Backpack home"><span class="brand-mark" aria-hidden="true"></span><span>Escape<br><strong>Backpack</strong></span></a><nav class="main-nav" aria-label="Main navigation"><a href="../../index.html#adventures">Adventures</a><a href="../../index.html#how-it-works">How it works</a><a class="nav-help" href="../../help/">Hints &amp; reset ↗</a><a href="../../borrow.html">Borrow a backpack</a></nav></div></header>"""
SITE_FOOTER = """<footer class="site-footer"><div class="container footer-inner"><span>Escape Backpack · Ottawa</span><div><a href="../../index.html">Home</a><a href="../../help/">Hints &amp; reset</a><a href="../../feedback.html">Feedback</a></div></div></footer>"""
CRUMB = """<div class="breadcrumb"><a href="../index.html">Design studio</a><span aria-hidden="true"> / </span><span>Norse box</span></div>
<p class="eyebrow">Behind the scenes</p>
<div class="design-warning" role="note"><strong>Spoiler warning.</strong> Every puzzle, answer and solution of The Raven Inheritance is on this page. If you might play this backpack, turn back now.</div>"""
# Page colours and shapes mapped to the site's tokens (cream/forest, rust accents, square corners, serif headings).
OVERRIDE = """<style>
:root{--bg:var(--paper);--card:#fffaf1;--ink:#20392e;--mute:#566d5c;--rule:rgba(32,57,46,.17);--accent:#963f29;--rust:#a54c32;--spoil:#eae0d0;--btn:#17372d}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--card:#1f4639;--ink:#f7f1e6;--mute:#c5d3c8;--rule:rgba(247,241,230,.16);--accent:#e58f6e;--rust:#e58f6e;--spoil:#1b4033;--btn:#f7f1e6}}
:root[data-theme="dark"]{--card:#1f4639;--ink:#f7f1e6;--mute:#c5d3c8;--rule:rgba(247,241,230,.16);--accent:#e58f6e;--rust:#e58f6e;--spoil:#1b4033;--btn:#f7f1e6}
:root[data-theme="light"]{--bg:var(--paper);--card:#fffaf1;--ink:#20392e;--mute:#566d5c;--rule:rgba(32,57,46,.17);--accent:#963f29;--rust:#a54c32;--spoil:#eae0d0;--btn:#17372d}
body{font-family:var(--sans);background:var(--paper);color:var(--ink)}
.wrap{width:min(1900px,calc(100% - 48px));max-width:none}
main{padding-left:28px}
.bar{background:var(--paper)}
h1,h2,h3,.top h1{font-family:var(--serif);font-weight:400;letter-spacing:-.02em}
.top h1{font-size:clamp(34px,4.4vw,58px);line-height:1.1;white-space:normal}
h3.inside,h5{font-family:var(--mono);font-weight:500;letter-spacing:.14em}
h4{font-family:var(--sans);font-weight:700}
.env,.prop,.logic,.chip,.noimg,figure img,.tbl table,button,details.plan,.st,input{border-radius:0!important}
.env{background:var(--card)}
.env>header{align-items:flex-start}
.prop{background:var(--paper)}
.num{border-radius:0;background:var(--btn);color:var(--paper);font-family:var(--serif);font-weight:400}
button{border-color:var(--btn);color:var(--btn);font-weight:600}
button:hover,.tabs button[aria-selected=true]{background:var(--btn);color:var(--paper)}
.tabs button[aria-selected=true]{background:var(--btn);color:var(--paper)}
nav a:hover{background:var(--spoil)}
.wrap>nav{border-right:1px solid var(--rule)}
a{color:var(--accent);text-underline-offset:3px}
.site-header a,.site-footer a{color:inherit}
.site-header .main-nav{display:flex}
.breadcrumb{margin:30px 0 14px;font:500 12px var(--mono)}
.breadcrumb a{color:inherit}
.design-warning{margin:0 0 6px}
:root[data-theme="dark"] .design-warning,:root:not([data-theme="light"]) .design-warning{}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .design-warning{background:#3a2a24}}
:root[data-theme="dark"] .design-warning{background:#3a2a24}
.container.pagehead{padding-top:0}
@media(max-width:760px){.wrap{width:min(100% - 32px,520px)}main{padding-left:0}}
</style>"""


def restyle(html):
    """The published copy: the site's header, footer, fonts and colours around the same page."""
    nl = chr(10)
    html = html.replace("</head>", SITE_HEAD + nl + "</head>", 1)
    html = html.replace("</head>", OVERRIDE + "</head>", 1)
    # The page's own side nav must not catch the site header's <nav>.
    start, end = html.index("<style>"), html.index("</style>")
    css = re.sub(r"(?<![.\w>-])nav(?=[ {,:])", ".wrap>nav", html[start:end])
    html = html[:start] + css + html[end:]
    html = html.replace("<body>", "<body>" + nl + SITE_HEADER, 1)
    html = html.replace('<div class="wrap">', '<div class="wrap" id="main">', 1)
    html = html.replace('<div class="top">', CRUMB + nl + '<div class="top">', 1)
    html = html.replace("</body>", SITE_FOOTER + nl + "</body>", 1)
    return html


with open(PAGE, encoding="utf-8") as f:
    page = f.read()
refs = {unquote(m.split("#")[0].split("?")[0]) for m in re.findall(r'(?:src|href)="([^"]+)"', page)}
refs = sorted(r for r in refs if r and not re.match(r"^(https?:|mailto:|#|data:)", r))
if os.path.isdir(DEST):
    shutil.rmtree(DEST)
os.makedirs(DEST)
with open(os.path.join(DEST, "index.html"), "w", encoding="utf-8") as f:
    f.write(restyle(page))
copied = size = 0
for r in refs:
    src = os.path.join(PROJECT, r)
    if not os.path.isfile(src):
        print("missing:", r)
        continue
    dst = os.path.join(DEST, r)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    copied += 1
    size += os.path.getsize(src)
print(f"Copied index.html + {copied} files ({size / 1e6:.1f} MB) to {DEST}")
sys.exit(0)
