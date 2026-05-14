#!/usr/bin/env python3
"""
Extract content from old-site (./site) + vmqtg-v5/translations.py into
data/oldsite-content.json.

Sources:
  - Pages (top-level): vi from ./site (when present), en/fr from v5 CONTENT.
    For pages that exist only in v5 (cac-hoat-dong sub-categories, dich-vu,
    trung-bay-trien-lam), vi comes from v5 too.
  - DiTich items: full vi + en/fr from v5 (per-item entries in CONTENT).

Output:
{
  "pages":  [{ "slug": str, "vi": str|None, "en": str|None, "fr": str|None }, ...],
  "diTich": [{ "slug": str, "vi": str|None, "en": str|None, "fr": str|None }, ...]
}
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OLDSITE = REPO_ROOT.parent / "site"
V5_ROOT = REPO_ROOT.parent / "vmqtg-v5"
V5_TRANS = V5_ROOT / "translations.py"
OUTPUT = REPO_ROOT / "data" / "oldsite-content.json"

# Page → v5 LABELS/SUBS key (None when no v5 entry exists for this slug)
PAGE_LABEL_KEY: dict[str, str | None] = {
    "tham-quan": "A",
    "ve-di-tich": "B",
    "giao-duc-di-san": "D2",
    "hoat-dong": "D",
    "bia-tien-si": None,         # custom page (not in v5 nav)
    "ve-chung-toi": None,        # custom page
    "trung-bay-trien-lam": "C",
    "dich-vu": "E",
}

# DiTich slug → v5 id_code (drives v5 LABELS lookup for en/fr title)
DI_TICH_CODE: dict[str, str] = {
    "lich-su/thoi-ly": "B1.1",
    "lich-su/thoi-tran": "B1.2",
    "lich-su/thoi-le": "B1.3",
    "lich-su/thoi-nguyen": "B1.4",
    "phan-khu/noi-tu": "B2.1",
    "phan-khu/vuon-giam": "B2.2",
    "phan-khu/ho-van": "B2.3",
    "kien-truc/bia-ha-ma": "B3.1",
    "kien-truc/cong-van-mieu": "B3.2",
    "kien-truc/cong-dai-trung": "B3.3",
    "kien-truc/khue-van-cac": "B3.4",
    "kien-truc/nha-che-bia": "B3.5",
    "kien-truc/cong-dai-thanh": "B3.6",
    "kien-truc/bai-duong": "B3.7",
    "kien-truc/cong-thai-hoc": "B3.8",
    "kien-truc/thai-hoc": "B3.9",
    "kien-truc/nha-chuong-trong": "B3.10",
    "kien-truc/nha-bat-giac": "B3.11",
    "kien-truc/phuong-dinh": "B3.12",
    "danh-nhan/vua-ly-thanh-tong": "B4.1",
    "danh-nhan/vua-ly-nhan-tong": "B4.2",
    "danh-nhan/vua-le-thanh-tong": "B4.3",
    "danh-nhan/chu-van-an": "B4.5",
    "danh-nhan/khoa-bang": "B4.6",
    "tuong-tho/khong-tu": "B5.1",
    "tuong-tho/nhan-tu": "B5.2",
    "tuong-tho/tu-tu": "B5.3",
    "tuong-tho/tang-tu": "B5.4",
    "tuong-tho/manh-tu": "B5.5",
    "thu-vien/thu-vien-anh": "B6.1",
    "thu-vien/video": "B6.2",
}

# Vietnamese titles for DiTich items (derived from v5 sitemap labels — same
# strings used in DI_TICH_ITEMS seed table).
DI_TICH_VI_TITLE: dict[str, str] = {
    "lich-su/thoi-ly": "Thời Lý",
    "lich-su/thoi-tran": "Thời Trần",
    "lich-su/thoi-le": "Thời Lê",
    "lich-su/thoi-nguyen": "Thời Nguyễn",
    "phan-khu/noi-tu": "Nội tự",
    "phan-khu/vuon-giam": "Vườn Giám",
    "phan-khu/ho-van": "Hồ Văn",
    "kien-truc/bia-ha-ma": "Bia Hạ mã",
    "kien-truc/cong-van-mieu": "Cổng Văn Miếu",
    "kien-truc/cong-dai-trung": "Cổng Đại Trung",
    "kien-truc/khue-van-cac": "Khuê Văn Các",
    "kien-truc/nha-che-bia": "Nhà che bia",
    "kien-truc/cong-dai-thanh": "Cổng Đại Thành",
    "kien-truc/bai-duong": "Bái đường",
    "kien-truc/cong-thai-hoc": "Cổng Thái học",
    "kien-truc/thai-hoc": "Thái học",
    "kien-truc/nha-chuong-trong": "Nhà chuông, nhà trống",
    "kien-truc/nha-bat-giac": "Nhà Bát Giác",
    "kien-truc/phuong-dinh": "Phương đình",
    "danh-nhan/vua-ly-thanh-tong": "Vua Lý Thánh Tông",
    "danh-nhan/vua-ly-nhan-tong": "Vua Lý Nhân Tông",
    "danh-nhan/vua-le-thanh-tong": "Vua Lê Thánh Tông",
    "danh-nhan/chu-van-an": "Tư nghiệp Chu Văn An",
    "danh-nhan/khoa-bang": "Danh nhân khoa bảng",
    "tuong-tho/khong-tu": "Khổng Tử",
    "tuong-tho/nhan-tu": "Nhan Tử",
    "tuong-tho/tu-tu": "Tử Tư",
    "tuong-tho/tang-tu": "Tăng Tử",
    "tuong-tho/manh-tu": "Mạnh Tử",
    "thu-vien/thu-vien-anh": "Thư viện ảnh",
    "thu-vien/video": "Video",
}

# ─────────────────────────────────────────────────────────────────────────────
# Top-level Pages.
# Schema: (slug, source: "site"|"v5", folder, recursive, v5_content_key|None)
# - source="site": vi from ./site/<folder>; en/fr from v5_content_key if given
# - source="v5":   vi extracted from v5/<folder> recursively; vi+en/fr from
#                  v5_content_key when present too
# ─────────────────────────────────────────────────────────────────────────────
PAGES: list[tuple[str, str, str, bool, str | None]] = [
    ("tham-quan",       "site", "tham-quan",                        False, "tham-quan"),
    ("ve-di-tich",      "site", "di-tich",                          False, None),
    ("giao-duc-di-san", "site", "giao-duc-di-san",                  True,  "cac-hoat-dong/giao-duc-di-san"),
    ("hoat-dong",       "v5",   "cac-hoat-dong",                    True,  None),  # multi-cat aggregator
    ("bia-tien-si",     "site", "di-tich/bia-tien-si",              False, None),
    ("ve-chung-toi",    "site", "ve-chung-toi",                     False, None),
    ("trung-bay-trien-lam", "v5", "trung-bay-trien-lam",            True,  None),
    ("dich-vu",         "v5",   "dich-vu",                          True,  None),
]

# DiTich items — full coverage of v5 CONTENT keys under ve-di-tich/.
# Tuple: (our slug, v5 path under root)
DI_TICH = [
    # B1 — lich-su (4)
    ("lich-su/thoi-ly", "ve-di-tich/lich-su/thoi-ly"),
    ("lich-su/thoi-tran", "ve-di-tich/lich-su/thoi-tran"),
    ("lich-su/thoi-le", "ve-di-tich/lich-su/thoi-le"),
    ("lich-su/thoi-nguyen", "ve-di-tich/lich-su/thoi-nguyen"),
    # B2 — phan-khu (3)
    ("phan-khu/noi-tu", "ve-di-tich/phan-khu/noi-tu"),
    ("phan-khu/vuon-giam", "ve-di-tich/phan-khu/vuon-giam"),
    ("phan-khu/ho-van", "ve-di-tich/phan-khu/ho-van"),
    # B3 — kien-truc (12)
    ("kien-truc/bia-ha-ma", "ve-di-tich/kien-truc/bia-ha-ma"),
    ("kien-truc/cong-van-mieu", "ve-di-tich/kien-truc/cong-van-mieu"),
    ("kien-truc/cong-dai-trung", "ve-di-tich/kien-truc/cong-dai-trung"),
    ("kien-truc/khue-van-cac", "ve-di-tich/kien-truc/khue-van-cac"),
    ("kien-truc/nha-che-bia", "ve-di-tich/kien-truc/nha-che-bia"),
    ("kien-truc/cong-dai-thanh", "ve-di-tich/kien-truc/cong-dai-thanh"),
    ("kien-truc/bai-duong", "ve-di-tich/kien-truc/bai-duong"),
    ("kien-truc/cong-thai-hoc", "ve-di-tich/kien-truc/cong-thai-hoc"),
    ("kien-truc/thai-hoc", "ve-di-tich/kien-truc/thai-hoc"),
    ("kien-truc/nha-chuong-trong", "ve-di-tich/kien-truc/nha-chuong-trong"),
    ("kien-truc/nha-bat-giac", "ve-di-tich/kien-truc/nha-bat-giac"),
    ("kien-truc/phuong-dinh", "ve-di-tich/kien-truc/phuong-dinh"),
    # B4 — danh-nhan (5)
    ("danh-nhan/vua-ly-thanh-tong", "ve-di-tich/danh-nhan/vua-ly-thanh-tong"),
    ("danh-nhan/vua-ly-nhan-tong", "ve-di-tich/danh-nhan/vua-ly-nhan-tong"),
    ("danh-nhan/vua-le-thanh-tong", "ve-di-tich/danh-nhan/vua-le-thanh-tong"),
    ("danh-nhan/chu-van-an", "ve-di-tich/danh-nhan/chu-van-an"),
    ("danh-nhan/khoa-bang", "ve-di-tich/danh-nhan/khoa-bang"),
    # B5 — tuong-tho (5) — newly added
    ("tuong-tho/khong-tu", "ve-di-tich/tuong-tho/khong-tu"),
    ("tuong-tho/nhan-tu", "ve-di-tich/tuong-tho/nhan-tu"),
    ("tuong-tho/tu-tu", "ve-di-tich/tuong-tho/tu-tu"),
    ("tuong-tho/tang-tu", "ve-di-tich/tuong-tho/tang-tu"),
    ("tuong-tho/manh-tu", "ve-di-tich/tuong-tho/manh-tu"),
    # B6 — thu-vien (2) — newly added
    ("thu-vien/thu-vien-anh", "ve-di-tich/thu-vien/thu-vien-anh"),
    ("thu-vien/video", "ve-di-tich/thu-vien/video"),
]

ARTICLE_RE = re.compile(
    r'<article\s+class="article-body"[^>]*>(.*?)</article>',
    re.DOTALL,
)
PAGE_INTRO_RE = re.compile(
    r'(<h2\s+class="page-title"[^>]*>.*?</h2>\s*<p\s+class="page-sub"[^>]*>.*?</p>)',
    re.DOTALL,
)
V5_ARTICLE_RE = re.compile(
    r'<div\s+class="article"[^>]*>(.*?)</div>\s*</div>\s*</div>',
    re.DOTALL,
)


def rewrite_paths(html: str) -> str:
    """Rewrite GitHub Pages prefix to a local-served path."""
    html = html.replace("/vmqtg-old-site/assets/", "/oldsite/assets/")
    html = html.replace("/vmqtg-old-site/", "/")
    return html


def extract_article_body(html_path: Path) -> str | None:
    """Return inner HTML of <article class="article-body">."""
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = ARTICLE_RE.search(text)
    return rewrite_paths(m.group(1).strip()) if m else None


def extract_page_intro(html_path: Path) -> str | None:
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = PAGE_INTRO_RE.search(text)
    return rewrite_paths(m.group(1).strip()) if m else None


def extract_v5_article(html_path: Path) -> str | None:
    """For v5 di-tich pages: inner HTML of <div class="article">."""
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = V5_ARTICLE_RE.search(text)
    return rewrite_paths(m.group(1).strip()) if m else None


def load_v5_dicts() -> tuple[dict, dict, dict, dict]:
    """Load CONTENT, LABELS, SUBS, UI from vmqtg-v5/translations.py."""
    if not V5_TRANS.exists():
        return ({}, {}, {}, {})
    ns: dict = {}
    exec(V5_TRANS.read_text(encoding="utf-8"), ns)
    return (
        ns.get("CONTENT", {}),
        ns.get("LABELS", {}),
        ns.get("SUBS", {}),
        ns.get("UI", {}),
    )


# Optional UI dict keys for page-specific title/subtitle (preferred over LABELS
# when present — these are written as page headers, not nav menu labels).
PAGE_UI_KEY: dict[str, str] = {
    "tham-quan": "a",  # UI["page_a_title"] = "Visitor information" etc.
}


# Hardcoded VI page titles/subtitles for slugs without a `<p class="page-sub">`
# on either site/ or v5. Used when neither HTML source nor v5 LABELS/SUBS
# provides one — keeps the seed deterministic instead of falling through to
# empty values that would break required-field validation later.
PAGE_VI_FALLBACK: dict[str, dict[str, str]] = {
    "tham-quan":           {"title": "Thông tin tham quan", "subtitle": "Vé, giờ mở cửa, nội quy, đường đến và các tiện ích."},
    # v0.3 sitemap shortens nav labels — page headings match
    "ve-di-tich":          {"title": "Di tích",             "subtitle": "Lịch sử, phân khu, kiến trúc, danh nhân, tượng thờ và thư viện."},
    "giao-duc-di-san":     {"title": "Giáo dục di sản",     "subtitle": "Các chương trình giáo dục dành cho mọi lứa tuổi từ mầm non đến THPT."},
    "hoat-dong":           {"title": "Các hoạt động",       "subtitle": "Sự kiện, giáo dục di sản, trải nghiệm, hội thảo và workshop."},
    "bia-tien-si":         {"title": "82 Bia Tiến Sĩ",      "subtitle": "Di sản tư liệu thế giới UNESCO · 1.307 tiến sĩ từ 1442–1779."},
    "ve-chung-toi":        {"title": "Về chúng tôi",        "subtitle": "Trung tâm hoạt động VHKH Văn Miếu – Quốc Tử Giám."},
    "trung-bay-trien-lam": {"title": "Trưng bày",           "subtitle": "Trưng bày cố định, chuyên đề và các triển lãm tại di tích."},
    "dich-vu":             {"title": "Dịch vụ",             "subtitle": "Tour đêm, audio guide, thuyết minh, quà lưu niệm, viết thư pháp."},
}

PAGE_TITLE_RE = re.compile(r'<h2\s+class="page-title"[^>]*>(.*?)</h2>', re.DOTALL)
PAGE_SUB_RE = re.compile(r'<p\s+class="page-sub"[^>]*>(.*?)</p>', re.DOTALL)


def extract_vi_title_subtitle(slug: str) -> tuple[str | None, str | None]:
    """Resolve VI page title + subtitle.

    Source of truth is PAGE_VI_FALLBACK (the v0.3 sitemap). When a slug has
    no fallback entry, we scrape site/<slug>/index.html as a safety net.
    """
    fb = PAGE_VI_FALLBACK.get(slug, {})
    if fb.get("title") and fb.get("subtitle"):
        return (fb["title"], fb["subtitle"])

    # Resolve slug → site/ folder for safety-net extraction
    folder_map = {
        "tham-quan": "tham-quan",
        "ve-di-tich": "di-tich",
        "giao-duc-di-san": "giao-duc-di-san",
        "hoat-dong": "hoat-dong",
        "bia-tien-si": "di-tich/bia-tien-si",
        "ve-chung-toi": "ve-chung-toi",
        # trung-bay-trien-lam + dich-vu are v5-only; site/ has no equivalent
    }
    folder_rel = folder_map.get(slug)
    title: str | None = fb.get("title")
    subtitle: str | None = fb.get("subtitle")
    if folder_rel:
        idx = OLDSITE / folder_rel / "index.html"
        if idx.exists():
            text = idx.read_text(encoding="utf-8")
            if title is None:
                m = PAGE_TITLE_RE.search(text)
                if m:
                    title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if subtitle is None:
                m = PAGE_SUB_RE.search(text)
                if m:
                    subtitle = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return (title, subtitle)


def build_site_html(folder: Path, recursive: bool = False) -> str | None:
    """Concat <article class="article-body"> from ./site folder.

    Top-level page may have only intro (page-title + page-sub) when its
    content lives in subpages — those are collected too.
    """
    if not folder.exists():
        return None

    parts: list[str] = []

    top_index = folder / "index.html"
    top_article = extract_article_body(top_index)
    if top_article:
        parts.append(top_article)
    else:
        intro = extract_page_intro(top_index)
        if intro:
            parts.append(intro)

    iterator = folder.rglob("index.html") if recursive else (
        sub / "index.html" for sub in sorted(folder.iterdir()) if sub.is_dir()
    )
    for sub_index in sorted(iterator):
        if sub_index == top_index:
            continue
        body = extract_article_body(sub_index)
        if body:
            parts.append(f'<section class="from-oldsite">\n{body}\n</section>')

    return "\n\n".join(parts) if parts else None


# Folders to skip entirely when walking v5/. Used when an item was dropped
# from the sitemap (e.g. E6 Nước uống removed in v0.3).
EXCLUDE_FOLDERS: set[str] = {
    "dich-vu/nuoc-uong",
}

# Folder name → anchor id mapping for v5-aggregated pages. The nav links to
# /<slug>#<id> so section ids must match the codes (C1, D1, E1...) rather than
# the raw v5 folder names. Falls back to the folder name when not mapped.
FOLDER_TO_ANCHOR: dict[str, str] = {
    # hoat-dong (cac-hoat-dong)
    "cac-hoat-dong/su-kien": "D1",
    "cac-hoat-dong/giao-duc-di-san": "D2",
    "cac-hoat-dong/trai-nghiem": "D3",
    "cac-hoat-dong/van-hoa-nghe-thuat": "D4",
    "cac-hoat-dong/hoi-thao": "D5",
    "cac-hoat-dong/doan-ngoai-giao": "D6",
    "cac-hoat-dong/workshop": "D7",
    "cac-hoat-dong/su-kien/sap-dien-ra": "D1.1",
    "cac-hoat-dong/su-kien/dang-dien-ra": "D1.2",
    # trung-bay-trien-lam
    "trung-bay-trien-lam/co-dinh": "C1",
    "trung-bay-trien-lam/chuyen-de": "C2",
    "trung-bay-trien-lam/trien-lam": "C3",
    "trung-bay-trien-lam/co-dinh/truong-quoc-hoc": "C1.1",
    "trung-bay-trien-lam/co-dinh/khoi-nguon-dao-hoc": "C1.2",
    "trung-bay-trien-lam/co-dinh/su-da-luu-danh": "C1.3",
    # dich-vu (E6 nuoc-uong removed in v0.3 sitemap)
    "dich-vu/tour-dem": "E1",
    "dich-vu/audio-guide": "E2",
    "dich-vu/huong-dan-vien": "E3",
    "dich-vu/qua-luu-niem": "E4",
    "dich-vu/thu-phap": "E5",
}


def build_v5_html(folder: Path, v5: dict, key_prefix: str, recursive: bool = True) -> tuple[str, str, str] | tuple[None, None, None]:
    """Aggregate v5 sub-categories into a single content_html block per locale.

    Walks v5/<folder>/, for each direct child <sub>/, extracts the v5 article
    body for vi and pulls en/fr from v5 CONTENT[<key_prefix>/<sub>].

    Section ids use FOLDER_TO_ANCHOR (so nav anchors #D2, #C1.1, #E4 resolve)
    and fall back to the sub-folder name when not mapped.

    Output triple is (vi, en, fr) — each is concatenated <section> blocks,
    or None if nothing found.
    """
    if not folder.exists():
        return (None, None, None)

    vi_parts: list[str] = []
    en_parts: list[str] = []
    fr_parts: list[str] = []

    for sub in sorted(folder.iterdir()):
        if not sub.is_dir():
            continue
        sub_idx = sub / "index.html"
        sub_key = f"{key_prefix}/{sub.name}"
        if sub_key in EXCLUDE_FOLDERS:
            continue
        sub_anchor = FOLDER_TO_ANCHOR.get(sub_key, sub.name)
        # vi: prefer extracted HTML, fall back to v5 CONTENT vi if defined
        vi_html = extract_v5_article(sub_idx)
        # en / fr from translations dict
        loc = v5.get(sub_key) or {}
        en_html = (loc.get("en") or "").strip() or None
        fr_html = (loc.get("fr") or "").strip() or None
        if vi_html:
            vi_parts.append(f'<section class="from-oldsite scroll-mt-24" id="{sub_anchor}">\n{vi_html}\n</section>')
        if en_html:
            en_parts.append(f'<section class="from-oldsite scroll-mt-24" id="{sub_anchor}">\n{en_html.strip()}\n</section>')
        if fr_html:
            fr_parts.append(f'<section class="from-oldsite scroll-mt-24" id="{sub_anchor}">\n{fr_html.strip()}\n</section>')

        # also dive deeper one level for su-kien/<sub-sub> (events)
        if recursive:
            for nested in sorted(sub.iterdir()) if sub.is_dir() else []:
                if not nested.is_dir():
                    continue
                nested_idx = nested / "index.html"
                nested_key = f"{key_prefix}/{sub.name}/{nested.name}"
                if nested_key in EXCLUDE_FOLDERS:
                    continue
                nested_anchor = FOLDER_TO_ANCHOR.get(nested_key, f"{sub.name}-{nested.name}")
                vi_n = extract_v5_article(nested_idx)
                loc_n = v5.get(nested_key) or {}
                en_n = (loc_n.get("en") or "").strip() or None
                fr_n = (loc_n.get("fr") or "").strip() or None
                if vi_n:
                    vi_parts.append(f'<section class="from-oldsite scroll-mt-24" id="{nested_anchor}">\n{vi_n}\n</section>')
                if en_n:
                    en_parts.append(f'<section class="from-oldsite scroll-mt-24" id="{nested_anchor}">\n{en_n.strip()}\n</section>')
                if fr_n:
                    fr_parts.append(f'<section class="from-oldsite scroll-mt-24" id="{nested_anchor}">\n{fr_n.strip()}\n</section>')

    vi = "\n\n".join(vi_parts) if vi_parts else None
    en = "\n\n".join(en_parts) if en_parts else None
    fr = "\n\n".join(fr_parts) if fr_parts else None
    return (vi, en, fr)


def main() -> None:
    if not OLDSITE.exists():
        print(f"ERROR: oldsite not found at {OLDSITE}", file=sys.stderr)
        sys.exit(1)

    v5, labels, subs, ui = load_v5_dicts()
    out = {"pages": [], "diTich": []}

    for slug, source, folder_rel, recursive, v5_key in PAGES:
        if source == "site":
            folder = OLDSITE / folder_rel
            vi = build_site_html(folder, recursive=recursive)
            en = (v5.get(v5_key) or {}).get("en") if v5_key else None
            fr = (v5.get(v5_key) or {}).get("fr") if v5_key else None
        else:  # source == "v5"
            folder = V5_ROOT / folder_rel
            vi, en, fr = build_v5_html(folder, v5, key_prefix=folder_rel, recursive=recursive)

        # Title + subtitle.
        # vi: site/<slug> page-title / page-sub, else PAGE_VI_FALLBACK.
        # en/fr: prefer UI["page_<x>_title"]/"page_<x>_sub" when defined
        # (richer page headers), else LABELS/SUBS keyed by nav code.
        vi_title, vi_subtitle = extract_vi_title_subtitle(slug)
        label_key = PAGE_LABEL_KEY.get(slug)
        ui_key = PAGE_UI_KEY.get(slug)

        ui_title = ui.get(f"page_{ui_key}_title", {}) if ui_key else {}
        ui_sub = ui.get(f"page_{ui_key}_sub", {}) if ui_key else {}
        labels_loc = labels.get(label_key) if label_key else {}
        subs_loc = subs.get(label_key) if label_key else {}

        title = {
            "vi": vi_title,
            "en": ui_title.get("en") or (labels_loc or {}).get("en"),
            "fr": ui_title.get("fr") or (labels_loc or {}).get("fr"),
        }
        subtitle = {
            "vi": vi_subtitle,
            "en": ui_sub.get("en") or (subs_loc or {}).get("en"),
            "fr": ui_sub.get("fr") or (subs_loc or {}).get("fr"),
        }

        out["pages"].append({
            "slug": slug,
            "title": title,
            "subtitle": subtitle,
            "vi": vi, "en": en, "fr": fr,
        })

    for slug, v5_path in DI_TICH:
        idx = V5_ROOT / v5_path / "index.html"
        id_code = DI_TICH_CODE.get(slug)
        title = {
            "vi": DI_TICH_VI_TITLE.get(slug),
            "en": (labels.get(id_code) or {}).get("en") if id_code else None,
            "fr": (labels.get(id_code) or {}).get("fr") if id_code else None,
        }
        out["diTich"].append({
            "slug": slug,
            "id_code": id_code,
            "title": title,
            "vi": extract_v5_article(idx),
            "en": (v5.get(v5_path) or {}).get("en"),
            "fr": (v5.get(v5_path) or {}).get("fr"),
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUTPUT}")
    for p in out["pages"]:
        marks = "".join(l[0].upper() if p[l] else "·" for l in ("vi", "en", "fr"))
        size_vi = len(p["vi"] or "")
        size_en = len(p["en"] or "")
        size_fr = len(p["fr"] or "")
        print(f"  page {p['slug']:<22} [{marks}]  vi:{size_vi:>7}B  en:{size_en:>7}B  fr:{size_fr:>7}B")
    v_count = sum(1 for d in out["diTich"] if d["vi"])
    e_count = sum(1 for d in out["diTich"] if d["en"])
    f_count = sum(1 for d in out["diTich"] if d["fr"])
    print(f"  diTich: vi {v_count}/{len(out['diTich'])}  en {e_count}/{len(out['diTich'])}  fr {f_count}/{len(out['diTich'])}")


if __name__ == "__main__":
    main()
