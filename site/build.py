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
from html import escape

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
}
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

@media (max-width: 720px) {
  .brand-text h1 { font-size: 18px; }
  nav.main-nav a { padding: 10px 12px; font-size: 12px; }
  .hero h2 { font-size: 26px; }
  article.article-body { padding: 22px; }
  footer.site-footer .row { grid-template-columns: 1fr; }
}
"""

NAV_ITEMS = [
    ("/", "Trang chủ"),
    ("/di-tich/", "Di tích"),
    ("/tham-quan/", "Tham quan"),
    ("/hoat-dong/", "Hoạt động"),
    ("/giao-duc-di-san/", "Giáo dục di sản"),
    ("/ve-chung-toi/", "Về chúng tôi"),
]

def page(title: str, body: str, current_path: str = "/", breadcrumbs=None) -> str:
    nav_html = "\n".join(
        f'<li><a href="{href}" class="{"active" if current_path.startswith(href) and href != "/" or (current_path == "/" and href == "/") else ""}">{label}</a></li>'
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
    <div class="brand-row">
      <div class="brand-mark">VM</div>
      <div class="brand-text">
        <h1>VĂN MIẾU – QUỐC TỬ GIÁM</h1>
        <p>Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám</p>
      </div>
    </div>
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
        <a href="/ve-chung-toi/">Về chúng tôi</a></p>
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
                 title_en=None, content_en=None, raw_text_vi=""):
        self.slug = slug
        self.title_vi = title_vi
        self.title_en = title_en
        self.content_vi = content_vi
        self.content_en = content_en
        self.images = images or []
        self.raw_text_vi = raw_text_vi

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
    return Article(
        slug=slugify(strip_lead_num(folder.name)),
        title_vi=title,
        content_vi=html,
        images=img_paths,
        raw_text_vi=raw,
    )

def article_from_file(docx: Path, img_subdir: str, title_override=None):
    title = title_override or strip_lead_num(docx.stem)
    raw = docx_to_text(docx)
    html = text_to_html(raw)
    imgs = collect_images(docx.parent)
    img_paths = [copy_image(im, img_subdir) for im in imgs]
    return Article(
        slug=slugify(title),
        title_vi=title,
        content_vi=html,
        images=img_paths,
        raw_text_vi=raw,
    )

def get_lead_num(name: str):
    m = re.match(r"^\s*(\d+)", name)
    return int(m.group(1)) if m else 999

# ---------- Build pages ----------

def render_article(art: Article, breadcrumbs):
    body_parts = [art.content_vi]
    if art.images:
        gallery = '\n'.join(
            f'<a href="{img}"><img src="{thumb_for(img)}" loading="lazy" alt=""></a>'
            for img in art.images
        )
        body_parts.append(f'<h3>Hình ảnh</h3><div class="gallery">{gallery}</div>')

    en_section = ""
    if art.content_en:
        en_section = f"""
<details style="margin-top:30px;background:var(--cream);padding:18px 22px;border:1px solid var(--line);">
<summary style="cursor:pointer;font-weight:600;color:var(--brick-dark);">English version</summary>
<h2 style="margin-top:14px;color:var(--brick-dark);">{escape(art.title_en or art.title_vi)}</h2>
{art.content_en}
</details>
"""

    body = f"""
<article class="article-body">
<h1>{escape(art.title_vi)}</h1>
{"".join(body_parts)}
{en_section}
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
def is_image_folder(name: str) -> bool: return _norm(name) in SKIP_NAMES
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

def merge_bilingual(vn_dir, en_dir, img_subdir: str):
    """Merge VN articles with EN articles by leading number, then by sequence."""
    def list_article_dirs(d):
        if not d:
            return []
        return sorted([p for p in d.iterdir() if p.is_dir()],
                      key=lambda p: (get_lead_num(p.name), p.name))

    def list_loose_docx(d):
        """Loose .docx files directly inside d (not in a subfolder)."""
        if not d:
            return []
        return sorted(
            [p for p in d.iterdir()
             if p.is_file() and p.suffix.lower() == ".docx" and not p.name.startswith("~")],
            key=lambda p: (get_lead_num(p.name), p.name),
        )

    vn_items = list_article_dirs(vn_dir)
    en_items = list_article_dirs(en_dir)

    # Match by leading number when available
    en_by_num = {}
    en_unmatched = []
    for e in en_items:
        n = get_lead_num(e.name)
        if n != 999 and n not in en_by_num:
            en_by_num[n] = e
        else:
            en_unmatched.append(e)

    articles = []
    used_unmatched = 0

    for vn in vn_items:
        # Recurse: vn folder might itself have nested articles (e.g. "2. Tư nghiep Chu Van An")
        sub = collect_articles_recursive(vn, img_subdir)
        if not sub:
            continue

        # If the vn folder is a single-article leaf (returned 1 article from itself)
        if len(sub) == 1 and has_own_docx(vn):
            art = sub[0]
            n = get_lead_num(vn.name)
            en_match = en_by_num.get(n)
            if not en_match and used_unmatched < len(en_unmatched):
                en_match = en_unmatched[used_unmatched]
                used_unmatched += 1
            attach_en(art, en_match, img_subdir)
            articles.append(art)
        else:
            # Hub folder with multiple sub-articles — append all, no EN merging at this level
            articles.extend(sub)

    # Loose .docx files directly in vn_dir (not wrapped in a folder)
    for docx in list_loose_docx(vn_dir):
        art = article_from_file(docx, img_subdir)
        articles.append(art)

    # Add unmatched VN-side EN articles as standalone (rare)
    if not vn_items and en_items:
        for en in en_items:
            sub = collect_articles_recursive(en, img_subdir)
            articles.extend(sub)

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

def build_tham_quan():
    src = ROOT / "Trang 2 Thăm quan"
    articles = []
    for f in sorted(src.iterdir()):
        if f.is_file() and f.suffix.lower() == ".docx":
            art = article_from_file(f, "tham-quan")
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
            n = sub.name.lower()
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
        gallery = "\n".join(
            f'<a href="{img}"><img src="{thumb_for(img)}" loading="lazy" alt=""></a>'
            for img in p["images"]
        )
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

# ---------- Main ----------

def main():
    print("== Build VMQTG site ==")
    # Reset
    for sub in ("di-tich", "tham-quan", "hoat-dong", "giao-duc-di-san", "ve-chung-toi"):
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
    print("Done. Output in:", SITE)

if __name__ == "__main__":
    main()
