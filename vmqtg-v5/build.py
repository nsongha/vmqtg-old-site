#!/usr/bin/env python3
"""Văn Miếu – Quốc Tử Giám · Website V5
Sitemap: 5 sections + Mua vé CTA
Style: monochrome minimalist · wireframe with real data
"""
import os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD_IMGS = ROOT.parent / "site" / "assets" / "images"

# ─── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;-webkit-text-size-adjust:100%}
body{
  font-family:'Inter',ui-sans-serif,system-ui,-apple-system,sans-serif;
  background:#f7f7f5;
  color:#111110;
  line-height:1.65;
}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
ul,ol{list-style:none}

/* Container */
.container{max-width:1160px;margin:0 auto;padding:0 1.5rem}

/* ── HEADER ── */
.site-header{
  background:#111110;
  color:#fff;
  position:sticky;top:0;z-index:100;
  border-bottom:1px solid #222;
}
.header-inner{
  display:flex;align-items:center;gap:2rem;
  max-width:1160px;margin:0 auto;padding:0 1.5rem;
  height:58px;
}
.brand{display:flex;align-items:center;gap:.75rem;flex-shrink:0}
.brand-mark{
  width:34px;height:34px;
  border:1.5px solid rgba(255,255,255,.35);
  display:flex;align-items:center;justify-content:center;
  font-size:.72rem;font-weight:700;letter-spacing:.06em;
}
.brand-text{display:flex;flex-direction:column;gap:.05rem}
.brand-name{font-size:.82rem;font-weight:600;letter-spacing:.01em;line-height:1.2;color:#fff}
.brand-sub{font-size:.6rem;color:rgba(255,255,255,.4);letter-spacing:.06em;text-transform:uppercase}
.main-nav{display:flex;align-items:center;gap:.1rem;flex:1}
.main-nav a{
  font-size:.78rem;color:rgba(255,255,255,.6);
  padding:.38rem .7rem;font-weight:400;white-space:nowrap;
}
.main-nav a:hover,.main-nav a.active{color:#fff}
.nav-cta{
  margin-left:auto;
  border:1px solid rgba(255,255,255,.35)!important;
  padding:.32rem 1rem!important;
  color:#fff!important;font-size:.76rem!important;font-weight:500!important;
  flex-shrink:0;
}

/* ── BREADCRUMB ── */
.breadcrumb{
  background:#fff;border-bottom:1px solid #e4e4df;
  padding:.55rem 0;font-size:.73rem;color:#999;
}
.breadcrumb a{color:#666}
.breadcrumb .sep{margin:0 .4rem;color:#ccc}

/* ── HERO ── */
.hero{position:relative;overflow:hidden;background:#ddd}
.hero-img{
  width:100%;height:400px;object-fit:cover;display:block;
  filter:grayscale(100%) contrast(.85) brightness(1.08);
}
.hero-overlay{
  position:absolute;inset:0;
  background:linear-gradient(to top,rgba(0,0,0,.55) 0%,rgba(0,0,0,.1) 55%,transparent 100%);
}
.hero-content{
  position:absolute;bottom:0;left:0;right:0;
  padding:2.5rem 3rem;color:#fff;
  max-width:1220px;margin:0 auto;
}
.hero-title{
  font-size:2.1rem;font-weight:700;letter-spacing:-.02em;
  line-height:1.15;margin-bottom:.5rem;
}
.hero-sub{font-size:.95rem;opacity:.7;max-width:540px}

/* ── QUICK INFO BAR ── */
.quick-bar{background:#fff;border-bottom:1px solid #e4e4df}
.quick-bar-inner{
  display:flex;max-width:1160px;margin:0 auto;
  padding:0 1.5rem;
}
.quick-item{
  flex:1;padding:1.2rem 1rem;
  border-right:1px solid #e4e4df;
}
.quick-item:first-child{padding-left:0}
.quick-item:last-child{border-right:none}
.quick-label{
  font-size:.63rem;text-transform:uppercase;letter-spacing:.08em;
  color:#aaa;margin-bottom:.25rem;font-weight:500;
}
.quick-value{font-size:.88rem;font-weight:500;color:#111110}

/* ── PAGE HEADER ── */
.page-hd{
  background:#fff;border-bottom:1px solid #e4e4df;
  padding:2.5rem 0 2rem;
}
.page-title{
  font-size:1.9rem;font-weight:700;letter-spacing:-.02em;
  color:#111110;margin-bottom:.45rem;
}
.page-sub{font-size:.95rem;color:#777;max-width:620px;line-height:1.6}

/* ── CONTENT BODY ── */
.content{padding:2.5rem 0 4rem}
.content-inner{display:grid;grid-template-columns:1fr 280px;gap:3rem;align-items:start}
.content-main{}

/* ── GRID ── */
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}

/* ── CARD ── */
.card{
  display:block;background:#fff;
  border:1px solid #e4e4df;overflow:hidden;
}
.card:hover{border-color:#bbb}
.card-img{
  aspect-ratio:16/9;background:#ebebE8;overflow:hidden;
  position:relative;
}
.card-img img{
  width:100%;height:100%;object-fit:cover;
  filter:grayscale(100%) contrast(.85) brightness(1.06);
}
.card-img-ph{
  width:100%;height:100%;background:#e8e8e4;
  display:flex;align-items:center;justify-content:center;
}
.card-img-ph span{font-size:.65rem;color:#bbb;text-transform:uppercase;letter-spacing:.06em}
.card-body{padding:1.2rem}
.card-num{font-size:.65rem;color:#bbb;font-weight:600;letter-spacing:.06em;margin-bottom:.5rem}
.card-title{font-size:.92rem;font-weight:600;color:#111110;margin-bottom:.4rem;line-height:1.4}
.card-desc{font-size:.8rem;color:#777;line-height:1.6}
.card-arrow{display:inline-block;margin-top:.8rem;font-size:.75rem;color:#aaa}

/* ── SECTION LIST ── */
.section-list li{
  border-bottom:1px solid #e4e4df;padding:.9rem 0;
  display:flex;align-items:flex-start;gap:1rem;
}
.section-list li:first-child{border-top:1px solid #e4e4df}
.section-list a{font-weight:500;font-size:.9rem;color:#111110;flex-shrink:0}
.section-list .meta{font-size:.78rem;color:#999;line-height:1.5;text-align:right;flex:1}

/* ── ARTICLE ── */
.article{max-width:680px}
.article h1{font-size:1.7rem;font-weight:700;letter-spacing:-.02em;margin-bottom:1.5rem}
.article h2{font-size:1.2rem;font-weight:600;margin:2rem 0 .65rem;letter-spacing:-.01em}
.article h3{font-size:1rem;font-weight:600;margin:1.5rem 0 .45rem}
.article p{margin-bottom:.95rem;color:#444;line-height:1.8}
.article li{color:#444;line-height:1.7;margin-bottom:.4rem;padding-left:.25rem}
.article ul{list-style:disc;margin:.5rem 0 1rem 1.25rem}
.article ol{list-style:decimal;margin:.5rem 0 1rem 1.4rem}
.article strong{color:#111110;font-weight:600}

/* ── INFO TABLE ── */
.info-table{width:100%;border-collapse:collapse;margin:1.5rem 0}
.info-table th,.info-table td{
  padding:.75rem 1rem;text-align:left;
  border-bottom:1px solid #e4e4df;font-size:.875rem;
}
.info-table th{font-weight:600;background:#f7f7f5;width:40%}
.info-table td{color:#444}

/* ── SIDEBAR ── */
.sidebar{}
.sidebar-box{
  border:1px solid #e4e4df;background:#fff;
  padding:1.25rem;margin-bottom:1.25rem;
}
.sidebar-title{
  font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;
  color:#aaa;margin-bottom:.75rem;font-weight:600;
}
.sidebar-links li{padding:.4rem 0;border-bottom:1px solid #f0f0ec}
.sidebar-links li:last-child{border:none}
.sidebar-links a{font-size:.82rem;color:#444}
.sidebar-links a.active{font-weight:600;color:#111110}
.sidebar-cta{
  display:block;background:#111110;color:#fff;
  padding:1rem 1.25rem;text-align:center;
  font-size:.82rem;font-weight:500;
  margin-top:.75rem;
}

/* ── HOME SECTIONS OVERVIEW ── */
.sections-overview{padding:2.5rem 0 3.5rem}
.sections-title{font-size:1rem;font-weight:600;margin-bottom:1.25rem;color:#888;letter-spacing:.02em;text-transform:uppercase;font-size:.72rem;letter-spacing:.1em}
.sections-grid{
  display:grid;grid-template-columns:repeat(5,1fr);
  gap:1px;background:#e4e4df;
  border:1px solid #e4e4df;
}
.section-block{
  background:#fff;padding:1.75rem 1.5rem;
  display:flex;flex-direction:column;gap:.55rem;
  transition:none;
}
.section-block:hover{background:#fafaf8}
.section-block-num{
  font-size:.63rem;font-weight:700;color:#ccc;
  letter-spacing:.1em;
}
.section-block-name{font-size:.95rem;font-weight:600;color:#111110;line-height:1.35}
.section-block-sub{font-size:.75rem;color:#999;line-height:1.6}
.section-block-count{
  margin-top:auto;padding-top:.85rem;
  border-top:1px solid #f0f0ec;
  font-size:.68rem;color:#bbb;letter-spacing:.04em;
}

/* ── PRICE TABLE ── */
.price-table{border:1px solid #e4e4df;margin:1.5rem 0}
.price-row{
  display:flex;align-items:center;
  border-bottom:1px solid #e4e4df;
  padding:1rem 1.25rem;gap:1.5rem;
}
.price-row:last-child{border:none}
.price-cat{flex:1;font-size:.9rem;color:#444}
.price-val{
  font-size:1.1rem;font-weight:600;color:#111110;
  white-space:nowrap;
}
.price-note{font-size:.75rem;color:#999;margin-top:.15rem}

/* ── TIMELINE ── */
.timeline{position:relative;padding-left:1.5rem}
.timeline::before{
  content:'';position:absolute;left:.5rem;top:0;bottom:0;
  width:1px;background:#e4e4df;
}
.timeline-item{position:relative;margin-bottom:2rem}
.timeline-dot{
  position:absolute;left:-1.5rem;top:.4rem;
  width:8px;height:8px;background:#aaa;
}
.timeline-year{font-size:.72rem;color:#aaa;font-weight:600;letter-spacing:.06em;margin-bottom:.3rem}
.timeline-title{font-size:.95rem;font-weight:600;color:#111110;margin-bottom:.35rem}
.timeline-desc{font-size:.82rem;color:#666;line-height:1.65}

/* ── HUB PAGE CARD ── */
.hub-card{
  display:block;background:#fff;border:1px solid #e4e4df;
  padding:1.75rem;
}
.hub-card:hover{border-color:#bbb}
.hub-card-num{font-size:.65rem;color:#bbb;font-weight:700;letter-spacing:.07em;margin-bottom:.65rem}
.hub-card-title{font-size:1rem;font-weight:600;color:#111110;margin-bottom:.45rem;line-height:1.35}
.hub-card-desc{font-size:.8rem;color:#777;line-height:1.6}
.hub-card-link{display:inline-block;margin-top:1rem;font-size:.75rem;color:#999}

/* ── GALLERY ── */
.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#e4e4df;border:1px solid #e4e4df;margin:1.5rem 0}
.gallery-item{background:#fff;aspect-ratio:4/3;overflow:hidden}
.gallery-item img{width:100%;height:100%;object-fit:cover;filter:grayscale(100%) contrast(.85) brightness(1.06)}

/* ── FOOTER ── */
.site-footer{
  background:#111110;color:rgba(255,255,255,.55);
  padding:3rem 0 2rem;margin-top:0;
}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2.5rem;margin-bottom:2rem}
.footer-brand{font-size:.85rem;font-weight:600;color:#fff;margin-bottom:.6rem}
.footer-address{font-size:.77rem;line-height:1.85}
.footer-col-title{
  font-size:.63rem;text-transform:uppercase;letter-spacing:.08em;
  color:rgba(255,255,255,.3);margin-bottom:.85rem;font-weight:600;
}
.footer-links li{padding:.3rem 0}
.footer-links a{font-size:.78rem;color:rgba(255,255,255,.5)}
.footer-links a:hover{color:rgba(255,255,255,.8)}
.footer-copy{
  border-top:1px solid rgba(255,255,255,.08);
  padding-top:1.5rem;font-size:.72rem;color:rgba(255,255,255,.25);
}

/* ── UTILITY ── */
.label{
  display:inline-block;font-size:.65rem;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;
  border:1px solid #ddd;padding:.2rem .55rem;color:#888;
  margin-bottom:.75rem;
}
.section-sep{border:none;border-top:1px solid #e4e4df;margin:2.5rem 0}
.note{
  background:#f7f7f5;border-left:2px solid #ccc;
  padding:.9rem 1.1rem;font-size:.82rem;color:#666;
  line-height:1.65;margin:1.25rem 0;
}
"""

# ─── NAV ──────────────────────────────────────────────────────────────────────

NAV = [
    ("Tham quan", "tham-quan/"),
    ("Về di tích", "ve-di-tich/"),
    ("Trưng bày, triển lãm", "trung-bay-trien-lam/"),
    ("Các hoạt động", "cac-hoat-dong/"),
    ("Dịch vụ", "dich-vu/"),
]

FOOTER_LINKS = {
    "Tham quan": [
        ("Giờ mở cửa", "tham-quan/gio-mo-cua/"),
        ("Chính sách giá", "tham-quan/chinh-sach-gia/"),
        ("Quy định & nội quy", "tham-quan/quy-dinh-noi-quy/"),
        ("Đường đến", "tham-quan/duong-den/"),
    ],
    "Di tích": [
        ("Lịch sử", "ve-di-tich/lich-su/"),
        ("Kiến trúc", "ve-di-tich/kien-truc/"),
        ("Danh nhân", "ve-di-tich/danh-nhan/"),
        ("Hệ thống tượng thờ", "ve-di-tich/he-thong-tuong-tho/"),
    ],
    "Dịch vụ": [
        ("Mua vé", "dich-vu/mua-ve/"),
        ("Audio guide", "dich-vu/audio-guide/"),
        ("Tour đêm", "dich-vu/tour-dem/"),
        ("Hướng dẫn viên", "dich-vu/huong-dan-vien/"),
    ],
}

# ─── TEMPLATE ─────────────────────────────────────────────────────────────────

def page(title, meta, section, crumbs, body, depth=0):
    b = "../" * depth
    nav_items = "".join(
        f'<a href="{b}{href}" class="{"active" if lbl == section else ""}">{lbl}</a>'
        for lbl, href in NAV
    )
    crumb_html = ""
    for i, (lbl, href) in enumerate(crumbs):
        if i: crumb_html += '<span class="sep">›</span>'
        if href and i < len(crumbs) - 1:
            crumb_html += f'<a href="{b}{href}">{lbl}</a>'
        else:
            crumb_html += f'<span>{lbl}</span>'

    footer_cols = ""
    for col_title, links in FOOTER_LINKS.items():
        items = "".join(f'<li><a href="{b}{href}">{lbl}</a></li>' for lbl, href in links)
        footer_cols += f"""
      <div>
        <p class="footer-col-title">{col_title}</p>
        <ul class="footer-links">{items}</ul>
      </div>"""

    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Văn Miếu Quốc Tử Giám</title>
<meta name="description" content="{meta}">
<link rel="stylesheet" href="{b}assets/css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{b}index.html">
      <span class="brand-mark">VM</span>
      <span class="brand-text">
        <span class="brand-name">Văn Miếu – Quốc Tử Giám</span>
        <span class="brand-sub">Di tích Quốc gia đặc biệt</span>
      </span>
    </a>
    <nav class="main-nav">
      {nav_items}
      <a href="{b}dich-vu/mua-ve/index.html" class="nav-cta">Mua vé</a>
    </nav>
  </div>
</header>
<nav class="breadcrumb"><div class="container">{crumb_html}</div></nav>
{body}
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <p class="footer-brand">Văn Miếu – Quốc Tử Giám</p>
        <p class="footer-address">
          58 Phố Quốc Tử Giám, Phường Văn Miếu<br>
          Quận Đống Đa, Hà Nội<br>
          Điện thoại: 024.3747.1322<br>
          Email: vanmieuqtg@hanoi.gov.vn
        </p>
      </div>
      {footer_cols}
    </div>
    <p class="footer-copy">© Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám</p>
  </div>
</footer>
</body>
</html>"""

def img_tag(rel_path, alt="", extra_style=""):
    src = f"assets/images/{rel_path}"
    return f'<img src="{src}" alt="{alt}" loading="lazy">'

def img_ph(label="Ảnh"):
    return f'<div class="card-img-ph"><span>{label}</span></div>'

def write(path: Path, html: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"  ✓ {path.relative_to(ROOT)}")

# ─── IMAGE COPY ───────────────────────────────────────────────────────────────

def copy_imgs():
    img_out = ROOT / "assets" / "images"
    img_out.mkdir(parents=True, exist_ok=True)
    pairs = [
        ("hero.jpg", "hero.jpg"),
        ("di-tich/lich-su/1-toan-canh-van-mieu-quoc-tu-giam-dau-the-ky-xx-copy.jpg", "lich-su/hero.jpg"),
        ("di-tich/lich-su/2-tu-tru-va-ho-van-phia-truoc-van-mieu-quoc-tu-giam.jpg",  "lich-su/ho-van.jpg"),
        ("di-tich/lich-su/12-bia-tien-si.jpg",                                        "lich-su/bia.jpg"),
        ("di-tich/lich-su/10-nha-bia-tien-si-ben-tay.jpg",                            "lich-su/nha-bia.jpg"),
        ("di-tich/lich-su/20-nha-ta-vu.jpg",                                          "lich-su/nha-ta-vu.jpg"),
        ("di-tich/kien-truc/cong-dai-thanh.jpg",   "kien-truc/cong-dai-thanh.jpg"),
        ("di-tich/kien-truc/cong-dai-trung-1.jpg", "kien-truc/cong-dai-trung.jpg"),
        ("di-tich/kien-truc/cong-dat-tai.jpg",     "kien-truc/cong-dat-tai.jpg"),
        ("di-tich/danh-nhan/1-nen-cu-cua-truong-giam-sau-khi-dien-khai-thanh-bi-pha-huy.jpg", "danh-nhan/hero.jpg"),
        ("hoat-dong/1-toan-canh-van-mieu-quoc-tu-giam-dau-the-ky-xx.jpg", "hoat-dong/toan-canh.jpg"),
        ("hoat-dong/10-du-khach-tham-quan-phong-trung-bay.jpg",            "hoat-dong/trung-bay.jpg"),
        ("hoat-dong/10-1.jpg", "hoat-dong/10-1.jpg"),
        ("hoat-dong/10-2.jpg", "hoat-dong/10-2.jpg"),
        ("hoat-dong/10-3.jpg", "hoat-dong/10-3.jpg"),
    ]
    for src_rel, dst_rel in pairs:
        src = OLD_IMGS / src_rel
        dst = img_out / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  img {dst_rel}")
        else:
            print(f"  skip (missing) {src_rel}")

# ─── PAGES ────────────────────────────────────────────────────────────────────

def build_home():
    sections = [
        ("01", "Tham quan", "Giờ mở cửa, vé, nội quy, sơ đồ và tiện ích.", "6 trang", "tham-quan/"),
        ("02", "Về di tích", "Lịch sử, kiến trúc, danh nhân và hệ thống tượng thờ.", "4 trang", "ve-di-tich/"),
        ("03", "Trưng bày, triển lãm", "Trưng bày cố định, chuyên đề và sự kiện đang diễn ra.", "3 trang", "trung-bay-trien-lam/"),
        ("04", "Các hoạt động", "Thư viện, không gian số, bia tiến sĩ, giáo dục di sản.", "4 trang", "cac-hoat-dong/"),
        ("05", "Dịch vụ", "Mua vé, audio guide, tour đêm, hướng dẫn viên và hàng lưu niệm.", "6 trang", "dich-vu/"),
    ]
    blocks = "".join(f"""
    <a href="{href}" class="section-block">
      <span class="section-block-num">{num}</span>
      <span class="section-block-name">{name}</span>
      <span class="section-block-sub">{desc}</span>
      <span class="section-block-count">{count}</span>
    </a>""" for num, name, desc, count, href in sections)

    body = f"""
<div class="hero">
  <img class="hero-img" src="assets/images/hero.jpg" alt="Toàn cảnh Văn Miếu – Quốc Tử Giám">
  <div class="hero-overlay"></div>
  <div class="hero-content container">
    <h1 class="hero-title">Văn Miếu – Quốc Tử Giám</h1>
    <p class="hero-sub">Di tích Quốc gia đặc biệt · Trường đại học đầu tiên của Việt Nam · 82 Bia Tiến sĩ — Di sản tư liệu UNESCO</p>
  </div>
</div>
<div class="quick-bar">
  <div class="quick-bar-inner">
    <div class="quick-item">
      <p class="quick-label">Giờ mở cửa</p>
      <p class="quick-value">07:30 – 18:00</p>
    </div>
    <div class="quick-item">
      <p class="quick-label">Địa chỉ</p>
      <p class="quick-value">58 Quốc Tử Giám, Đống Đa, Hà Nội</p>
    </div>
    <div class="quick-item">
      <p class="quick-label">Điện thoại</p>
      <p class="quick-value">024.3747.1322</p>
    </div>
    <div class="quick-item">
      <p class="quick-label">Giá vé</p>
      <p class="quick-value">30.000đ / người lớn</p>
    </div>
  </div>
</div>
<main>
<div class="container sections-overview">
  <p class="sections-title">Khám phá Văn Miếu – Quốc Tử Giám</p>
  <div class="sections-grid">{blocks}</div>
</div>
</main>"""
    return page("Trang chủ", "Di tích Quốc gia đặc biệt Văn Miếu – Quốc Tử Giám.", "", [("Trang chủ","")], body, 0)

# ── HUB helper ────────────────────────────────────────────────────────────────

def hub(section_label, section_key, title, sub, cards_data, depth, crumbs):
    cards = ""
    for i, (card_title, card_desc, card_href, card_img) in enumerate(cards_data, 1):
        img_html = (f'<div class="card-img"><img src="{"../"*depth}assets/images/{card_img}" alt="{card_title}" loading="lazy"></div>'
                    if card_img else f'<div class="card-img">{img_ph()}</div>')
        cards += f"""
    <a href="{card_href}" class="card">
      {img_html}
      <div class="card-body">
        <p class="card-num">{i:02d}</p>
        <h3 class="card-title">{card_title}</h3>
        <p class="card-desc">{card_desc}</p>
        <span class="card-arrow">Xem chi tiết →</span>
      </div>
    </a>"""
    body = f"""
<div class="page-hd"><div class="container">
  <h1 class="page-title">{title}</h1>
  <p class="page-sub">{sub}</p>
</div></div>
<div class="content"><div class="container">
  <div class="grid-3">{cards}
  </div>
</div></div>"""
    return page(title, sub, section_label, crumbs, body, depth)

# ── ARTICLE helper ─────────────────────────────────────────────────────────────

def article_page(section_label, title, sub, body_html, sidebar_links, active_link, crumbs, depth):
    sidebar_items = "".join(
        f'<li><a href="{"../"*depth}{href}" class="{"active" if href == active_link else ""}">{lbl}</a></li>'
        for lbl, href in sidebar_links
    )
    content = f"""
<div class="page-hd"><div class="container">
  <p class="label">{section_label}</p>
  <h1 class="page-title">{title}</h1>
  <p class="page-sub">{sub}</p>
</div></div>
<div class="content"><div class="container">
  <div class="content-inner">
    <div class="content-main">
      <div class="article">{body_html}</div>
    </div>
    <aside class="sidebar">
      <div class="sidebar-box">
        <p class="sidebar-title">Trong mục này</p>
        <ul class="sidebar-links">{sidebar_items}</ul>
      </div>
      <a href="{"../"*depth}dich-vu/mua-ve/index.html" class="sidebar-cta">Mua vé →</a>
    </aside>
  </div>
</div></div>"""
    return page(title, sub, section_label, crumbs, content, depth)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 · THAM QUAN
# ═══════════════════════════════════════════════════════════════════════════════

THAM_QUAN_SIDEBAR = [
    ("Giờ mở cửa",     "tham-quan/gio-mo-cua/index.html"),
    ("Chính sách giá", "tham-quan/chinh-sach-gia/index.html"),
    ("Quy định & nội quy", "tham-quan/quy-dinh-noi-quy/index.html"),
    ("Sơ đồ thăm quan","tham-quan/so-do/index.html"),
    ("Đường đến",      "tham-quan/duong-den/index.html"),
    ("Tiện ích",       "tham-quan/tien-ich/index.html"),
]

def build_tham_quan():
    cards = [
        ("Giờ mở cửa", "Mùa hè 07:30 – 18:00 · Mùa đông 08:00 – 17:00, mở cửa hằng ngày.", "gio-mo-cua/index.html", ""),
        ("Chính sách giá", "Người lớn 30.000đ · Học sinh/sinh viên 15.000đ · Trẻ em dưới 15 tuổi miễn phí.", "chinh-sach-gia/index.html", ""),
        ("Quy định & nội quy", "Các quy định khi tham quan di tích Quốc gia đặc biệt.", "quy-dinh-noi-quy/index.html", ""),
        ("Sơ đồ thăm quan", "Hướng dẫn tham quan 5 khu vực: từ Văn Miếu Môn đến khu Thái Học.", "so-do/index.html", ""),
        ("Đường đến", "58 Phố Quốc Tử Giám, Đống Đa. Hướng dẫn đi bộ, xe buýt và taxi.", "duong-den/index.html", ""),
        ("Tiện ích", "Bãi đỗ xe, café, nhà hàng và quầy đồ lưu niệm trong khuôn viên.", "tien-ich/index.html", ""),
    ]
    return hub("Tham quan", "tham-quan", "Thông tin tham quan",
               "Vé, giờ mở cửa, nội quy và các tiện ích tại Văn Miếu – Quốc Tử Giám.",
               cards, 1, [("Trang chủ","index.html"),("Tham quan","")])

def build_gio_mo_cua():
    body = """
<table class="info-table">
  <tr><th>Mùa hè (tháng 4 – 10)</th><td>07:30 – 18:00 (mở cửa hằng ngày)</td></tr>
  <tr><th>Mùa đông (tháng 11 – 3)</th><td>08:00 – 17:00 (mở cửa hằng ngày)</td></tr>
  <tr><th>Ngày lễ, Tết</th><td>Mở cửa bình thường — xem thông báo cụ thể</td></tr>
  <tr><th>Quầy bán vé đóng cửa</th><td>Trước giờ đóng cửa 30 phút</td></tr>
</table>
<div class="note">Thời gian thăm quan khuyến nghị: 1,5 – 2 giờ. Tham quan buổi sáng (trước 10:00) để tránh đông và có ánh sáng đẹp.</div>
<h2>Liên hệ</h2>
<p>Điện thoại: 024.3747.1322 &nbsp;·&nbsp; 024.3211.5793<br>
Email: vanmieuqtg@hanoi.gov.vn</p>"""
    return article_page("Tham quan", "Giờ mở cửa",
                        "Văn Miếu – Quốc Tử Giám mở cửa hằng ngày, bao gồm cuối tuần và ngày lễ.",
                        body, THAM_QUAN_SIDEBAR, "tham-quan/gio-mo-cua/index.html",
                        [("Trang chủ","index.html"),("Tham quan","tham-quan/index.html"),("Giờ mở cửa","")], 2)

def build_chinh_sach_gia():
    body = """
<div class="price-table">
  <div class="price-row">
    <div class="price-cat">
      <p>Người lớn</p>
      <p class="price-note">Từ 16 tuổi trở lên</p>
    </div>
    <p class="price-val">30.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat">
      <p>Học sinh, sinh viên</p>
      <p class="price-note">Có thẻ học sinh hoặc thẻ sinh viên</p>
    </div>
    <p class="price-val">15.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat">
      <p>Người cao tuổi</p>
      <p class="price-note">Từ 60 tuổi trở lên — có CMND/hộ chiếu</p>
    </div>
    <p class="price-val">15.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat">
      <p>Trẻ em</p>
      <p class="price-note">Dưới 15 tuổi</p>
    </div>
    <p class="price-val">Miễn phí</p>
  </div>
</div>
<h2>Đặt vé</h2>
<p>Vé được bán tại quầy bán vé tại cổng chính (58 Phố Quốc Tử Giám). Quầy đóng cửa trước giờ đóng cửa 30 phút.</p>
<h2>Miễn vé — đối tượng đặc biệt</h2>
<ul>
  <li>Người khuyết tật có giấy chứng nhận</li>
  <li>Người có công với cách mạng</li>
  <li>Đoàn khách ngoại giao, cơ quan nhà nước (liên hệ trước)</li>
</ul>"""
    return article_page("Tham quan", "Chính sách giá",
                        "Giá vé tham quan Văn Miếu – Quốc Tử Giám năm 2024.",
                        body, THAM_QUAN_SIDEBAR, "tham-quan/chinh-sach-gia/index.html",
                        [("Trang chủ","index.html"),("Tham quan","tham-quan/index.html"),("Chính sách giá","")], 2)

def build_quy_dinh():
    body = """
<p>Thực hiện Quy tắc ứng xử nơi công cộng do UBND Thành phố Hà Nội ban hành, khi tham quan di tích Quốc gia đặc biệt Văn Miếu – Quốc Tử Giám, đề nghị Quý khách thực hiện nghiêm túc các điều sau:</p>
<ol style="list-style:decimal;margin:1rem 0 1.5rem 1.25rem">
  <li>Quý khách vào tham quan di tích phải mua vé, xuất trình vé tại nơi soát vé.</li>
  <li>Nêu cao ý thức bảo vệ di tích, giữ gìn vệ sinh môi trường. Không nằm, ngồi, sờ vào hiện vật. Không viết, vẽ lên tượng thờ, bia đá, công trình kiến trúc. Không giẫm lên cỏ, không hái hoa, bẻ cành.</li>
  <li>Giữ gìn an ninh trật tự, tuân thủ quy định phòng chống cháy nổ. Không hút thuốc trong khuôn viên. Không mang vũ khí, chất độc, chất nổ, động vật sống vào di tích.</li>
  <li>Trang phục phù hợp, lịch sự. Không đội nón/mũ, mặc áo ngắn, quần đùi tại nơi thờ tự. Giữ yên tĩnh tại những nơi tôn nghiêm.</li>
  <li>Nghiêm cấm lợi dụng tự do tín ngưỡng để thực hiện hành vi mê tín dị đoan, cờ bạc, lừa đảo.</li>
  <li>Khách tham quan chịu trách nhiệm pháp lý đối với tổn thất gây ra theo quy định pháp luật.</li>
  <li>Bảo vệ di tích có quyền chấm dứt chương trình tham quan với khách vi phạm nội quy.</li>
  <li>Phát hiện hiện tượng tiêu cực, đề nghị thông báo: 024.3747.1322 / 024.3211.5793.</li>
</ol>
<div class="note">Kính chúc Quý khách một chuyến tham quan bổ ích và lý thú!</div>"""
    return article_page("Tham quan", "Quy định & nội quy",
                        "Nội quy tham quan di tích Quốc gia đặc biệt Văn Miếu – Quốc Tử Giám.",
                        body, THAM_QUAN_SIDEBAR, "tham-quan/quy-dinh-noi-quy/index.html",
                        [("Trang chủ","index.html"),("Tham quan","tham-quan/index.html"),("Quy định & nội quy","")], 2)

def build_so_do():
    body = """
<p>Khu di tích Văn Miếu – Quốc Tử Giám được chia thành 5 khu vực (tiền đình) từ cổng chính đến khu Thái Học phía sau:</p>
<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <p class="timeline-year">Khu 1</p>
    <p class="timeline-title">Cổng Văn Miếu đến Đại Trung Môn</p>
    <p class="timeline-desc">Khu tiền đình với hồ Văn phía trước và hai trụ biểu hai bên cổng chính.</p>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <p class="timeline-year">Khu 2</p>
    <p class="timeline-title">Đại Trung Môn đến Khuê Văn Các</p>
    <p class="timeline-desc">Vườn cây xanh với hai gác chuông và trống ở hai bên.</p>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <p class="timeline-year">Khu 3</p>
    <p class="timeline-title">Khuê Văn Các – Vườn bia Tiến sĩ</p>
    <p class="timeline-desc">Hai dãy nhà bia với 82 tấm bia đá ghi tên các Tiến sĩ — Di sản tư liệu UNESCO.</p>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <p class="timeline-year">Khu 4</p>
    <p class="timeline-title">Đại Thành Môn – Khu thờ tự chính</p>
    <p class="timeline-desc">Đại Bái Đường và Thượng Điện — nơi thờ Khổng Tử và Tứ Phối.</p>
  </div>
  <div class="timeline-item">
    <div class="timeline-dot"></div>
    <p class="timeline-year">Khu 5</p>
    <p class="timeline-title">Khu Thái Học</p>
    <p class="timeline-desc">Nhà Hậu Đường (trưng bày thường xuyên), Tiền Đường và nhà Đông Vũ – Tây Vũ.</p>
  </div>
</div>"""
    return article_page("Tham quan", "Sơ đồ thăm quan",
                        "Hướng dẫn tham quan 5 khu vực trong di tích Văn Miếu – Quốc Tử Giám.",
                        body, THAM_QUAN_SIDEBAR, "tham-quan/so-do/index.html",
                        [("Trang chủ","index.html"),("Tham quan","tham-quan/index.html"),("Sơ đồ thăm quan","")], 2)

def build_duong_den():
    body = """
<table class="info-table">
  <tr><th>Địa chỉ</th><td>58 Phố Quốc Tử Giám, Phường Văn Miếu, Quận Đống Đa, Hà Nội</td></tr>
  <tr><th>Google Maps</th><td>Tìm kiếm "Văn Miếu Quốc Tử Giám Hà Nội"</td></tr>
</table>
<h2>Các tuyến xe buýt</h2>
<ul>
  <li>Tuyến 02 — Bác Cổ đến Bến xe Mỹ Đình, dừng tại Văn Miếu</li>
  <li>Tuyến 23 — Kim Mã đến Đại học Bách Khoa, dừng tại Văn Miếu</li>
  <li>Tuyến 38 — Ga Hà Nội đến Văn Điển, dừng tại Văn Miếu</li>
</ul>
<h2>Đi bộ từ các điểm lân cận</h2>
<ul>
  <li>Hồ Hoàn Kiếm: ~3km, khoảng 35 phút đi bộ</li>
  <li>Ga Hà Nội: ~2km, khoảng 25 phút đi bộ</li>
  <li>Hồ Tây: ~2,5km theo đường Hoàng Hoa Thám</li>
</ul>
<h2>Taxi và xe ôm công nghệ</h2>
<p>Grab, Be, Xanh SM hoạt động tốt trong khu vực. Đặt xe đến "Văn Miếu Quốc Tử Giám" hoặc nhập địa chỉ 58 Quốc Tử Giám.</p>
<div class="note">Bãi đỗ xe oto tại phố Văn Miếu và bãi đỗ xe máy trong vườn Giám — xem mục Tiện ích để biết thêm.</div>"""
    return article_page("Tham quan", "Đường đến",
                        "Hướng dẫn đến Văn Miếu – Quốc Tử Giám bằng xe buýt, taxi và đi bộ.",
                        body, THAM_QUAN_SIDEBAR, "tham-quan/duong-den/index.html",
                        [("Trang chủ","index.html"),("Tham quan","tham-quan/index.html"),("Đường đến","")], 2)

def build_tien_ich():
    body = """
<h2>Bãi đỗ xe</h2>
<ul>
  <li>Bãi đỗ xe ô tô: Phố Văn Miếu (phía trước cổng chính)</li>
  <li>Bãi đỗ xe máy và xe đạp: Vườn Giám (trong khuôn viên)</li>
</ul>
<h2>Ăn uống và giải khát</h2>
<ul>
  <li>Café và quầy giải khát trong khuôn viên</li>
  <li>Hàng ăn nhẹ gần cổng ra vào</li>
  <li>Nhiều nhà hàng, quán cà phê trên phố Quốc Tử Giám và Văn Miếu xung quanh</li>
</ul>
<h2>Đồ lưu niệm</h2>
<ul>
  <li>Quầy đồ lưu niệm tại lối ra — sách, ấn phẩm, đồ thủ công mỹ nghệ</li>
  <li>Sản phẩm do Trung tâm HVVHKH Văn Miếu – Quốc Tử Giám sản xuất và phân phối</li>
</ul>
<h2>Tiện ích khác</h2>
<ul>
  <li>Nhà vệ sinh công cộng tại nhiều điểm trong khuôn viên</li>
  <li>Chỗ nghỉ, ghế đá trong vườn cây bóng mát</li>
  <li>Wifi miễn phí tại khu vực khuôn viên chính</li>
</ul>"""
    return article_page("Tham quan", "Tiện ích",
                        "Bãi đỗ xe, café, đồ lưu niệm và các tiện ích khác trong khuôn viên.",
                        body, THAM_QUAN_SIDEBAR, "tham-quan/tien-ich/index.html",
                        [("Trang chủ","index.html"),("Tham quan","tham-quan/index.html"),("Tiện ích","")], 2)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 · VỀ DI TÍCH
# ═══════════════════════════════════════════════════════════════════════════════

VE_DI_TICH_SIDEBAR = [
    ("Lịch sử",             "ve-di-tich/lich-su/index.html"),
    ("Kiến trúc",           "ve-di-tich/kien-truc/index.html"),
    ("Danh nhân",           "ve-di-tich/danh-nhan/index.html"),
    ("Hệ thống tượng thờ",  "ve-di-tich/he-thong-tuong-tho/index.html"),
]

def build_ve_di_tich():
    cards = [
        ("Lịch sử", "Từ thời Lý Thánh Tông (1070) qua các triều đại Lý, Trần, Hồ, Lê, Nguyễn đến nay.", "lich-su/index.html", "lich-su/hero.jpg"),
        ("Kiến trúc", "10 công trình kiến trúc tiêu biểu: Khuê Văn Các, vườn bia, Đại Thành Điện, khu Thái Học…", "kien-truc/index.html", "kien-truc/cong-dai-trung.jpg"),
        ("Danh nhân", "Các Tiến sĩ, Tế tửu – Tư nghiệp và những dòng họ khoa bảng tiêu biểu.", "danh-nhan/index.html", "danh-nhan/hero.jpg"),
        ("Hệ thống tượng thờ", "Tượng thờ Khổng Tử, Tứ Phối, các vị Thánh nho và các vua.", "he-thong-tuong-tho/index.html", ""),
    ]
    return hub("Về di tích", "ve-di-tich", "Khu di tích Văn Miếu – Quốc Tử Giám",
               "Khám phá lịch sử, kiến trúc, hệ thống bia tiến sĩ và những danh nhân gắn liền với di tích.",
               cards, 1, [("Trang chủ","index.html"),("Về di tích","")])

def build_lich_su():
    body = """
<p>Văn Miếu – Quốc Tử Giám là di tích lịch sử – văn hóa hơn 950 năm tuổi, gắn liền với lịch sử giáo dục Việt Nam thời phong kiến.</p>
<h2>Thời Lý, Trần, Hồ (1070 – 1428)</h2>
<p>Văn Miếu được lập dưới thời Lý Thánh Tông, năm Canh Tuất (1070) là nơi thờ Khổng Tử, Chu Công và Tứ Phối. Năm 1076, vua Lý Nhân Tông lập Quốc Tử Giám — trường đại học đầu tiên của Việt Nam — ngay trong khuôn viên Văn Miếu.</p>
<p>Thời Trần (1225–1400), Văn Miếu tiếp tục được chăm sóc và là trung tâm đào tạo Nho học. Thời Hồ (1400–1407), nhà nước vẫn duy trì các hoạt động của Quốc Tử Giám.</p>
<h2>Thời Lê sơ – Mạc (1428 – 1593)</h2>
<p>Sau khi đánh đuổi quân Minh (1428), triều Lê chính thức kiến lập và xây dựng lại Văn Miếu – Quốc Tử Giám quy mô hơn. Từ năm 1484, nhà Lê bắt đầu dựng bia Tiến sĩ — 82 bia đá được lập từ 1484 đến 1780, ghi danh 1.304 Tiến sĩ qua 82 kỳ thi Đình.</p>
<h2>Thời Lê Trung hưng (1593 – 1788)</h2>
<p>Thời Lê Trung hưng, Văn Miếu – Quốc Tử Giám tiếp tục được tu sửa và mở rộng. Năm 1645, khu kiến trúc đã đạt quy mô tương đối hoàn chỉnh. Khuê Văn Các được xây dựng năm 1805 dưới thời Nguyễn.</p>
<h2>Giai đoạn 1802 – 1945</h2>
<p>Dưới thời Nguyễn, Thăng Long không còn là Kinh đô. Quốc Tử Giám Hà Nội dần thu hẹp chức năng giáo dục. Năm 1946, sau Cách mạng, Văn Miếu trở thành di tích lịch sử được Nhà nước bảo tồn.</p>
<h2>Từ 1945 đến nay</h2>
<p>Văn Miếu – Quốc Tử Giám được xếp hạng Di tích lịch sử – văn hóa quốc gia năm 1962, và Di tích Quốc gia đặc biệt năm 2014. Năm 2010, 82 Bia Tiến sĩ được UNESCO công nhận là Di sản tư liệu thế giới.</p>"""
    return article_page("Về di tích", "Lịch sử Văn Miếu – Quốc Tử Giám",
                        "Lược sử di tích qua các triều đại từ Lý Thánh Tông (1070) đến nay.",
                        body, VE_DI_TICH_SIDEBAR, "ve-di-tich/lich-su/index.html",
                        [("Trang chủ","index.html"),("Về di tích","ve-di-tich/index.html"),("Lịch sử","")], 2)

def build_kien_truc():
    body = """
<p>Khu di tích Văn Miếu – Quốc Tử Giám trải dài theo trục Bắc – Nam, gồm 5 lớp sân với nhiều công trình kiến trúc tiêu biểu.</p>
<h2>Các công trình chính</h2>
<ul>
  <li><strong>Hồ Văn</strong> — Hồ nước lớn phía trước, có gò Kim Châu ở giữa với đình Phán Thuỷ.</li>
  <li><strong>Cổng Văn Miếu (Văn Miếu Môn)</strong> — Cổng tam quan 3 cửa, xây thời Lê, trùng tu thời Nguyễn.</li>
  <li><strong>Đại Trung Môn</strong> — Cổng thứ hai với 3 gian mái cong.</li>
  <li><strong>Khuê Văn Các</strong> — Gác vuông 8 mái, xây năm 1805, biểu tượng của Hà Nội. Tầng trên có 4 cửa tròn tượng trưng vầng sáng văn học.</li>
  <li><strong>Vườn bia Tiến sĩ</strong> — Hai dãy nhà bia với 82 tấm bia đá, dựng từ 1484–1780.</li>
  <li><strong>Đại Thành Môn</strong> — Cổng vào khu thờ chính, 3 cửa.</li>
  <li><strong>Đại Bái Đường</strong> — Nhà thờ chính, nơi thờ Khổng Tử và Tứ Phối.</li>
  <li><strong>Thượng Điện (Đại Thành Điện)</strong> — Điện thờ phía trong.</li>
  <li><strong>Khu Thái Học</strong> — Xây dựng lại năm 2000 trên nền trường Quốc Tử Giám xưa, gồm Tiền Đường, Hậu Đường và hai nhà Đông Vũ – Tây Vũ.</li>
  <li><strong>82 Bia Tiến sĩ</strong> — Di sản tư liệu UNESCO; 82 bia đá rùa khắc tên 1.304 Tiến sĩ.</li>
</ul>
<div class="gallery">
  <div class="gallery-item"><img src="../../assets/images/kien-truc/cong-dai-trung.jpg" alt="Đại Trung Môn" loading="lazy"></div>
  <div class="gallery-item"><img src="../../assets/images/kien-truc/cong-dai-thanh.jpg" alt="Đại Thành Môn" loading="lazy"></div>
  <div class="gallery-item"><img src="../../assets/images/kien-truc/cong-dat-tai.jpg" alt="Cổng Đạt Tài" loading="lazy"></div>
</div>"""
    return article_page("Về di tích", "Kiến trúc",
                        "10 công trình kiến trúc tiêu biểu trong khu di tích Văn Miếu – Quốc Tử Giám.",
                        body, VE_DI_TICH_SIDEBAR, "ve-di-tich/kien-truc/index.html",
                        [("Trang chủ","index.html"),("Về di tích","ve-di-tich/index.html"),("Kiến trúc","")], 2)

def build_danh_nhan():
    body = """
<p>Văn Miếu – Quốc Tử Giám gắn liền với nhiều danh nhân khoa bảng, Tế tửu – Tư nghiệp Quốc Tử Giám và các dòng họ khoa bảng tiêu biểu của Việt Nam.</p>
<h2>Tế tửu và Tư nghiệp Quốc Tử Giám</h2>
<p>Tế tửu là chức quan đứng đầu Quốc Tử Giám, phụ trách giáo dục quốc gia. Các Tế tửu nổi tiếng bao gồm Chu Văn An — người được thờ phụng tại Văn Miếu cùng Khổng Tử và Tứ Phối.</p>
<h2>Các dòng họ khoa bảng tiêu biểu</h2>
<ul>
  <li>Dòng họ Nguyễn Quán Nho (Thanh Hoá) — nhiều đời liên tiếp đỗ Tiến sĩ</li>
  <li>Dòng họ Lê Quý Đôn (Thái Bình) — bác học lớn thế kỷ 18</li>
  <li>Dòng họ Phan Huy (Hà Tĩnh) — nhiều nhà văn hoá, chính khách</li>
</ul>
<h2>Tiến sĩ tiêu biểu</h2>
<ul>
  <li><strong>Nguyễn Trãi</strong> — Anh hùng dân tộc, đại thi hào, đỗ Thái học sinh năm 1400</li>
  <li><strong>Lê Quý Đôn</strong> — Bác học lớn, đỗ Tiến sĩ năm 1752, tác giả hơn 40 bộ sách</li>
  <li><strong>Chu Văn An</strong> — Nhà giáo mẫu mực, Tư nghiệp Quốc Tử Giám thời Trần</li>
  <li><strong>Nguyễn Bỉnh Khiêm</strong> — Đỗ Trạng nguyên năm 1535, nhà tiên tri nổi tiếng</li>
</ul>
<p>Danh sách đầy đủ 1.304 Tiến sĩ được khắc trên 82 bia đá trong vườn bia — Di sản tư liệu UNESCO.</p>"""
    return article_page("Về di tích", "Danh nhân",
                        "Các Tiến sĩ, Tế tửu và dòng họ khoa bảng tiêu biểu gắn với Văn Miếu – Quốc Tử Giám.",
                        body, VE_DI_TICH_SIDEBAR, "ve-di-tich/danh-nhan/index.html",
                        [("Trang chủ","index.html"),("Về di tích","ve-di-tich/index.html"),("Danh nhân","")], 2)

def build_tuong_tho():
    body = """
<p>Hệ thống tượng thờ tại Văn Miếu – Quốc Tử Giám phản ánh hệ thống thờ phụng Nho giáo theo truyền thống Hán – Việt, được đặt trang trọng tại Đại Bái Đường và Thượng Điện.</p>
<h2>Tượng thờ tại Thượng Điện (Đại Thành Điện)</h2>
<ul>
  <li><strong>Khổng Tử</strong> — Người sáng lập Nho giáo, thờ ở vị trí trung tâm</li>
  <li><strong>Tứ Phối</strong> — Bốn học trò xuất sắc: Nhan Hồi, Tăng Sâm, Tử Tư, Mạnh Tử</li>
  <li><strong>Thập nhị triết</strong> — 12 vị Thánh nho tiêu biểu của Nho giáo</li>
</ul>
<h2>Tượng thờ tại Đại Bái Đường</h2>
<ul>
  <li>Tượng Chu Công Đán — người đặt nền móng lễ nhạc Nho giáo</li>
  <li>Hai bên bái đường thờ Thất thập nhị hiền (72 học trò Khổng Tử)</li>
</ul>
<h2>Khu Thái Học — Tiền Đường</h2>
<ul>
  <li>Tượng thờ ba vị vua có công với Văn Miếu: Lý Thánh Tông, Lý Nhân Tông, Lê Thánh Tông</li>
  <li>Tượng Tế tửu Chu Văn An — nhà giáo mẫu mực thời Trần</li>
</ul>
<div class="note">Quý khách vui lòng không chạm vào tượng thờ và mặc trang phục lịch sự khi vào khu thờ tự.</div>"""
    return article_page("Về di tích", "Hệ thống tượng thờ",
                        "Tượng thờ Khổng Tử, Tứ Phối, Thánh nho và các vị vua tại Văn Miếu – Quốc Tử Giám.",
                        body, VE_DI_TICH_SIDEBAR, "ve-di-tich/he-thong-tuong-tho/index.html",
                        [("Trang chủ","index.html"),("Về di tích","ve-di-tich/index.html"),("Hệ thống tượng thờ","")], 2)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 · TRƯNG BÀY, TRIỂN LÃM
# ═══════════════════════════════════════════════════════════════════════════════

TRUNG_BAY_SIDEBAR = [
    ("Trưng bày cố định",  "trung-bay-trien-lam/co-dinh/index.html"),
    ("Trưng bày chuyên đề","trung-bay-trien-lam/chuyen-de/index.html"),
    ("Sự kiện đang diễn ra","trung-bay-trien-lam/su-kien/index.html"),
]

def build_trung_bay_hub():
    cards = [
        ("Trưng bày cố định", "Khu trưng bày thường xuyên tại tầng 1 nhà Hậu Đường — lịch sử Văn Miếu và khoa cử Nho học.", "co-dinh/index.html", "hoat-dong/trung-bay.jpg"),
        ("Trưng bày chuyên đề", "Các triển lãm theo chuyên đề thay đổi theo từng thời điểm trong năm.", "chuyen-de/index.html", ""),
        ("Sự kiện đang diễn ra", "Lịch sự kiện, hội thảo và các hoạt động văn hóa tại Văn Miếu – Quốc Tử Giám.", "su-kien/index.html", "hoat-dong/10-1.jpg"),
    ]
    return hub("Trưng bày, triển lãm", "trung-bay-trien-lam", "Trưng bày, triển lãm",
               "Khu trưng bày cố định, triển lãm chuyên đề và các sự kiện văn hóa tại Văn Miếu.",
               cards, 1, [("Trang chủ","index.html"),("Trưng bày, triển lãm","")])

def build_trung_bay_co_dinh():
    body = """
<p>Khu trưng bày thường xuyên đặt tại tầng 1 nhà Hậu Đường, khu Thái Học. Không gian trưng bày giới thiệu khái quát lịch sử hình thành và phát triển của Văn Miếu – Quốc Tử Giám và lịch sử khoa cử Nho học Việt Nam.</p>
<h2>Nội dung trưng bày</h2>
<ul>
  <li>Lịch sử thành lập Văn Miếu và Quốc Tử Giám (1070 – nay)</li>
  <li>Hệ thống giáo dục Nho học và chế độ thi cử qua các triều đại</li>
  <li>82 Bia Tiến sĩ — bản dập, nội dung văn bia và ý nghĩa Di sản UNESCO</li>
  <li>Hiện vật khai quật tại khu Quốc Tử Giám — đồ gốm, vật liệu kiến trúc</li>
  <li>Sắc phong, văn bản Hán – Nôm gốc và bản phục dựng</li>
  <li>Văn phòng tứ bảo (bút, mực, nghiên, giấy) qua các thời kỳ</li>
</ul>
<div class="gallery">
  <div class="gallery-item"><img src="../../assets/images/hoat-dong/toan-canh.jpg" alt="Toàn cảnh khu trưng bày" loading="lazy"></div>
  <div class="gallery-item"><img src="../../assets/images/hoat-dong/trung-bay.jpg" alt="Phòng trưng bày" loading="lazy"></div>
  <div class="gallery-item"><img src="../../assets/images/hoat-dong/10-1.jpg" alt="Hiện vật trưng bày" loading="lazy"></div>
</div>
<h2>Thông tin tham quan</h2>
<table class="info-table">
  <tr><th>Vị trí</th><td>Tầng 1, Nhà Hậu Đường – Khu Thái Học</td></tr>
  <tr><th>Diện tích</th><td>Khoảng 800m²</td></tr>
  <tr><th>Vào cửa</th><td>Bao gồm trong vé tham quan di tích</td></tr>
</table>"""
    return article_page("Trưng bày, triển lãm", "Trưng bày cố định",
                        "Khu trưng bày thường xuyên về lịch sử Văn Miếu và khoa cử Nho học tại nhà Hậu Đường.",
                        body, TRUNG_BAY_SIDEBAR, "trung-bay-trien-lam/co-dinh/index.html",
                        [("Trang chủ","index.html"),("Trưng bày, triển lãm","trung-bay-trien-lam/index.html"),("Trưng bày cố định","")], 2)

def build_chuyen_de():
    body = """
<p>Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám tổ chức các triển lãm chuyên đề theo các chủ đề về di sản văn hóa, lịch sử, khảo cổ và nghệ thuật.</p>
<h2>Các chủ đề tiêu biểu</h2>
<ul>
  <li>Di sản Hán – Nôm và văn khắc bia đá Việt Nam</li>
  <li>Khảo cổ học Hà Nội — hiện vật và tư liệu</li>
  <li>Mỹ thuật truyền thống và đương đại</li>
  <li>Lịch sử giáo dục Việt Nam qua các thời kỳ</li>
</ul>
<div class="note">Lịch triển lãm chuyên đề thay đổi theo từng thời điểm. Liên hệ 024.3747.1322 để biết lịch triển lãm hiện tại.</div>
<h2>Hợp tác tổ chức triển lãm</h2>
<p>Các tổ chức, bảo tàng, cơ quan nghiên cứu và cá nhân có nhu cầu hợp tác tổ chức triển lãm tại Văn Miếu – Quốc Tử Giám, vui lòng liên hệ Phòng Truyền thông: 024.3747.1322.</p>"""
    return article_page("Trưng bày, triển lãm", "Trưng bày chuyên đề",
                        "Các triển lãm chuyên đề về di sản văn hóa, lịch sử và nghệ thuật.",
                        body, TRUNG_BAY_SIDEBAR, "trung-bay-trien-lam/chuyen-de/index.html",
                        [("Trang chủ","index.html"),("Trưng bày, triển lãm","trung-bay-trien-lam/index.html"),("Trưng bày chuyên đề","")], 2)

def build_su_kien():
    body = """
<p>Văn Miếu – Quốc Tử Giám là không gian tổ chức nhiều sự kiện văn hóa, lễ hội và hội thảo khoa học thường niên.</p>
<h2>Các sự kiện định kỳ</h2>
<ul>
  <li><strong>Tết Nguyên đán</strong> — Lễ khai bút đầu năm, dâng hương Khổng Tử</li>
  <li><strong>Ngày Thơ Việt Nam</strong> (Rằm tháng Giêng) — Hội thơ tại Khuê Văn Các</li>
  <li><strong>Ngày Di sản văn hóa Việt Nam</strong> (23/11) — Các hoạt động kỷ niệm</li>
  <li><strong>Hội nghị – Hội thảo khoa học</strong> — Về di sản Hán Nôm, lịch sử giáo dục</li>
</ul>
<h2>Lịch sự kiện hiện tại</h2>
<div class="note">Lịch sự kiện cụ thể được cập nhật theo từng tháng. Liên hệ 024.3747.1322 hoặc email vanmieuqtg@hanoi.gov.vn để biết thông tin sự kiện sắp diễn ra.</div>"""
    return article_page("Trưng bày, triển lãm", "Sự kiện đang diễn ra",
                        "Lịch sự kiện, hội thảo và hoạt động văn hóa tại Văn Miếu – Quốc Tử Giám.",
                        body, TRUNG_BAY_SIDEBAR, "trung-bay-trien-lam/su-kien/index.html",
                        [("Trang chủ","index.html"),("Trưng bày, triển lãm","trung-bay-trien-lam/index.html"),("Sự kiện","")], 2)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 · CÁC HOẠT ĐỘNG
# ═══════════════════════════════════════════════════════════════════════════════

HOAT_DONG_SIDEBAR = [
    ("Thư viện",                     "cac-hoat-dong/thu-vien/index.html"),
    ("Không gian trải nghiệm số",    "cac-hoat-dong/khong-gian-so/index.html"),
    ("Dòng thời gian bia tiến sĩ",   "cac-hoat-dong/dong-thoi-gian/index.html"),
    ("Giáo dục di sản",              "cac-hoat-dong/giao-duc-di-san/index.html"),
]

def build_hoat_dong_hub():
    cards = [
        ("Thư viện", "Thư viện Văn Miếu – Quốc Tử Giám lưu trữ sách và tài liệu về di sản văn hóa.", "thu-vien/index.html", ""),
        ("Không gian trải nghiệm số", "Tương tác với nội dung số về lịch sử và di sản Văn Miếu qua màn hình cảm ứng và AR.", "khong-gian-so/index.html", "hoat-dong/10-2.jpg"),
        ("Dòng thời gian bia tiến sĩ", "Khám phá 1.304 Tiến sĩ và 82 kỳ thi Đình qua 300 năm trên dòng thời gian tương tác.", "dong-thoi-gian/index.html", "lich-su/bia.jpg"),
        ("Giáo dục di sản", "Các chương trình giáo dục di sản dành cho học sinh từ mầm non đến THPT.", "giao-duc-di-san/index.html", "hoat-dong/10-3.jpg"),
    ]
    return hub("Các hoạt động", "cac-hoat-dong", "Các hoạt động",
               "Thư viện, không gian số, dòng thời gian bia tiến sĩ và chương trình giáo dục di sản.",
               cards, 1, [("Trang chủ","index.html"),("Các hoạt động","")])

def build_thu_vien():
    body = """
<p>Thư viện Văn Miếu – Quốc Tử Giám là nơi lưu trữ và phục vụ tài liệu về di sản văn hóa, lịch sử giáo dục và Nho học Việt Nam.</p>
<h2>Vốn tài liệu</h2>
<ul>
  <li>Sách về lịch sử, văn hóa và di sản Hà Nội</li>
  <li>Tài liệu nghiên cứu về Văn Miếu – Quốc Tử Giám</li>
  <li>Ấn phẩm Hán – Nôm và bản dịch</li>
  <li>Tạp chí và kỷ yếu hội thảo khoa học</li>
</ul>
<h2>Đối tượng phục vụ</h2>
<p>Nhà nghiên cứu, học sinh, sinh viên và người quan tâm đến di sản văn hóa. Phục vụ tại chỗ theo lịch làm việc hành chính.</p>
<h2>Liên hệ</h2>
<p>Điện thoại: 024.3747.1322<br>Thứ Hai đến Thứ Sáu: 08:00 – 16:30</p>"""
    return article_page("Các hoạt động", "Thư viện",
                        "Thư viện lưu trữ tài liệu về di sản văn hóa, Nho học và lịch sử Văn Miếu.",
                        body, HOAT_DONG_SIDEBAR, "cac-hoat-dong/thu-vien/index.html",
                        [("Trang chủ","index.html"),("Các hoạt động","cac-hoat-dong/index.html"),("Thư viện","")], 2)

def build_khong_gian_so():
    body = """
<p>Không gian trải nghiệm số tại Văn Miếu – Quốc Tử Giám sử dụng công nghệ hiện đại để đưa di sản 950 năm tuổi đến gần hơn với khách tham quan, đặc biệt là thế hệ trẻ.</p>
<h2>Nội dung trải nghiệm</h2>
<ul>
  <li>Màn hình cảm ứng tương tác về lịch sử Văn Miếu và hệ thống bia Tiến sĩ</li>
  <li>Thực tế tăng cường (AR) – tái hiện kiến trúc cổ và các hoạt động thi cử xưa</li>
  <li>Video tư liệu về di sản và quá trình bảo tồn</li>
  <li>Trải nghiệm viết chữ Hán – Nôm trên bảng số</li>
</ul>
<h2>Vị trí và giờ mở cửa</h2>
<table class="info-table">
  <tr><th>Vị trí</th><td>Khu Thái Học, nhà Đông Vũ</td></tr>
  <tr><th>Giờ mở cửa</th><td>Theo giờ tham quan di tích</td></tr>
  <tr><th>Chi phí</th><td>Bao gồm trong vé tham quan</td></tr>
</table>"""
    return article_page("Các hoạt động", "Không gian trải nghiệm số",
                        "Tương tác với lịch sử và di sản Văn Miếu qua công nghệ AR và màn hình cảm ứng.",
                        body, HOAT_DONG_SIDEBAR, "cac-hoat-dong/khong-gian-so/index.html",
                        [("Trang chủ","index.html"),("Các hoạt động","cac-hoat-dong/index.html"),("Không gian số","")], 2)

def build_dong_thoi_gian():
    body = """
<p>Dòng thời gian bia Tiến sĩ là hệ thống trực quan hóa 82 kỳ thi Đình và 1.304 vị Tiến sĩ trong suốt 300 năm (1442–1779) dưới các triều đại Lê sơ, Mạc, Lê Trung hưng.</p>
<h2>Về 82 Bia Tiến sĩ</h2>
<p>82 bia đá được dựng từ năm 1484 đến 1780, ghi lại tên, quê quán và chức vụ của 1.304 Tiến sĩ đỗ qua các kỳ thi Đình từ 1442 đến 1779. Năm 2010, UNESCO công nhận 82 Bia Tiến sĩ là Di sản tư liệu thế giới.</p>
<h2>Dòng thời gian tương tác</h2>
<p>Khách tham quan có thể tra cứu tên Tiến sĩ theo năm thi, quê quán và khoa thi thông qua hệ thống màn hình cảm ứng đặt trong vườn bia và khu Thái Học.</p>
<h2>Thống kê nổi bật</h2>
<table class="info-table">
  <tr><th>Số bia</th><td>82 tấm bia đá</td></tr>
  <tr><th>Giai đoạn</th><td>1442 – 1779 (337 năm)</td></tr>
  <tr><th>Số Tiến sĩ</th><td>1.304 người</td></tr>
  <tr><th>Công nhận UNESCO</th><td>Năm 2010 — Di sản tư liệu thế giới</td></tr>
</table>"""
    return article_page("Các hoạt động", "Dòng thời gian bia Tiến sĩ",
                        "Khám phá 1.304 Tiến sĩ qua 82 kỳ thi Đình — Di sản tư liệu UNESCO.",
                        body, HOAT_DONG_SIDEBAR, "cac-hoat-dong/dong-thoi-gian/index.html",
                        [("Trang chủ","index.html"),("Các hoạt động","cac-hoat-dong/index.html"),("Dòng thời gian","")], 2)

def build_giao_duc_di_san():
    body = """
<p>Chương trình giáo dục di sản của Văn Miếu – Quốc Tử Giám được thiết kế phù hợp với từng cấp học, giúp học sinh trải nghiệm và hiểu về di sản văn hóa dân tộc.</p>
<h2>Chương trình theo cấp học</h2>
<ul>
  <li><strong>Mầm non (3–5 tuổi)</strong> — Tham quan, nghe kể chuyện, vẽ và tô màu về di tích</li>
  <li><strong>Tiểu học lớp 1–3</strong> — Tìm hiểu lịch sử đơn giản, trò chơi dân gian, thực hành viết chữ</li>
  <li><strong>Tiểu học lớp 4–6</strong> — Tìm hiểu bia Tiến sĩ, thực hành in dập, kể chuyện lịch sử</li>
  <li><strong>THCS, THPT (lớp 7–12)</strong> — Nghiên cứu chuyên sâu, thuyết trình, hội thảo học sinh</li>
</ul>
<h2>Đặt chương trình</h2>
<table class="info-table">
  <tr><th>Liên hệ</th><td>0369.087.468 (Phòng Giáo dục – Truyền thông)</td></tr>
  <tr><th>Đặt trước</th><td>Tối thiểu 3 ngày làm việc</td></tr>
  <tr><th>Nhóm tối thiểu</th><td>15 học sinh</td></tr>
  <tr><th>Chi phí</th><td>Theo chương trình — liên hệ để báo giá</td></tr>
</table>"""
    return article_page("Các hoạt động", "Giáo dục di sản",
                        "Các chương trình giáo dục di sản cho học sinh từ mầm non đến THPT.",
                        body, HOAT_DONG_SIDEBAR, "cac-hoat-dong/giao-duc-di-san/index.html",
                        [("Trang chủ","index.html"),("Các hoạt động","cac-hoat-dong/index.html"),("Giáo dục di sản","")], 2)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 · DỊCH VỤ
# ═══════════════════════════════════════════════════════════════════════════════

DICH_VU_SIDEBAR = [
    ("Dịch vụ Hồ Văn",   "dich-vu/ho-van/index.html"),
    ("Mua vé",            "dich-vu/mua-ve/index.html"),
    ("Audio guide",       "dich-vu/audio-guide/index.html"),
    ("Hàng lưu niệm",     "dich-vu/hang-luu-niem/index.html"),
    ("Tour đêm",          "dich-vu/tour-dem/index.html"),
    ("Hướng dẫn viên",    "dich-vu/huong-dan-vien/index.html"),
]

def build_dich_vu_hub():
    cards = [
        ("Dịch vụ Hồ Văn", "Không gian tổ chức sự kiện, triển lãm và hoạt động văn hóa tại khu Hồ Văn.", "ho-van/index.html", "lich-su/ho-van.jpg"),
        ("Mua vé", "Giá vé và các hình thức mua vé tham quan Văn Miếu – Quốc Tử Giám.", "mua-ve/index.html", ""),
        ("Audio guide", "Thuyết minh tự động 8 ngôn ngữ — Việt, Anh, Pháp, Tây Ban Nha, Hàn, Nhật, Trung, Thái.", "audio-guide/index.html", ""),
        ("Hàng lưu niệm", "Sách, ấn phẩm, đồ thủ công mỹ nghệ và quà lưu niệm mang bản sắc Văn Miếu.", "hang-luu-niem/index.html", ""),
        ("Tour đêm", "Trải nghiệm Văn Miếu – Quốc Tử Giám dưới ánh đèn đêm với hướng dẫn viên chuyên nghiệp.", "tour-dem/index.html", "lich-su/nha-bia.jpg"),
        ("Hướng dẫn viên", "Dịch vụ hướng dẫn viên tiếng Việt, Anh, Pháp và Trung Quốc.", "huong-dan-vien/index.html", ""),
    ]
    return hub("Dịch vụ", "dich-vu", "Dịch vụ",
               "Mua vé, audio guide, tour đêm, hướng dẫn viên và hàng lưu niệm tại Văn Miếu – Quốc Tử Giám.",
               cards, 1, [("Trang chủ","index.html"),("Dịch vụ","")])

def build_mua_ve():
    body = """
<p>Vé tham quan được bán tại quầy bán vé tại cổng chính, 58 Phố Quốc Tử Giám.</p>
<div class="price-table">
  <div class="price-row">
    <div class="price-cat"><p>Người lớn</p><p class="price-note">Từ 16 tuổi</p></div>
    <p class="price-val">30.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat"><p>Học sinh, sinh viên</p><p class="price-note">Có thẻ</p></div>
    <p class="price-val">15.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat"><p>Người cao tuổi (60+)</p><p class="price-note">Có CMND/hộ chiếu</p></div>
    <p class="price-val">15.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat"><p>Trẻ em dưới 15 tuổi</p></div>
    <p class="price-val">Miễn phí</p>
  </div>
</div>
<div class="note">Quầy bán vé đóng cửa trước giờ đóng cửa di tích 30 phút.</div>
<h2>Vé đoàn và vé đặc biệt</h2>
<p>Đoàn từ 20 người trở lên vui lòng liên hệ trước: 024.3747.1322 để được hỗ trợ và thỏa thuận giá vé đoàn.</p>"""
    return article_page("Dịch vụ", "Mua vé",
                        "Giá vé và thông tin mua vé tham quan Văn Miếu – Quốc Tử Giám.",
                        body, DICH_VU_SIDEBAR, "dich-vu/mua-ve/index.html",
                        [("Trang chủ","index.html"),("Dịch vụ","dich-vu/index.html"),("Mua vé","")], 2)

def build_ho_van():
    body = """
<p>Khu vực Hồ Văn nằm phía trước Văn Miếu Môn, bao gồm hồ nước lớn và gò Kim Châu với đình Phán Thuỷ. Đây là không gian văn hóa đặc sắc dành cho các sự kiện ngoài trời.</p>
<h2>Các dịch vụ tổ chức sự kiện</h2>
<ul>
  <li>Tổ chức hội chợ, triển lãm ngoài trời</li>
  <li>Biểu diễn nghệ thuật truyền thống và đương đại</li>
  <li>Lễ hội văn hóa, sự kiện cộng đồng</li>
  <li>Gala dinner, tiệc tối tại không gian di sản</li>
</ul>
<h2>Liên hệ đặt dịch vụ</h2>
<table class="info-table">
  <tr><th>Điện thoại</th><td>024.3747.1322</td></tr>
  <tr><th>Email</th><td>vanmieuqtg@hanoi.gov.vn</td></tr>
  <tr><th>Gặp trực tiếp</th><td>Phòng Hành chính – Quản trị, 58 Quốc Tử Giám</td></tr>
</table>"""
    return article_page("Dịch vụ", "Dịch vụ Hồ Văn",
                        "Không gian tổ chức sự kiện và hoạt động văn hóa tại khu Hồ Văn.",
                        body, DICH_VU_SIDEBAR, "dich-vu/ho-van/index.html",
                        [("Trang chủ","index.html"),("Dịch vụ","dich-vu/index.html"),("Dịch vụ Hồ Văn","")], 2)

def build_audio_guide():
    body = """
<p>Thiết bị thuyết minh tự động giúp Quý khách tham quan theo tốc độ riêng với nội dung thuyết minh chuyên sâu tại từng điểm di tích.</p>
<h2>Ngôn ngữ</h2>
<p>Nội dung thuyết minh có sẵn bằng 8 ngôn ngữ:</p>
<ul>
  <li>Tiếng Việt</li>
  <li>Tiếng Anh</li>
  <li>Tiếng Pháp</li>
  <li>Tiếng Tây Ban Nha</li>
  <li>Tiếng Hàn Quốc</li>
  <li>Tiếng Nhật Bản</li>
  <li>Tiếng Trung Quốc</li>
  <li>Tiếng Thái Lan</li>
</ul>
<h2>Giá thuê thiết bị</h2>
<div class="price-table">
  <div class="price-row">
    <div class="price-cat"><p>Tiếng Việt</p></div>
    <p class="price-val">30.000đ</p>
  </div>
  <div class="price-row">
    <div class="price-cat"><p>Tiếng nước ngoài</p></div>
    <p class="price-val">50.000đ</p>
  </div>
</div>
<div class="note">Liên hệ cán bộ tại quầy bán vé để thuê thiết bị thuyết minh tự động.</div>"""
    return article_page("Dịch vụ", "Audio guide",
                        "Thuyết minh tự động 8 ngôn ngữ — Việt, Anh, Pháp, Tây Ban Nha, Hàn, Nhật, Trung, Thái.",
                        body, DICH_VU_SIDEBAR, "dich-vu/audio-guide/index.html",
                        [("Trang chủ","index.html"),("Dịch vụ","dich-vu/index.html"),("Audio guide","")], 2)

def build_hang_luu_niem():
    body = """
<p>Quầy hàng lưu niệm Văn Miếu – Quốc Tử Giám cung cấp các sản phẩm mang bản sắc văn hóa di tích.</p>
<h2>Các sản phẩm tiêu biểu</h2>
<ul>
  <li>Sách và ấn phẩm về Văn Miếu, di sản Hà Nội và Nho học</li>
  <li>Bản dập bia Tiến sĩ và phiên bản nghệ thuật</li>
  <li>Đồ gốm, đồ đồng phong cách truyền thống</li>
  <li>Quà tặng: bộ văn phòng phẩm phong cách cổ, tranh thêu, tranh sơn mài</li>
  <li>Áo dài và phụ kiện mang họa tiết Văn Miếu</li>
</ul>
<h2>Vị trí và giờ mở cửa</h2>
<table class="info-table">
  <tr><th>Vị trí</th><td>Lối ra chính và khu Thái Học</td></tr>
  <tr><th>Giờ mở cửa</th><td>Theo giờ tham quan di tích</td></tr>
</table>"""
    return article_page("Dịch vụ", "Hàng lưu niệm",
                        "Sách, ấn phẩm, đồ thủ công và quà lưu niệm mang bản sắc Văn Miếu – Quốc Tử Giám.",
                        body, DICH_VU_SIDEBAR, "dich-vu/hang-luu-niem/index.html",
                        [("Trang chủ","index.html"),("Dịch vụ","dich-vu/index.html"),("Hàng lưu niệm","")], 2)

def build_tour_dem():
    body = """
<p>Tour đêm Văn Miếu – Quốc Tử Giám mang đến trải nghiệm khám phá di tích dưới ánh đèn đêm độc đáo, kết hợp nghệ thuật ánh sáng và kể chuyện lịch sử.</p>
<h2>Nội dung tour</h2>
<ul>
  <li>Tham quan 5 khu vực của di tích trong ánh sáng nghệ thuật</li>
  <li>Hướng dẫn viên chuyên nghiệp kể chuyện lịch sử và truyền thuyết về Văn Miếu</li>
  <li>Biểu diễn nghệ thuật truyền thống tại Khuê Văn Các</li>
  <li>Trải nghiệm viết thư pháp dưới ánh nến</li>
</ul>
<h2>Thông tin tour</h2>
<table class="info-table">
  <tr><th>Thời gian</th><td>19:30 – 21:30 (Thứ Sáu, Thứ Bảy, Chủ nhật)</td></tr>
  <tr><th>Nhóm</th><td>Tối đa 30 người/tour</td></tr>
  <tr><th>Ngôn ngữ</th><td>Tiếng Việt; tiếng Anh theo yêu cầu</td></tr>
</table>
<div class="note">Đặt trước tối thiểu 2 ngày. Liên hệ: 024.3747.1322 hoặc vanmieuqtg@hanoi.gov.vn</div>"""
    return article_page("Dịch vụ", "Tour đêm",
                        "Trải nghiệm Văn Miếu – Quốc Tử Giám dưới ánh đèn đêm với hướng dẫn viên.",
                        body, DICH_VU_SIDEBAR, "dich-vu/tour-dem/index.html",
                        [("Trang chủ","index.html"),("Dịch vụ","dich-vu/index.html"),("Tour đêm","")], 2)

def build_huong_dan_vien():
    body = """
<p>Dịch vụ hướng dẫn viên cung cấp thuyết minh chuyên sâu tại từng điểm di tích bởi đội ngũ hướng dẫn viên được đào tạo chuyên nghiệp.</p>
<h2>Ngôn ngữ</h2>
<ul>
  <li>Tiếng Việt</li>
  <li>Tiếng Anh</li>
  <li>Tiếng Pháp</li>
  <li>Tiếng Trung Quốc</li>
</ul>
<h2>Đặt dịch vụ</h2>
<table class="info-table">
  <tr><th>Điện thoại</th><td>024.3823.5601</td></tr>
  <tr><th>Đặt trước</th><td>Tối thiểu 1 ngày làm việc</td></tr>
  <tr><th>Nhóm tối thiểu</th><td>5 người</td></tr>
</table>
<div class="note">Hãy liên hệ với cán bộ tại quầy bán vé nếu muốn sử dụng dịch vụ hướng dẫn viên trong ngày.</div>
<h2>Hướng dẫn theo đoàn</h2>
<p>Đối với đoàn lớn (từ 20 người), vui lòng liên hệ trước để sắp xếp hướng dẫn viên và lịch tham quan phù hợp.</p>"""
    return article_page("Dịch vụ", "Hướng dẫn viên",
                        "Dịch vụ hướng dẫn viên tiếng Việt, Anh, Pháp và Trung Quốc.",
                        body, DICH_VU_SIDEBAR, "dich-vu/huong-dan-vien/index.html",
                        [("Trang chủ","index.html"),("Dịch vụ","dich-vu/index.html"),("Hướng dẫn viên","")], 2)

# ─── BUILD ALL ────────────────────────────────────────────────────────────────

def main():
    print("Building Văn Miếu – Quốc Tử Giám V5 site...")

    # CSS
    css_path = ROOT / "assets" / "css" / "style.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(CSS, encoding="utf-8")
    print(f"  ✓ assets/css/style.css")

    # Images
    print("Copying images...")
    copy_imgs()

    # Pages
    print("Generating pages...")
    pages = [
        ("index.html",                                     build_home()),
        # Tham quan
        ("tham-quan/index.html",                           build_tham_quan()),
        ("tham-quan/gio-mo-cua/index.html",               build_gio_mo_cua()),
        ("tham-quan/chinh-sach-gia/index.html",           build_chinh_sach_gia()),
        ("tham-quan/quy-dinh-noi-quy/index.html",         build_quy_dinh()),
        ("tham-quan/so-do/index.html",                    build_so_do()),
        ("tham-quan/duong-den/index.html",                build_duong_den()),
        ("tham-quan/tien-ich/index.html",                 build_tien_ich()),
        # Về di tích
        ("ve-di-tich/index.html",                         build_ve_di_tich()),
        ("ve-di-tich/lich-su/index.html",                 build_lich_su()),
        ("ve-di-tich/kien-truc/index.html",               build_kien_truc()),
        ("ve-di-tich/danh-nhan/index.html",               build_danh_nhan()),
        ("ve-di-tich/he-thong-tuong-tho/index.html",      build_tuong_tho()),
        # Trưng bày
        ("trung-bay-trien-lam/index.html",                build_trung_bay_hub()),
        ("trung-bay-trien-lam/co-dinh/index.html",        build_trung_bay_co_dinh()),
        ("trung-bay-trien-lam/chuyen-de/index.html",      build_chuyen_de()),
        ("trung-bay-trien-lam/su-kien/index.html",        build_su_kien()),
        # Các hoạt động
        ("cac-hoat-dong/index.html",                      build_hoat_dong_hub()),
        ("cac-hoat-dong/thu-vien/index.html",             build_thu_vien()),
        ("cac-hoat-dong/khong-gian-so/index.html",        build_khong_gian_so()),
        ("cac-hoat-dong/dong-thoi-gian/index.html",       build_dong_thoi_gian()),
        ("cac-hoat-dong/giao-duc-di-san/index.html",      build_giao_duc_di_san()),
        # Dịch vụ
        ("dich-vu/index.html",                            build_dich_vu_hub()),
        ("dich-vu/ho-van/index.html",                     build_ho_van()),
        ("dich-vu/mua-ve/index.html",                     build_mua_ve()),
        ("dich-vu/audio-guide/index.html",                build_audio_guide()),
        ("dich-vu/hang-luu-niem/index.html",              build_hang_luu_niem()),
        ("dich-vu/tour-dem/index.html",                   build_tour_dem()),
        ("dich-vu/huong-dan-vien/index.html",             build_huong_dan_vien()),
    ]

    for rel_path, html in pages:
        write(ROOT / rel_path, html)

    print(f"\nDone. {len(pages)} pages generated.")

if __name__ == "__main__":
    main()
