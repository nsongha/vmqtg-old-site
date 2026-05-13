#!/usr/bin/env python3
"""
Extract content from old-site (./site) into data/oldsite-content.json.

For each top-level Page slug, builds a Vietnamese content_html by combining:
  1) The intro from <main> of <slug>/index.html (page-title + page-sub)
  2) Every subpage's <article class="article-body"> content, each as a <section>

Vietnamese only — old-site has no en/fr (those came from vmqtg-v5/translations.py,
extracted separately if needed). Output JSON shape:
{
  "pages": [{ "slug": str, "vi": str|None, "en": str|None, "fr": str|None }, ...]
}
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OLDSITE = REPO_ROOT.parent / "site"
V5_TRANS = REPO_ROOT.parent / "vmqtg-v5" / "translations.py"
OUTPUT = REPO_ROOT / "data" / "oldsite-content.json"

# Map our new slug → old-site folder path (relative to ./site)
# bia-tien-si is nested under di-tich/ in the old site
# (slug, folder under ./site, recursive)
PAGES: list[tuple[str, str, bool]] = [
    ("tham-quan", "tham-quan", False),
    # ve-di-tich intentionally non-recursive: di-tich-items collection
    # already provides per-item content; only seed the overview intro here.
    ("ve-di-tich", "di-tich", False),
    ("giao-duc-di-san", "giao-duc-di-san", True),
    ("hoat-dong", "hoat-dong", True),
    ("bia-tien-si", "di-tich/bia-tien-si", False),
    ("ve-chung-toi", "ve-chung-toi", False),
]

# DiTich items still use v5 (richer per-item content + has en/fr translations).
DI_TICH = [
    ("lich-su/thoi-ly", "ve-di-tich/lich-su/thoi-ly"),
    ("lich-su/thoi-tran", "ve-di-tich/lich-su/thoi-tran"),
    ("lich-su/thoi-le", "ve-di-tich/lich-su/thoi-le"),
    ("lich-su/thoi-nguyen", "ve-di-tich/lich-su/thoi-nguyen"),
    ("phan-khu/noi-tu", "ve-di-tich/phan-khu/noi-tu"),
    ("phan-khu/vuon-giam", "ve-di-tich/phan-khu/vuon-giam"),
    ("phan-khu/ho-van", "ve-di-tich/phan-khu/ho-van"),
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
    ("danh-nhan/vua-ly-thanh-tong", "ve-di-tich/danh-nhan/vua-ly-thanh-tong"),
    ("danh-nhan/vua-ly-nhan-tong", "ve-di-tich/danh-nhan/vua-ly-nhan-tong"),
    ("danh-nhan/vua-le-thanh-tong", "ve-di-tich/danh-nhan/vua-le-thanh-tong"),
    ("danh-nhan/chu-van-an", "ve-di-tich/danh-nhan/chu-van-an"),
    ("danh-nhan/khoa-bang", "ve-di-tich/danh-nhan/khoa-bang"),
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


def extract_article_body(html_path: Path) -> str | None:
    """Return inner HTML of <article class="article-body">."""
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = ARTICLE_RE.search(text)
    return m.group(1).strip() if m else None


def extract_page_intro(html_path: Path) -> str | None:
    """Return the page-title + page-sub block from a top-level page."""
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = PAGE_INTRO_RE.search(text)
    return m.group(1).strip() if m else None


def extract_v5_article(html_path: Path) -> str | None:
    """For v5 di-tich pages: inner HTML of <div class="article">."""
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    m = V5_ARTICLE_RE.search(text)
    return m.group(1).strip() if m else None


def load_v5_content() -> dict:
    """Load CONTENT dict from vmqtg-v5/translations.py for en/fr fallbacks."""
    if not V5_TRANS.exists():
        return {}
    ns = {}
    exec(V5_TRANS.read_text(encoding="utf-8"), ns)
    return ns.get("CONTENT", {})


def build_page_html(folder: Path, recursive: bool = False) -> str | None:
    """Combine intro + subpage articles into a single content_html block.

    When `recursive=True`, walks all nested subfolders to collect article bodies.
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

    # Collect article bodies from descendants (skip the top index.html itself).
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


def main() -> None:
    if not OLDSITE.exists():
        print(f"ERROR: oldsite not found at {OLDSITE}", file=sys.stderr)
        sys.exit(1)

    v5 = load_v5_content()
    out = {"pages": [], "diTich": []}

    for slug, folder_rel, recursive in PAGES:
        folder = OLDSITE / folder_rel
        vi = build_page_html(folder, recursive=recursive)
        v5_key = {
            "tham-quan": "tham-quan",
            "giao-duc-di-san": "cac-hoat-dong/giao-duc-di-san",
        }.get(slug)
        en = (v5.get(v5_key) or {}).get("en") if v5_key else None
        fr = (v5.get(v5_key) or {}).get("fr") if v5_key else None
        out["pages"].append({"slug": slug, "vi": vi, "en": en, "fr": fr})

    # DiTich items: pulled from v5 (richer per-item, has en/fr)
    v5_root = REPO_ROOT.parent / "vmqtg-v5"
    for slug, v5_path in DI_TICH:
        idx = v5_root / v5_path / "index.html"
        entry = {
            "slug": slug,
            "vi": extract_v5_article(idx),
            "en": (v5.get(v5_path) or {}).get("en"),
            "fr": (v5.get(v5_path) or {}).get("fr"),
        }
        out["diTich"].append(entry)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUTPUT}")
    for p in out["pages"]:
        marks = "".join(l[0].upper() if p[l] else "·" for l in ("vi", "en", "fr"))
        size = len(p["vi"] or "")
        print(f"  page {p['slug']:<20} [{marks}]  vi:{size}B")
    print(f"  diTich: {sum(1 for d in out['diTich'] if d['vi'])} / {len(out['diTich'])} with vi")


if __name__ == "__main__":
    main()
