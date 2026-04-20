#!/usr/bin/env python3
"""Build static site from VMQTG source data.

Set env BASE_PATH=/repo-name to deploy under a GitHub Pages project subpath.
Default is "" (root deployment, e.g. Vercel / Netlify / Cloudflare Pages /
username.github.io repo).
"""
import json
import os
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path
from html import escape, unescape

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(__file__).resolve().parent
ASSETS = SITE / "assets"
IMG_DIR = ASSETS / "images"

BASE_PATH = os.environ.get("BASE_PATH", "").rstrip("/")  # e.g. "/vmqtg-old-site"

def url(path: str) -> str:
    """Prefix absolute path with BASE_PATH (no-op if empty)."""
    if not path.startswith("/"):
        return path
    return BASE_PATH + path

# ---------- helpers ----------

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s[:80] or "untitled"

def strip_lead_num(s: str) -> str:
    return re.sub(r"^\s*\d+[\.\s]+", "", s).strip()

def docx_to_text(path: Path) -> str:
    try:
        out = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        return out.stdout
    except Exception as e:
        return f"[Lỗi đọc file: {e}]"

def text_to_html(txt: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", txt) if p.strip()]
    out = []
    for p in paragraphs:
        # Detect headings (short, all caps or title case)
        if len(p) < 120 and (p.isupper() or p.endswith(":")) and "\n" not in p:
            out.append(f"<h3>{escape(p)}</h3>")
        else:
            # Replace single newlines with <br>
            html_p = escape(p).replace("\n", "<br>\n")
            out.append(f"<p>{html_p}</p>")
    return "\n".join(out)

def excerpt(txt: str, n: int = 180) -> str:
    txt = re.sub(r"\s+", " ", txt).strip()
    if len(txt) <= n:
        return txt
    return txt[:n].rsplit(" ", 1)[0] + "…"

def collect_images(folder: Path):
    """Find images in folder + any 'ảnh'/'anh' subfolder (case-insensitive, dedup'd)."""
    if not folder.exists():
        return []
    exts = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
    seen = set()
    imgs = []
    def add(p):
        key = p.resolve()
        if key in seen: return
        seen.add(key)
        imgs.append(p)
    for p in folder.iterdir():
        if p.is_file() and p.suffix.lower() in exts:
            add(p)
        elif p.is_dir() and is_image_folder(p.name):
            for q in p.iterdir():
                if q.is_file() and q.suffix.lower() in exts:
                    add(q)
    return sorted(imgs)

FULL_DIM = 1600
FULL_QUALITY = 82
THUMB_DIM = 640
THUMB_QUALITY = 72

def _sips(src: Path, dest: Path, dim: int, quality: int):
    subprocess.run(
        [
            "sips",
            "-Z", str(dim),
            "-s", "format", "jpeg",
            "-s", "formatOptions", str(quality),
            str(src), "--out", str(dest),
        ],
        capture_output=True, timeout=60, check=True,
    )

def copy_image(src: Path, dest_subdir: str) -> str:
    """Generate both full (<=1600px) and thumb (<=640px) JPG. Returns full URL.
    Thumb URL is derived by replacing '.jpg' with '-thumb.jpg'."""
    dest_dir = IMG_DIR / dest_subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    base_slug = slugify(src.stem)
    full = dest_dir / f"{base_slug}.jpg"
    thumb = dest_dir / f"{base_slug}-thumb.jpg"
    # cache by name
    if full.exists() and full.stat().st_size > 0 and thumb.exists() and thumb.stat().st_size > 0:
        return f"/assets/images/{dest_subdir}/{full.name}"
    try:
        if not (full.exists() and full.stat().st_size > 0):
            _sips(src, full, FULL_DIM, FULL_QUALITY)
        if not (thumb.exists() and thumb.stat().st_size > 0):
            _sips(src, thumb, THUMB_DIM, THUMB_QUALITY)
    except Exception:
        try:
            shutil.copy2(src, full.with_suffix(src.suffix.lower()))
            full = full.with_suffix(src.suffix.lower())
        except Exception:
            return ""
    return f"/assets/images/{dest_subdir}/{full.name}"

def thumb_for(url: str) -> str:
    """Given a full image URL, return the thumb variant URL."""
    if url.endswith(".jpg"):
        return url[:-4] + "-thumb.jpg"
    return url

# ---------- HTML template ----------

CSS = """
:root {
  --brick: #8b2e2e;
  --brick-dark: #5a1818;
  --gold: #c9a14a;
  --cream: #f5efe2;
  --ink: #2a221c;
  --paper: #fbf8f1;
  --muted: #6b5e52;
  --line: #d8cdb8;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Times New Roman", "Source Serif 4", Georgia, serif;
  background: var(--paper);
  color: var(--ink);
  line-height: 1.7;
  font-size: 17px;
}
a { color: var(--brick); text-decoration: none; }
a:hover { text-decoration: underline; }
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }

header.site-header {
  background: var(--brick-dark);
  color: var(--cream);
  border-bottom: 4px solid var(--gold);
}
.topbar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 0; font-size: 13px; border-bottom: 1px solid rgba(255,255,255,.15);
}
.topbar a { color: var(--cream); margin-left: 14px; }
.brand-row {
  display: flex; align-items: center; gap: 18px; padding: 18px 0;
  color: var(--cream); text-decoration: none;
}
a.brand-row:hover { text-decoration: none; }
a.brand-row:hover .brand-text h1 { color: var(--gold); }
.brand-mark {
  width: 64px; height: 64px; border: 2px solid var(--gold);
  border-radius: 50%; display:flex; align-items:center; justify-content:center;
  color: var(--gold); font-weight: 700; font-size: 22px;
}
.brand-text h1 { margin: 0; font-size: 22px; letter-spacing: .5px; }
.brand-text p { margin: 2px 0 0; font-size: 13px; opacity: .85; font-style: italic; }
nav.main-nav {
  background: var(--brick);
  border-top: 1px solid rgba(255,255,255,.1);
}
nav.main-nav ul {
  list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap;
}
nav.main-nav a {
  display: block; padding: 12px 18px; color: var(--cream);
  text-transform: uppercase; font-size: 13px; letter-spacing: .8px;
  border-right: 1px solid rgba(255,255,255,.1);
}
nav.main-nav a:hover, nav.main-nav a.active {
  background: var(--brick-dark); text-decoration: none;
}

.hero {
  position: relative; padding: 60px 0 50px;
  background: linear-gradient(rgba(90,24,24,.6), rgba(90,24,24,.55)),
    url('/assets/images/hero.jpg') center/cover;
  color: var(--cream); text-align: center;
}
.hero h2 { font-size: 36px; margin: 0 0 10px; letter-spacing: 1px; }
.hero p { font-size: 17px; max-width: 720px; margin: 0 auto; opacity: .95; }

.breadcrumbs {
  font-size: 13px; padding: 14px 0; color: var(--muted);
  border-bottom: 1px solid var(--line);
}
.breadcrumbs a { color: var(--muted); }
.breadcrumbs span.sep { margin: 0 8px; opacity: .6; }

main { padding: 32px 0 60px; }
h2.page-title {
  font-size: 28px; color: var(--brick-dark); margin: 0 0 6px;
  border-bottom: 2px solid var(--gold); padding-bottom: 8px; display: inline-block;
}
.page-sub { color: var(--muted); font-style: italic; margin: 4px 0 24px; }

.grid {
  display: grid; gap: 22px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}
.card {
  background: #fff; border: 1px solid var(--line);
  border-radius: 4px; overflow: hidden; display: flex; flex-direction: column;
  transition: box-shadow .2s, transform .2s;
}
.card:hover { box-shadow: 0 6px 24px rgba(90,24,24,.12); transform: translateY(-2px); }
.card .thumb {
  width: 100%; height: 170px; background: var(--cream) center/cover no-repeat;
  border-bottom: 1px solid var(--line);
}
.card .body { padding: 14px 16px 18px; flex: 1; display: flex; flex-direction: column; }
.card h3 { margin: 0 0 8px; font-size: 17px; color: var(--brick-dark); line-height: 1.35; }
.card p { margin: 0 0 12px; color: var(--muted); font-size: 14px; flex: 1; }
.card a.more {
  align-self: flex-start; font-size: 13px; color: var(--brick);
  border-bottom: 1px solid var(--gold); padding-bottom: 1px;
}

.section-list { list-style: none; padding: 0; margin: 0 0 40px; }
.section-list li {
  padding: 14px 0; border-bottom: 1px dotted var(--line);
}
.section-list li a {
  font-size: 17px; color: var(--brick-dark); font-weight: 600;
}
.section-list li .meta { display: block; font-size: 13px; color: var(--muted); margin-top: 2px; font-style: italic; }

article.article-body {
  background: #fff; padding: 36px 44px; border: 1px solid var(--line);
  border-radius: 4px; max-width: 820px; margin: 0 auto;
}
article.article-body h1 {
  font-size: 26px; color: var(--brick-dark); margin: 0 0 6px;
  border-bottom: 2px solid var(--gold); padding-bottom: 12px;
}
article.article-body p { margin: 0 0 14px; text-align: justify; }
article.article-body h3 {
  color: var(--brick-dark); font-size: 18px; margin-top: 28px; margin-bottom: 8px;
}
article.article-body img {
  max-width: 100%; height: auto; display: block; margin: 18px auto;
  border: 1px solid var(--line); padding: 4px; background: #fff;
}
article.article-body .gallery {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px; margin: 24px 0;
}
article.article-body .gallery a {
  display: block; overflow: hidden; border: 1px solid var(--line);
  background: var(--cream); cursor: zoom-in; position: relative;
}
article.article-body .gallery a::after {
  content: "⤢"; position: absolute; right: 6px; bottom: 4px;
  color: #fff; background: rgba(0,0,0,.55); padding: 2px 7px;
  border-radius: 2px; font-size: 12px; opacity: 0; transition: opacity .15s;
}
article.article-body .gallery a:hover::after { opacity: 1; }
article.article-body .gallery img {
  margin: 0; padding: 0; border: 0;
  width: 100%; height: 160px; object-fit: cover;
  display: block; transition: transform .3s;
}
article.article-body .gallery a:hover img { transform: scale(1.04); }
article.article-body .gallery .caption {
  display: block; font-size: 12px; color: var(--muted);
  padding: 6px 8px; line-height: 1.35; background: #fff;
  border-top: 1px solid var(--line);
}

/* Lightbox */
.lightbox {
  position: fixed; inset: 0; background: rgba(0,0,0,.92);
  display: none; align-items: center; justify-content: center;
  z-index: 1000; cursor: zoom-out; padding: 20px;
}
.lightbox.open { display: flex; }
.lightbox img {
  max-width: 100%; max-height: 100%;
  box-shadow: 0 0 60px rgba(255,255,255,.1);
}
.lightbox .close {
  position: absolute; top: 14px; right: 18px; color: #fff;
  font-size: 28px; cursor: pointer; line-height: 1; user-select: none;
  background: rgba(255,255,255,.1); width: 40px; height: 40px;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
}
.lightbox .nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  color: #fff; font-size: 40px; cursor: pointer; user-select: none;
  padding: 14px 20px; background: rgba(255,255,255,.08);
}
.lightbox .nav:hover { background: rgba(255,255,255,.2); }
.lightbox .prev { left: 12px; }
.lightbox .next { right: 12px; }
.lightbox .counter {
  position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
  color: #fff; font-size: 13px; background: rgba(0,0,0,.5);
  padding: 4px 12px; border-radius: 12px;
}

.lang-switch {
  margin: 20px 0 0; font-size: 13px;
}
.lang-switch a {
  display: inline-block; padding: 6px 12px; margin-right: 6px;
  border: 1px solid var(--line); background: #fff; color: var(--brick);
}
.lang-switch a.active { background: var(--brick); color: var(--cream); border-color: var(--brick); }

footer.site-footer {
  background: var(--brick-dark); color: var(--cream);
  padding: 30px 0; margin-top: 40px; font-size: 14px;
  border-top: 4px solid var(--gold);
}
footer.site-footer .row { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 30px; }
footer.site-footer h4 { color: var(--gold); margin: 0 0 10px; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
footer.site-footer a { color: var(--cream); }
footer.site-footer .copy { text-align: center; padding-top: 22px; margin-top: 22px; border-top: 1px solid rgba(255,255,255,.15); font-size: 13px; opacity: .8; }

/* Interactive sitemap */
.sm-toolbar {
  display: flex; gap: 10px; flex-wrap: wrap;
  margin: 18px 0 26px; padding: 14px 16px;
  background: var(--cream); border: 1px solid var(--line); border-radius: 4px;
}
.sm-search {
  flex: 1 1 260px; min-width: 180px;
  padding: 10px 12px; font: inherit;
  border: 1px solid var(--line); background: #fff; color: var(--ink);
  border-radius: 2px;
}
.sm-search:focus { outline: 2px solid var(--gold); outline-offset: -1px; border-color: var(--gold); }
.sm-btn {
  padding: 8px 14px; border: 1px solid var(--brick); background: #fff;
  color: var(--brick); font: inherit; font-size: 14px; cursor: pointer;
  letter-spacing: .3px; border-radius: 2px;
}
.sm-btn:hover { background: var(--brick); color: var(--cream); }
.sm-stats { color: var(--muted); font-size: 13px; font-style: italic; margin: -10px 0 16px; }
.sm-tree, .sm-tree ul { list-style: none; padding: 0; margin: 0; }
.sm-tree ul.sm-children {
  padding-left: 22px; margin-left: 10px;
  border-left: 1px dashed var(--line);
}
.sm-node { padding: 2px 0; }
.sm-row { display: flex; align-items: center; gap: 2px; }
.sm-toggle {
  width: 22px; height: 22px; border: none; background: transparent;
  cursor: pointer; color: var(--brick); font-size: 11px; line-height: 1;
  padding: 0; display: inline-flex; align-items: center; justify-content: center;
  transition: transform .15s; flex: 0 0 auto;
}
.sm-node.sm-open > .sm-row > .sm-toggle { transform: rotate(90deg); }
.sm-dot {
  display: inline-flex; width: 22px; justify-content: center;
  color: var(--muted); flex: 0 0 auto; font-size: 12px;
}
.sm-link {
  color: var(--ink); padding: 3px 8px; border-radius: 2px;
  flex: 1 1 auto; min-width: 0;
}
.sm-link[href]:hover { background: var(--cream); color: var(--brick); text-decoration: none; }
.sm-count {
  display: inline-block; margin-left: 8px; padding: 1px 9px;
  background: #fff; color: var(--muted); border: 1px solid var(--line);
  border-radius: 12px; font-size: 12px; font-style: italic; flex: 0 0 auto;
}
.sm-tree > .sm-node > .sm-row > .sm-link {
  font-weight: 700; color: var(--brick-dark); font-size: 18px;
  padding: 6px 10px;
}
.sm-tree > .sm-node { padding: 6px 0; border-bottom: 1px dotted var(--line); }
.sm-tree > .sm-node:last-child { border-bottom: none; }
.sm-node.sm-has-children > .sm-children { display: none; }
.sm-node.sm-open > .sm-children { display: block; }
.sm-node.sm-filtered-out { display: none; }
.sm-link mark { background: var(--gold); color: var(--ink); padding: 0 2px; border-radius: 2px; }
.sm-empty { padding: 20px; color: var(--muted); font-style: italic; text-align: center; }

@media (max-width: 720px) {
  .brand-text h1 { font-size: 18px; }
  nav.main-nav a { padding: 10px 12px; font-size: 12px; }
  .hero h2 { font-size: 26px; }
  article.article-body { padding: 22px; }
  footer.site-footer .row { grid-template-columns: 1fr; }
  .sm-tree > .sm-node > .sm-row > .sm-link { font-size: 16px; }
}
"""

NAV_ITEMS = [
    ("/di-tich/", "Di tích"),
    ("/tham-quan/", "Tham quan"),
    ("/hoat-dong/", "Hoạt động"),
    ("/giao-duc-di-san/", "Giáo dục di sản"),
    ("/ve-chung-toi/", "Về chúng tôi"),
]

def page(title: str, body: str, current_path: str = "/", breadcrumbs=None) -> str:
    nav_html = "\n".join(
        f'<li><a href="{href}" class="{"active" if current_path.startswith(href) else ""}">{label}</a></li>'
        for href, label in NAV_ITEMS
    )
    bc = ""
    if breadcrumbs:
        parts = []
        for href, label in breadcrumbs:
            if href:
                parts.append(f'<a href="{href}">{escape(label)}</a>')
            else:
                parts.append(f'<span>{escape(label)}</span>')
        bc = f'<div class="breadcrumbs"><div class="container">{("<span class=\"sep\">›</span>").join(parts)}</div></div>'

    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} — Văn Miếu Quốc Tử Giám</title>
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<header class="site-header">
  <div class="container">
    <div class="topbar">
      <span>Di tích Quốc gia đặc biệt</span>
      <span><a href="mailto:vanmieuqtg@hanoi.gov.vn">vanmieuqtg@hanoi.gov.vn</a> · ĐT: 024.3747.1322</span>
    </div>
    <a class="brand-row" href="/">
      <div class="brand-mark">VM</div>
      <div class="brand-text">
        <h1>VĂN MIẾU – QUỐC TỬ GIÁM</h1>
        <p>Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám</p>
      </div>
    </a>
  </div>
  <nav class="main-nav">
    <div class="container">
      <ul>{nav_html}</ul>
    </div>
  </nav>
</header>
{bc}
<main>
<div class="container">
{body}
</div>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="row">
      <div>
        <h4>Văn Miếu – Quốc Tử Giám</h4>
        <p>58 Phố Quốc Tử Giám, Phường Văn Miếu, Quận Đống Đa, Hà Nội<br>
        Điện thoại: 024.3747.1322 / 024.3211.5793<br>
        Website cũ — bản demo</p>
      </div>
      <div>
        <h4>Liên kết</h4>
        <p><a href="/di-tich/">Di tích</a><br>
        <a href="/tham-quan/">Tham quan</a><br>
        <a href="/hoat-dong/">Hoạt động</a></p>
      </div>
      <div>
        <h4>Thông tin</h4>
        <p><a href="/giao-duc-di-san/">Giáo dục di sản</a><br>
        <a href="/ve-chung-toi/">Về chúng tôi</a><br>
        <a href="/so-do-trang/">Sơ đồ trang</a></p>
      </div>
    </div>
    <div class="copy">© Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám</div>
  </div>
</footer>
<div class="lightbox" id="lb" aria-hidden="true">
  <span class="close" id="lb-close">×</span>
  <span class="nav prev" id="lb-prev">‹</span>
  <img id="lb-img" alt="">
  <span class="nav next" id="lb-next">›</span>
  <span class="counter" id="lb-counter"></span>
</div>
<script>
(function(){{
  var lb = document.getElementById('lb');
  var img = document.getElementById('lb-img');
  var counter = document.getElementById('lb-counter');
  var links = [];
  var idx = 0;
  function collect(){{
    links = Array.from(document.querySelectorAll('.gallery a[href]'));
  }}
  function open(i){{
    idx = (i + links.length) % links.length;
    img.src = links[idx].getAttribute('href');
    counter.textContent = (idx+1) + ' / ' + links.length;
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }}
  function close(){{
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    img.src = '';
    document.body.style.overflow = '';
  }}
  document.addEventListener('click', function(e){{
    var a = e.target.closest('.gallery a[href]');
    if (a) {{
      e.preventDefault();
      collect();
      open(links.indexOf(a));
    }}
  }});
  document.getElementById('lb-close').onclick = close;
  document.getElementById('lb-prev').onclick = function(e){{ e.stopPropagation(); open(idx-1); }};
  document.getElementById('lb-next').onclick = function(e){{ e.stopPropagation(); open(idx+1); }};
  lb.onclick = function(e){{ if (e.target === lb || e.target === img) close(); }};
  document.addEventListener('keydown', function(e){{
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') open(idx-1);
    else if (e.key === 'ArrowRight') open(idx+1);
  }});
}})();
</script>
</body></html>"""

_URL_ATTR_RE = re.compile(r'''((?:href|src)\s*=\s*["'])/(?!/)''')
_URL_CSS_RE = re.compile(r'''url\(\s*(['"]?)/(?!/)''')

def _apply_base_path(html: str) -> str:
    if not BASE_PATH:
        return html
    html = _URL_ATTR_RE.sub(lambda m: m.group(1) + BASE_PATH + "/", html)
    html = _URL_CSS_RE.sub(lambda m: f"url({m.group(1)}{BASE_PATH}/", html)
    return html

def write_page(path: Path, html: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_apply_base_path(html), encoding="utf-8")

# ---------- Article model ----------

class Article:
    def __init__(self, slug, title_vi, content_vi, images=None,
                 title_en=None, content_en=None, raw_text_vi="",
                 source_folder=None, captions=None, content_fr=None):
        self.slug = slug
        self.title_vi = title_vi
        self.title_en = title_en
        self.content_vi = content_vi
        self.content_en = content_en
        self.content_fr = content_fr
        self.images = images or []
        self.raw_text_vi = raw_text_vi
        self.source_folder = source_folder  # for cross-language matching
        self.captions = captions or {}      # {image_url: caption_text}

    def excerpt(self):
        return excerpt(self.raw_text_vi)

# ---------- Discovery ----------

def find_first_docx(folder: Path):
    for p in folder.iterdir():
        if p.is_file() and p.suffix.lower() == ".docx" and not p.name.startswith("~"):
            return p
    return None

def article_from_folder(folder: Path, img_subdir: str):
    docx = find_first_docx(folder)
    if not docx:
        return None
    title = strip_lead_num(folder.name)
    raw = docx_to_text(docx)
    html = text_to_html(raw)
    imgs = collect_images(folder)
    img_paths = [copy_image(im, img_subdir) for im in imgs]
    captions = parse_caption_doc(folder, img_paths)
    return Article(
        slug=slugify(strip_lead_num(folder.name)),
        title_vi=title,
        content_vi=html,
        images=img_paths,
        raw_text_vi=raw,
        source_folder=folder,
        captions=captions,
    )

def article_from_file(docx: Path, img_subdir: str, title_override=None):
    title = title_override or strip_lead_num(docx.stem)
    raw = docx_to_text(docx)
    html = text_to_html(raw)
    imgs = collect_images(docx.parent)
    img_paths = [copy_image(im, img_subdir) for im in imgs]
    captions = parse_caption_doc(docx.parent, img_paths)
    return Article(
        slug=slugify(title),
        title_vi=title,
        content_vi=html,
        images=img_paths,
        raw_text_vi=raw,
        source_folder=docx.parent,
        captions=captions,
    )

def parse_caption_doc(folder: Path, img_paths):
    """Look for 'Chú thích ảnh.docx' in folder/ảnh/ and extract per-image captions.
    Convention: lines starting with 'N.' or 'N ' map to N-th image (1-indexed)."""
    if not folder.exists() or not img_paths:
        return {}
    # Find caption doc
    caption_doc = None
    for sub in folder.iterdir():
        if sub.is_dir() and is_image_folder(sub.name):
            for f in sub.iterdir():
                if f.is_file() and f.suffix.lower() == ".docx" and "chú thích" in _norm(f.stem):
                    caption_doc = f
                    break
        if caption_doc: break
    if not caption_doc:
        return {}
    raw = docx_to_text(caption_doc)
    # Split by lines starting with "N." or "N " (numbered captions)
    captions = {}
    current_num = None
    current_text = []
    for line in raw.splitlines():
        m = re.match(r"^\s*(\d+)\s*[\.\):]\s*(.*)$", line)
        if m:
            if current_num is not None and current_text:
                captions[current_num] = " ".join(current_text).strip()
            current_num = int(m.group(1))
            current_text = [m.group(2).strip()] if m.group(2).strip() else []
        elif current_num is not None and line.strip():
            current_text.append(line.strip())
    if current_num is not None and current_text:
        captions[current_num] = " ".join(current_text).strip()
    # Map to image URL (by 1-indexed position)
    out = {}
    for i, url in enumerate(img_paths, start=1):
        if i in captions:
            out[url] = captions[i]
    return out

def get_lead_num(name: str):
    m = re.match(r"^\s*(\d+)", name)
    return int(m.group(1)) if m else 999

# ---------- Build pages ----------

def _img_anchor(img, captions):
    cap = captions.get(img, "") if captions else ""
    if cap:
        return (f'<a href="{img}" title="{escape(cap)}">'
                f'<img src="{thumb_for(img)}" loading="lazy" alt="{escape(cap)}">'
                f'<span class="caption">{escape(cap)}</span></a>')
    return f'<a href="{img}"><img src="{thumb_for(img)}" loading="lazy" alt=""></a>'

def render_article(art: Article, breadcrumbs):
    body_parts = [art.content_vi]
    if art.images:
        gallery = '\n'.join(_img_anchor(img, art.captions) for img in art.images)
        body_parts.append(f'<h3>Hình ảnh</h3><div class="gallery">{gallery}</div>')

    extra_lang = ""
    if art.content_en:
        extra_lang += f"""
<details style="margin-top:18px;background:var(--cream);padding:18px 22px;border:1px solid var(--line);">
<summary style="cursor:pointer;font-weight:600;color:var(--brick-dark);">English version</summary>
<h2 style="margin-top:14px;color:var(--brick-dark);">{escape(art.title_en or art.title_vi)}</h2>
{art.content_en}
</details>
"""
    if art.content_fr:
        extra_lang += f"""
<details style="margin-top:12px;background:var(--cream);padding:18px 22px;border:1px solid var(--line);">
<summary style="cursor:pointer;font-weight:600;color:var(--brick-dark);">Version française</summary>
{art.content_fr}
</details>
"""

    body = f"""
<article class="article-body">
<h1>{escape(art.title_vi)}</h1>
{"".join(body_parts)}
{extra_lang}
</article>
"""
    return body

def render_listing(title: str, intro: str, items, base_path: str):
    """items: list of (slug, title, excerpt, thumb)"""
    cards = []
    for slug, t, ex, thumb in items:
        thumb_style = f' style="background-image:url(\'{thumb}\')"' if thumb else ""
        cards.append(f"""
<a class="card" href="{base_path}{slug}/">
  <div class="thumb"{thumb_style}></div>
  <div class="body">
    <h3>{escape(t)}</h3>
    <p>{escape(ex)}</p>
    <span class="more">Xem chi tiết →</span>
  </div>
</a>""")
    return f"""
<h2 class="page-title">{escape(title)}</h2>
<p class="page-sub">{escape(intro)}</p>
<div class="grid">
{"".join(cards)}
</div>
"""

def render_section_index(title: str, intro: str, sections):
    """sections: list of (href, title, count)"""
    items = []
    for href, t, count, blurb in sections:
        items.append(f"""
<li>
  <a href="{href}">{escape(t)}</a>
  <span class="meta">{count} bài · {escape(blurb)}</span>
</li>""")
    return f"""
<h2 class="page-title">{escape(title)}</h2>
<p class="page-sub">{escape(intro)}</p>
<ul class="section-list">
{"".join(items)}
</ul>
"""

# ---------- Section definitions ----------

DI_TICH_SUBS = [
    ("kien-truc", "Kiến trúc", "Kiến trúc",
     "Tổng thể quần thể: Hồ Văn, Cổng Văn Miếu, Khuê Văn Các, vườn bia Tiến sĩ, Đại Thành Môn, Thái Học Đường…"),
    ("lich-su", "Lịch sử Văn Miếu – Quốc Tử Giám", "Lich su VM",
     "Lược sử di tích qua các triều đại Lý, Trần, Hồ, Lê sơ – Mạc, Lê Trung hưng và giai đoạn cận hiện đại."),
    ("bia-tien-si", "82 Bia Tiến sĩ", "82 bia Tiên sĩ",
     "Hệ thống 82 bia đá khắc tên các vị Tiến sĩ — Di sản tư liệu thế giới."),
    ("tuong-tho", "Hệ thống tượng thờ", "Hệ thống tượng thờ",
     "Tượng thờ Khổng Tử, các vị Thánh nho và các vị vua, Tế tửu Quốc Tử Giám."),
    ("danh-nhan", "Danh nhân & dòng họ", "Danh nhân và dòng họ",
     "Tiến sĩ, Tế tửu – Tư nghiệp, các dòng họ khoa bảng tiêu biểu."),
]

def build_di_tich():
    section_root = ROOT / "Trang 1 Trang di tich"
    sections = []

    for slug, title, src, blurb in DI_TICH_SUBS:
        src_path = section_root / src
        articles = collect_di_tich_subsection(src_path, f"di-tich/{slug}")
        # write subsection index
        items = []
        for art in articles:
            thumb = art.images[0] if art.images else ""
            items.append((art.slug, art.title_vi, art.excerpt(), thumb))
        body = render_listing(title, blurb, items, f"/di-tich/{slug}/")
        bc = [("/", "Trang chủ"), ("/di-tich/", "Di tích"), (None, title)]
        write_page(SITE / "di-tich" / slug / "index.html",
                   page(title, body, f"/di-tich/{slug}/", bc))
        # write each article
        for art in articles:
            abc = bc + [(None, art.title_vi)]
            write_page(SITE / "di-tich" / slug / art.slug / "index.html",
                       page(art.title_vi, render_article(art, abc), f"/di-tich/{slug}/", abc))

        sections.append((f"/di-tich/{slug}/", title, len(articles), blurb))

    body = render_section_index("Khu di tích Văn Miếu – Quốc Tử Giám",
                                "Khám phá lịch sử, kiến trúc, hệ thống bia tiến sĩ và những danh nhân gắn liền với di tích.",
                                sections)
    write_page(SITE / "di-tich" / "index.html",
               page("Di tích", body, "/di-tich/",
                    [("/", "Trang chủ"), (None, "Di tích")]))

def _norm(s: str) -> str:
    """Normalize unicode + lower + strip — fixes NFC/NFD mismatches on macOS."""
    return unicodedata.normalize("NFC", s).strip().lower()

VN_NAMES = {_norm(x) for x in ("Tiếng Việt", "Tieng Viet")}
EN_NAMES = {_norm(x) for x in ("Tiếng Anh", "Tieng Anh")}
SKIP_NAMES = {_norm(x) for x in ("Ảnh", "ảnh", "anh")}
WRAPPER_NAMES = {_norm(x) for x in ("Bài viết và ảnh",)}

def is_vn(name: str) -> bool: return _norm(name) in VN_NAMES
def is_en(name: str) -> bool: return _norm(name) in EN_NAMES
def is_image_folder(name: str) -> bool:
    n = _norm(name)
    if n in SKIP_NAMES:
        return True
    # custom variants like "ảnh Môi trường", "Ảnh Kiến trúc cổ lớp 7-12"
    return n.startswith("ảnh ") or n.startswith("anh ")
def is_wrapper(name: str) -> bool: return _norm(name) in WRAPPER_NAMES

def find_lang_split(folder: Path):
    """Return (vn_dir, en_dir) if folder contains direct VN/EN children, else (None, None)."""
    if not folder.exists():
        return None, None
    vn = en = None
    for c in folder.iterdir():
        if not c.is_dir():
            continue
        if is_vn(c.name): vn = c
        elif is_en(c.name): en = c
    return vn, en

def has_own_docx(folder: Path) -> bool:
    return find_first_docx(folder) is not None

def collect_articles_recursive(folder: Path, img_subdir: str):
    """
    Recursively collect articles from folder, handling bilingual splits.
    - 'Bài viết và ảnh' wrapper folders are unwrapped.
    - VN/EN sibling folders are merged into one bilingual article list.
    - Image-only folders (no docx anywhere inside) are skipped.
    Returns flat list of Article objects.
    """
    if not folder.exists():
        return []

    # Unwrap "Bài viết và ảnh"
    inner = folder
    for c in folder.iterdir():
        if c.is_dir() and is_wrapper(c.name):
            inner = c
            break

    vn_dir, en_dir = find_lang_split(inner)
    if vn_dir or en_dir:
        return merge_bilingual(vn_dir, en_dir, img_subdir)

    # No language split here; this folder may itself be an article or contain articles
    out = []

    # If this folder has a docx, treat folder as an article
    if has_own_docx(inner):
        art = article_from_folder(inner, img_subdir)
        if art:
            out.append(art)

    # Plus, recurse into subfolders that are not images
    for c in sorted([p for p in inner.iterdir() if p.is_dir()],
                    key=lambda p: (get_lead_num(p.name), p.name)):
        if is_image_folder(c.name):
            continue
        if c == vn_dir or c == en_dir:
            continue
        out.extend(collect_articles_recursive(c, img_subdir))
    return out

def _walk_leaf_dirs_with_docx(root: Path):
    """Walk root tree, yield every folder that directly contains a .docx file
    (skipping folders inside an image-folder ancestor)."""
    if not root or not root.exists():
        return
    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        if any(is_image_folder(parent.name) for parent in [p, *p.parents]):
            continue
        if has_own_docx(p):
            yield p

# Stop words that don't help cross-language topic matching (common fillers
# in both Vietnamese folder names and English titles).
_TOPIC_STOP = {
    "the", "of", "and", "a", "to", "in", "with", "for", "by",
    "va", "voi", "cua", "ve", "trong", "qua", "tai", "tu", "den",
    "bai", "viet", "anh", "ban", "mot", "nay", "do", "no",
    "hoc", "khoa", "thi", "danh", "nhan",  # too common in Tế tửu section
}

def _topic_tokens(name: str):
    """ASCII-fold and tokenize a folder name (after stripping lead num).
    Used for cross-language topic matching."""
    s = unicodedata.normalize("NFD", strip_lead_num(name))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "d").lower()
    return {t for t in re.split(r"[^a-z0-9]+", s) if t and t not in _TOPIC_STOP and len(t) > 1}

def folder_topics(folder: Path, lang_root: Path):
    """Union of topic tokens from every ancestor between lang_root and folder."""
    topics = set()
    cur = folder
    while cur and cur != lang_root:
        topics |= _topic_tokens(cur.name)
        cur = cur.parent
    return topics

def merge_bilingual(vn_dir, en_dir, img_subdir: str):
    """Merge VN articles with EN articles.

    Strategy:
      1. Build a flat index of EN leaf folders (any depth inside en_dir),
         keyed by lead number. This handles asymmetric nesting (e.g. when VN
         uses a 'Bài viết và ảnh' wrapper but EN doesn't, or when EN nests
         deeper under a person-name folder).
      2. Walk VN top items normally. For each resulting article, attach
         matching EN by lead number (if not already used).
    """
    def list_article_dirs(d):
        if not d:
            return []
        return sorted([p for p in d.iterdir() if p.is_dir()],
                      key=lambda p: (get_lead_num(p.name), p.name))

    def list_loose_docx(d):
        if not d:
            return []
        return sorted(
            [p for p in d.iterdir()
             if p.is_file() and p.suffix.lower() == ".docx" and not p.name.startswith("~")],
            key=lambda p: (get_lead_num(p.name), p.name),
        )

    # Flat EN index with topic context for cross-language matching.
    en_pool = []  # (lead_num, depth, folder, topic_set)
    for f in _walk_leaf_dirs_with_docx(en_dir):
        en_pool.append((get_lead_num(f.name), len(f.parts), f, folder_topics(f, en_dir)))
    en_pool.sort(key=lambda t: (t[0], t[1]))
    en_used = set()

    # Count EN folders per lead_num — only enforce topic match when there's
    # ambiguity (>1 EN with same num), otherwise the match is unambiguous.
    en_count_by_num = {}
    for lead, _, _, _ in en_pool:
        en_count_by_num[lead] = en_count_by_num.get(lead, 0) + 1

    def take_en(num, vn_topics=None):
        """Find EN folder by lead num. When multiple EN share the same num,
        require ≥1 shared topic token to disambiguate (handles wrapper-structure
        cases like CVA). Single-candidate matches are accepted regardless of
        topic (handles simple sections like Tượng thờ where person names don't
        share tokens across languages, e.g. Khổng Tử / Confucius)."""
        candidates = [t for t in en_pool if t[0] == num and t[2] not in en_used]
        if not candidates:
            return None
        if len(candidates) == 1 or vn_topics is None:
            lead, depth, folder, _ = candidates[0]
            en_used.add(folder)
            return folder
        # Multiple candidates: prefer one with topic overlap
        for lead, depth, folder, en_topics in candidates:
            if en_topics and (en_topics & vn_topics):
                en_used.add(folder)
                return folder
        # No topic match — refuse rather than guess wrong
        return None

    vn_items = list_article_dirs(vn_dir)
    articles = []

    for vn in vn_items:
        sub = collect_articles_recursive(vn, img_subdir)
        if not sub:
            continue

        if len(sub) == 1 and has_own_docx(vn):
            art = sub[0]
            num = get_lead_num(vn.name)
            vn_topics = folder_topics(vn, vn_dir)
            en_folder = take_en(num, vn_topics) if num != 999 else None
            attach_en(art, en_folder, img_subdir)
            articles.append(art)
        else:
            # Hub: try to match each sub-article by its source folder's
            # lead num + topic context (so VN #4 inside Nguyễn Duy Thì doesn't
            # accidentally match EN #4 inside Chu Văn An).
            for art in sub:
                if art.source_folder:
                    num = get_lead_num(art.source_folder.name)
                    vn_topics = folder_topics(art.source_folder, vn_dir)
                    en_folder = take_en(num, vn_topics) if num != 999 else None
                    attach_en(art, en_folder, img_subdir)
            articles.extend(sub)

    # Loose .docx directly in vn_dir
    for docx in list_loose_docx(vn_dir):
        art = article_from_file(docx, img_subdir)
        num = get_lead_num(docx.stem)
        vn_topics = _topic_tokens(docx.stem)
        en_folder = take_en(num, vn_topics) if num != 999 else None
        attach_en(art, en_folder, img_subdir)
        articles.append(art)

    # Leftover EN folders not matched by num: surface as English-only articles
    # (don't FIFO-attach to VN — would pair wrong content). User sees them in
    # the section listing as separate EN entries.
    for lead, depth, en_folder, _topics in en_pool:
        if en_folder in en_used:
            continue
        art = article_from_folder(en_folder, img_subdir)
        if not art:
            continue
        # Mark as EN-only (no VN content)
        art.title_vi = strip_lead_num(en_folder.name)  # English title
        art.content_en = art.content_vi
        art.content_vi = '<p style="color:var(--muted);font-style:italic;">Bản tiếng Việt chưa có. Xem phiên bản tiếng Anh dưới đây.</p>'
        articles.append(art)

    return articles

def attach_en(art, en_folder, img_subdir):
    if not en_folder:
        return
    en_docx = find_first_docx(en_folder)
    if not en_docx:
        return
    en_raw = docx_to_text(en_docx)
    art.title_en = strip_lead_num(en_folder.name)
    art.content_en = text_to_html(en_raw)
    for im in collect_images(en_folder):
        ip = copy_image(im, img_subdir)
        if ip not in art.images:
            art.images.append(ip)

def collect_di_tich_subsection(src_path: Path, img_subdir: str):
    return collect_articles_recursive(src_path, img_subdir)

# ---------- Trang 2 (Tham quan) ----------

EN_MARKERS = (
    "REGULATIONS", "WELCOME TO", "Welcome to", "Dear Guests",
    "FOR THE SPECIAL", "VISITOR RULES", "GENERAL INFORMATION",
    "ENTRANCE FEE", "ENTRANCE FEES", "ADMISSION", "OPENING HOURS",
    "GUIDE SERVICE", "SERVICES",
)
FR_MARKERS = (
    "CENTRE DES", "RÈGLEMENT", "BIENVENUE", "Bienvenue",
    "Aux visiteurs", "Cher visiteur", "TARIF", "HORAIRES",
    "SERVICES TOURISTIQUES",
)

def split_languages(text: str):
    """Split a multilingual docx text into {lang: section_text} by heuristic markers.
    Default language is 'vi'. Returns dict like {'vi': ..., 'en': ..., 'fr': ...}.
    """
    lines = text.splitlines()
    boundaries = [(0, "vi")]  # (line_index, lang)
    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s: continue
        if any(m in s for m in EN_MARKERS) and boundaries[-1][1] != "en":
            boundaries.append((i, "en"))
        elif any(m in s for m in FR_MARKERS) and boundaries[-1][1] != "fr":
            boundaries.append((i, "fr"))
    result = {}
    for idx, (start, lang) in enumerate(boundaries):
        end = boundaries[idx+1][0] if idx+1 < len(boundaries) else len(lines)
        chunk = "\n".join(lines[start:end]).strip()
        if chunk:
            # Avoid overwriting if same lang appears twice (rare); keep first
            result.setdefault(lang, chunk)
    return result

def build_tham_quan():
    src = ROOT / "Trang 2 Thăm quan"
    articles = []
    for f in sorted(src.iterdir()):
        if f.is_file() and f.suffix.lower() == ".docx":
            raw = docx_to_text(f)
            langs = split_languages(raw)
            title = strip_lead_num(f.stem)
            imgs = collect_images(f.parent)
            img_paths = [copy_image(im, "tham-quan") for im in imgs]
            art = Article(
                slug=slugify(title),
                title_vi=title,
                content_vi=text_to_html(langs.get("vi", "")),
                images=img_paths,
                raw_text_vi=langs.get("vi", ""),
                source_folder=f.parent,
            )
            if "en" in langs:
                art.content_en = text_to_html(langs["en"])
            if "fr" in langs:
                # store as attribute on art for renderer
                art.content_fr = text_to_html(langs["fr"])
            articles.append(art)

    items = [(a.slug, a.title_vi, a.excerpt(), a.images[0] if a.images else "") for a in articles]
    body = render_listing("Thông tin tham quan",
                          "Hướng dẫn tham quan di tích Văn Miếu – Quốc Tử Giám: vé, nội quy, dịch vụ và tiện ích.",
                          items, "/tham-quan/")
    write_page(SITE / "tham-quan" / "index.html",
               page("Tham quan", body, "/tham-quan/",
                    [("/", "Trang chủ"), (None, "Tham quan")]))
    for art in articles:
        bc = [("/", "Trang chủ"), ("/tham-quan/", "Tham quan"), (None, art.title_vi)]
        write_page(SITE / "tham-quan" / art.slug / "index.html",
                   page(art.title_vi, render_article(art, bc), "/tham-quan/", bc))

# ---------- Trang 3 (Hoạt động) ----------

def build_hoat_dong():
    src = ROOT / "Trang 3 các hoạt động"
    articles = []
    for sub in sorted([p for p in src.iterdir() if p.is_dir()]):
        # each subdir could have docx + images
        for f in sorted(sub.iterdir()):
            if f.is_file() and f.suffix.lower() == ".docx":
                art = article_from_file(f, "hoat-dong")
                # use folder name as title if doc name is generic
                if "trưng bày" in f.stem.lower() or len(f.stem) < 12:
                    art.title_vi = sub.name
                    art.slug = slugify(sub.name)
                articles.append(art)
        # also pick caption docs in 'Ảnh' subfolder for image-only sections
        anh = sub / "Ảnh"
        if anh.exists():
            for f in sorted(anh.iterdir()):
                if f.is_file() and f.suffix.lower() == ".docx":
                    art = article_from_file(f, "hoat-dong", title_override=f"{sub.name} — Chú thích ảnh")
                    art.images = [copy_image(im, "hoat-dong") for im in collect_images(anh)]
                    articles.append(art)

    items = [(a.slug, a.title_vi, a.excerpt(), a.images[0] if a.images else "") for a in articles]
    body = render_listing("Các hoạt động",
                          "Hoạt động trưng bày, triển lãm thường xuyên tại di tích.",
                          items, "/hoat-dong/")
    write_page(SITE / "hoat-dong" / "index.html",
               page("Hoạt động", body, "/hoat-dong/",
                    [("/", "Trang chủ"), (None, "Hoạt động")]))
    for art in articles:
        bc = [("/", "Trang chủ"), ("/hoat-dong/", "Hoạt động"), (None, art.title_vi)]
        write_page(SITE / "hoat-dong" / art.slug / "index.html",
                   page(art.title_vi, render_article(art, bc), "/hoat-dong/", bc))

# ---------- Trang 4 (Giáo dục di sản) ----------

GIAO_DUC_LEVELS = [
    ("mam-non", "Mầm non", "Mầm non"),
    ("lop-1-3", "Lớp 1 – Lớp 3", "lớp 1-lớp 3"),
    ("lop-4-6", "Lớp 4 – Lớp 6", "lớp 4-lớp 6"),
    ("lop-7-12", "Lớp 7 – Lớp 12", "lớp 7-lớp 12"),
]

def build_giao_duc():
    src_root = ROOT / "trang 4 Trang Giáo dục di sản"
    levels = []

    for slug, label, dirname in GIAO_DUC_LEVELS:
        src = src_root / dirname
        if not src.exists():
            continue
        programs = []
        for prog_dir in sorted([p for p in src.iterdir() if p.is_dir()]):
            program = build_program(prog_dir, f"giao-duc-di-san/{slug}")
            if program:
                programs.append(program)

        # level index page
        items = [(p["slug"], p["title"], p["intro"], p["thumb"]) for p in programs]
        body = render_listing(label,
                              "Các chương trình giáo dục di sản dành cho cấp học này.",
                              items, f"/giao-duc-di-san/{slug}/")
        bc = [("/", "Trang chủ"), ("/giao-duc-di-san/", "Giáo dục di sản"), (None, label)]
        write_page(SITE / "giao-duc-di-san" / slug / "index.html",
                   page(label, body, f"/giao-duc-di-san/{slug}/", bc))

        # program detail pages
        for p in programs:
            pbc = bc + [(None, p["title"])]
            write_page(SITE / "giao-duc-di-san" / slug / p["slug"] / "index.html",
                       page(p["title"], render_program(p), f"/giao-duc-di-san/{slug}/", pbc))

        levels.append((f"/giao-duc-di-san/{slug}/", label, len(programs),
                       f"{len(programs)} chương trình giáo dục"))

    body = render_section_index("Giáo dục di sản",
                                "Các chương trình giáo dục dành cho mọi lứa tuổi từ mầm non đến THPT.",
                                levels)
    write_page(SITE / "giao-duc-di-san" / "index.html",
               page("Giáo dục di sản", body, "/giao-duc-di-san/",
                    [("/", "Trang chủ"), (None, "Giáo dục di sản")]))

def build_program(prog_dir: Path, img_subdir: str):
    """A program folder has multiple docx files representing different sections."""
    sections = []
    title = prog_dir.name

    images = [copy_image(im, img_subdir) for im in collect_images(prog_dir)]

    # Group: top-level docx, "Trước thăm quan/", "Sau thăm quan/"
    def docx_in(folder: Path, label_map=None):
        out = []
        if not folder.exists():
            return out
        for f in sorted(folder.iterdir()):
            if f.is_file() and f.suffix.lower() == ".docx" and not f.name.startswith("~"):
                lbl = strip_lead_num(f.stem)
                if label_map:
                    lbl = label_map.get(f.stem.lower(), lbl)
                raw = docx_to_text(f)
                out.append({"label": lbl, "html": text_to_html(raw), "raw": raw})
        return out

    main_docs = docx_in(prog_dir)
    pre_docs = []
    post_docs = []
    for sub in prog_dir.iterdir():
        if sub.is_dir():
            n = _norm(sub.name)  # NFC normalize for reliable Vietnamese matching
            if "trước" in n or "truoc" in n:
                pre_docs = docx_in(sub)
            elif "sau" in n:
                post_docs = docx_in(sub)

    if not (main_docs or pre_docs or post_docs):
        return None

    intro_raw = main_docs[0]["raw"] if main_docs else ""

    return {
        "slug": slugify(title),
        "title": title,
        "intro": excerpt(intro_raw, 160),
        "thumb": images[0] if images else "",
        "images": images,
        "main": main_docs,
        "pre": pre_docs,
        "post": post_docs,
    }

def render_program(p):
    parts = [f'<article class="article-body"><h1>{escape(p["title"])}</h1>']

    if p["main"]:
        for d in p["main"]:
            parts.append(f'<h3>{escape(d["label"])}</h3>{d["html"]}')

    if p["pre"]:
        parts.append('<h3 style="border-top:2px solid var(--gold);padding-top:18px;margin-top:30px;">Trước thăm quan</h3>')
        for d in p["pre"]:
            parts.append(f'<h3 style="font-size:16px;color:var(--muted);">{escape(d["label"])}</h3>{d["html"]}')

    if p["post"]:
        parts.append('<h3 style="border-top:2px solid var(--gold);padding-top:18px;margin-top:30px;">Sau thăm quan</h3>')
        for d in p["post"]:
            parts.append(f'<h3 style="font-size:16px;color:var(--muted);">{escape(d["label"])}</h3>{d["html"]}')

    if p["images"]:
        gallery = "\n".join(_img_anchor(img, p.get("captions", {})) for img in p["images"])
        parts.append(f'<h3>Hình ảnh chương trình</h3><div class="gallery">{gallery}</div>')

    parts.append("</article>")
    return "".join(parts)

# ---------- Trang 5 (Về chúng tôi) ----------

def build_ve_chung_toi():
    src = ROOT / "Trang 5 Về chúng tôi"
    articles = []
    for f in sorted(src.iterdir()):
        if f.is_file() and f.suffix.lower() == ".docx":
            art = article_from_file(f, "ve-chung-toi")
            articles.append(art)

    if articles:
        # single article pages
        body = render_article(articles[0], None) if len(articles) == 1 else None
        if body:
            write_page(SITE / "ve-chung-toi" / "index.html",
                       page("Về chúng tôi", body, "/ve-chung-toi/",
                            [("/", "Trang chủ"), (None, "Về chúng tôi")]))
        else:
            items = [(a.slug, a.title_vi, a.excerpt(), "") for a in articles]
            body = render_listing("Về chúng tôi", "", items, "/ve-chung-toi/")
            write_page(SITE / "ve-chung-toi" / "index.html",
                       page("Về chúng tôi", body, "/ve-chung-toi/",
                            [("/", "Trang chủ"), (None, "Về chúng tôi")]))
            for art in articles:
                bc = [("/", "Trang chủ"), ("/ve-chung-toi/", "Về chúng tôi"), (None, art.title_vi)]
                write_page(SITE / "ve-chung-toi" / art.slug / "index.html",
                           page(art.title_vi, render_article(art, bc), "/ve-chung-toi/", bc))

# ---------- Home ----------

def build_home():
    # Pick a hero image
    candidates = list(IMG_DIR.rglob("*.jpg"))
    if candidates:
        hero_src = candidates[0]
        # try to find a "good" one (full Văn Miếu shot)
        for c in candidates:
            n = c.name.lower()
            if "toan canh" in n or "toàn cảnh" in n or "khue van" in n or "1-" in n:
                hero_src = c
                break
        shutil.copy2(hero_src, IMG_DIR / "hero.jpg")

    body = """
<section class="hero" style="margin: -32px -24px 32px;">
  <div class="container">
    <h2>VĂN MIẾU – QUỐC TỬ GIÁM</h2>
    <p>Di tích Quốc gia đặc biệt — Trường đại học đầu tiên của Việt Nam, biểu tượng ngàn năm của đạo học và văn hiến Thăng Long – Hà Nội.</p>
  </div>
</section>

<h2 class="page-title">Khám phá di tích</h2>
<p class="page-sub">Toàn bộ nội dung được sắp xếp theo 5 chuyên mục chính.</p>

<div class="grid">
  <a class="card" href="/di-tich/">
    <div class="thumb" style="background:var(--brick);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:42px;">⛩</div>
    <div class="body"><h3>Di tích</h3><p>Lịch sử, 82 bia Tiến sĩ, hệ thống tượng thờ và danh nhân khoa bảng.</p><span class="more">Khám phá →</span></div>
  </a>
  <a class="card" href="/tham-quan/">
    <div class="thumb" style="background:var(--brick);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:42px;">🎫</div>
    <div class="body"><h3>Tham quan</h3><p>Vé, nội quy, dịch vụ và các tiện ích phục vụ khách tham quan.</p><span class="more">Xem chi tiết →</span></div>
  </a>
  <a class="card" href="/hoat-dong/">
    <div class="thumb" style="background:var(--brick);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:42px;">🏛</div>
    <div class="body"><h3>Hoạt động</h3><p>Trưng bày và triển lãm thường xuyên tại di tích.</p><span class="more">Xem chi tiết →</span></div>
  </a>
  <a class="card" href="/giao-duc-di-san/">
    <div class="thumb" style="background:var(--brick);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:42px;">📚</div>
    <div class="body"><h3>Giáo dục di sản</h3><p>Chương trình giáo dục dành cho mầm non đến THPT.</p><span class="more">Khám phá →</span></div>
  </a>
  <a class="card" href="/ve-chung-toi/">
    <div class="thumb" style="background:var(--brick);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:42px;">ℹ️</div>
    <div class="body"><h3>Về chúng tôi</h3><p>Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám.</p><span class="more">Tìm hiểu →</span></div>
  </a>
</div>
"""
    write_page(SITE / "index.html", page("Trang chủ", body, "/"))

# ---------- Site map ----------

_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
_SUFFIX_RE = re.compile(r"\s*[—–-]\s*Văn Miếu.*$")

SITEMAP_LABELS = {
    "di-tich": "Di tích",
    "tham-quan": "Tham quan",
    "hoat-dong": "Hoạt động",
    "giao-duc-di-san": "Giáo dục di sản",
    "ve-chung-toi": "Về chúng tôi",
    "kien-truc": "Kiến trúc",
    "lich-su": "Lịch sử",
    "bia-tien-si": "82 Bia Tiến sĩ",
    "tuong-tho": "Hệ thống tượng thờ",
    "danh-nhan": "Danh nhân & dòng họ",
    "mam-non": "Mầm non",
    "lop-1-3": "Lớp 1–3",
    "lop-4-6": "Lớp 4–6",
    "lop-7-12": "Lớp 7–12",
}

SITEMAP_TOP_ORDER = {
    "di-tich": 0,
    "tham-quan": 1,
    "hoat-dong": 2,
    "giao-duc-di-san": 3,
    "ve-chung-toi": 4,
}


def _extract_title(html_path: Path, fallback: str) -> str:
    try:
        txt = html_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return fallback
    m = _TITLE_RE.search(txt)
    if not m:
        return fallback
    t = unescape(m.group(1).strip())
    t = _SUFFIX_RE.sub("", t).strip()
    return t or fallback


def _collect_sitemap_pages():
    pages = []
    for html_file in SITE.rglob("index.html"):
        rel = html_file.parent.relative_to(SITE)
        parts = [] if str(rel) == "." else list(rel.parts)
        if not parts:
            continue
        if parts[0] == "so-do-trang":
            continue
        url_path = "/" + "/".join(parts) + "/"
        fallback = SITEMAP_LABELS.get(
            parts[-1], strip_lead_num(parts[-1].replace("-", " ")).title()
        )
        title = _extract_title(html_file, fallback)
        pages.append((parts, url_path, title))
    return pages


def _build_sitemap_tree(pages):
    root = {"title": "", "url": None, "children": {}}
    for parts, url_path, title in pages:
        node = root
        for i, part in enumerate(parts):
            child = node["children"].get(part)
            if child is None:
                child = {
                    "title": SITEMAP_LABELS.get(part, part.replace("-", " ").title()),
                    "url": None,
                    "children": {},
                }
                node["children"][part] = child
            if i == len(parts) - 1:
                child["title"] = title
                child["url"] = url_path
            node = child
    return root


def _count_sm_pages(node):
    total = 1 if node.get("url") else 0
    for c in node["children"].values():
        total += _count_sm_pages(c)
    return total


def _sort_sm_children(children_dict, is_root: bool):
    items = list(children_dict.items())
    if is_root:
        items.sort(key=lambda kv: SITEMAP_TOP_ORDER.get(kv[0], 99))
    else:
        items.sort(key=lambda kv: (kv[1]["url"] or "", kv[0]))
    return [v for _, v in items]


def _render_sm_node(node) -> str:
    has_children = bool(node["children"])
    cls = "sm-node" + (" sm-has-children" if has_children else "")
    page_count = sum(_count_sm_pages(c) for c in node["children"].values())
    toggle = (
        '<button class="sm-toggle" type="button" aria-label="Mở rộng">▸</button>'
        if has_children
        else '<span class="sm-dot" aria-hidden="true">·</span>'
    )
    title = escape(node["title"])
    if node["url"]:
        link = f'<a class="sm-link" href="{node["url"]}">{title}</a>'
    else:
        link = f'<span class="sm-link">{title}</span>'
    count_html = f'<span class="sm-count">{page_count}</span>' if page_count else ""
    children_html = ""
    if has_children:
        kids = _sort_sm_children(node["children"], is_root=False)
        children_html = (
            '<ul class="sm-children">'
            + "".join(_render_sm_node(c) for c in kids)
            + "</ul>"
        )
    return (
        f'<li class="{cls}"><div class="sm-row">{toggle}{link}{count_html}</div>'
        f"{children_html}</li>"
    )


SITEMAP_JS = r"""
(function(){
  var tree = document.querySelector('.sm-tree');
  if (!tree) return;
  var search = document.getElementById('sm-search');
  var expandBtn = document.getElementById('sm-expand');
  var collapseBtn = document.getElementById('sm-collapse');
  var stats = document.getElementById('sm-stats');

  function normalize(s){
    return (s || '').toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/đ/g, 'd').replace(/Đ/g, 'd');
  }

  tree.querySelectorAll('.sm-link').forEach(function(el){
    el.dataset.text = el.textContent;
  });

  function openNode(n, open){ n.classList.toggle('sm-open', open); }
  function setAll(open){
    tree.querySelectorAll('.sm-has-children').forEach(function(n){ openNode(n, open); });
  }

  tree.addEventListener('click', function(e){
    var btn = e.target.closest('.sm-toggle');
    if (!btn) return;
    e.preventDefault();
    var node = btn.closest('.sm-node');
    openNode(node, !node.classList.contains('sm-open'));
  });

  expandBtn.addEventListener('click', function(){ setAll(true); });
  collapseBtn.addEventListener('click', function(){
    setAll(false);
    tree.querySelectorAll(':scope > .sm-node.sm-has-children').forEach(function(n){ openNode(n, true); });
  });

  function clearHighlights(){
    tree.querySelectorAll('.sm-link').forEach(function(el){
      if (el.dataset.text) el.textContent = el.dataset.text;
    });
  }
  function highlight(el, q){
    var text = el.dataset.text || el.textContent;
    var idx = normalize(text).indexOf(q);
    if (idx < 0) { el.textContent = text; return; }
    el.innerHTML = '';
    el.appendChild(document.createTextNode(text.slice(0, idx)));
    var mark = document.createElement('mark');
    mark.textContent = text.slice(idx, idx + q.length);
    el.appendChild(mark);
    el.appendChild(document.createTextNode(text.slice(idx + q.length)));
  }

  function filter(){
    var q = normalize(search.value.trim());
    var nodes = tree.querySelectorAll('.sm-node');
    if (!q) {
      nodes.forEach(function(n){ n.classList.remove('sm-filtered-out'); });
      clearHighlights();
      if (stats) stats.textContent = '';
      return;
    }
    var matched = 0;
    nodes.forEach(function(n){
      var link = n.querySelector(':scope > .sm-row > .sm-link');
      var text = normalize(link.dataset.text || link.textContent);
      n._match = text.indexOf(q) !== -1;
      if (n._match) matched++;
    });
    function anyDescMatches(n){
      var kids = n.querySelectorAll(':scope > .sm-children > .sm-node');
      for (var i = 0; i < kids.length; i++){
        if (kids[i]._match || anyDescMatches(kids[i])) return true;
      }
      return false;
    }
    clearHighlights();
    nodes.forEach(function(n){
      var visible = n._match || anyDescMatches(n);
      n.classList.toggle('sm-filtered-out', !visible);
      if (visible && n.classList.contains('sm-has-children')) openNode(n, true);
      if (n._match) highlight(n.querySelector(':scope > .sm-row > .sm-link'), q);
    });
    if (stats) {
      stats.textContent = matched
        ? 'Tìm thấy ' + matched + ' kết quả cho \u201c' + search.value.trim() + '\u201d.'
        : 'Không có kết quả nào khớp với \u201c' + search.value.trim() + '\u201d.';
    }
  }

  search.addEventListener('input', filter);
  search.addEventListener('keydown', function(e){
    if (e.key === 'Escape') { search.value = ''; filter(); search.blur(); }
  });
  document.addEventListener('keydown', function(e){
    if (e.key === '/' && document.activeElement !== search
        && !/input|textarea/i.test(document.activeElement.tagName)) {
      e.preventDefault();
      search.focus();
    }
  });

  tree.querySelectorAll(':scope > .sm-node.sm-has-children').forEach(function(n){
    openNode(n, true);
  });
})();
"""


def build_site_map():
    pages = _collect_sitemap_pages()
    root = _build_sitemap_tree(pages)
    total = len(pages)
    top_nodes = _sort_sm_children(root["children"], is_root=True)
    tree_html = "".join(_render_sm_node(n) for n in top_nodes)

    body = f"""
<h2 class="page-title">Sơ đồ trang</h2>
<p class="page-sub">Toàn bộ {total} trang của website được sắp xếp theo cấu trúc phân cấp. Nhấn mũi tên để mở rộng, gõ vào ô tìm kiếm để lọc.</p>
<div class="sm-toolbar">
  <input type="search" id="sm-search" class="sm-search" placeholder="Tìm trong sơ đồ… (phím tắt: / )" autocomplete="off" aria-label="Tìm trong sơ đồ trang">
  <button class="sm-btn" id="sm-expand" type="button">Mở rộng tất cả</button>
  <button class="sm-btn" id="sm-collapse" type="button">Thu gọn</button>
</div>
<p class="sm-stats" id="sm-stats"></p>
<ul class="sm-tree">
{tree_html}
</ul>
<script>{SITEMAP_JS}</script>
"""
    write_page(
        SITE / "so-do-trang" / "index.html",
        page(
            "Sơ đồ trang",
            body,
            "/so-do-trang/",
            breadcrumbs=[("/", "Trang chủ"), (None, "Sơ đồ trang")],
        ),
    )
    print(f"  → {total} trang trong sơ đồ.")


# ---------- Main ----------

def main():
    print("== Build VMQTG site ==")
    # Reset
    for sub in (
        "di-tich",
        "tham-quan",
        "hoat-dong",
        "giao-duc-di-san",
        "ve-chung-toi",
        "so-do-trang",
    ):
        d = SITE / sub
        if d.exists():
            shutil.rmtree(d)
    if IMG_DIR.exists():
        shutil.rmtree(IMG_DIR)
    IMG_DIR.mkdir(parents=True)

    # Write CSS (apply base path for url() references)
    (ASSETS / "css" / "style.css").write_text(_apply_base_path(CSS), encoding="utf-8")

    print("Building Di tích…")
    build_di_tich()
    print("Building Tham quan…")
    build_tham_quan()
    print("Building Hoạt động…")
    build_hoat_dong()
    print("Building Giáo dục di sản…")
    build_giao_duc()
    print("Building Về chúng tôi…")
    build_ve_chung_toi()
    print("Building Home…")
    build_home()
    print("Building Sơ đồ trang…")
    build_site_map()
    print("Done. Output in:", SITE)

if __name__ == "__main__":
    main()
