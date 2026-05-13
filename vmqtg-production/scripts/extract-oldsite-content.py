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


def load_v5_content() -> dict:
    if not V5_TRANS.exists():
        return {}
    ns: dict = {}
    exec(V5_TRANS.read_text(encoding="utf-8"), ns)
    return ns.get("CONTENT", {})


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


def build_v5_html(folder: Path, v5: dict, key_prefix: str, recursive: bool = True) -> tuple[str, str, str] | tuple[None, None, None]:
    """Aggregate v5 sub-categories into a single content_html block per locale.

    Walks v5/<folder>/, for each direct child <sub>/, extracts the v5 article
    body for vi and pulls en/fr from v5 CONTENT[<key_prefix>/<sub>].

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
        # vi: prefer extracted HTML, fall back to v5 CONTENT vi if defined
        vi_html = extract_v5_article(sub_idx)
        # en / fr from translations dict
        loc = v5.get(sub_key) or {}
        en_html = (loc.get("en") or "").strip() or None
        fr_html = (loc.get("fr") or "").strip() or None
        if vi_html:
            vi_parts.append(f'<section class="from-oldsite" id="{sub.name}">\n{vi_html}\n</section>')
        if en_html:
            en_parts.append(f'<section class="from-oldsite" id="{sub.name}">\n{en_html.strip()}\n</section>')
        if fr_html:
            fr_parts.append(f'<section class="from-oldsite" id="{sub.name}">\n{fr_html.strip()}\n</section>')

        # also dive deeper one level for su-kien/<sub-sub> (events)
        if recursive:
            for nested in sorted(sub.iterdir()) if sub.is_dir() else []:
                if not nested.is_dir():
                    continue
                nested_idx = nested / "index.html"
                nested_key = f"{key_prefix}/{sub.name}/{nested.name}"
                vi_n = extract_v5_article(nested_idx)
                loc_n = v5.get(nested_key) or {}
                en_n = (loc_n.get("en") or "").strip() or None
                fr_n = (loc_n.get("fr") or "").strip() or None
                if vi_n:
                    vi_parts.append(f'<section class="from-oldsite" id="{sub.name}-{nested.name}">\n{vi_n}\n</section>')
                if en_n:
                    en_parts.append(f'<section class="from-oldsite" id="{sub.name}-{nested.name}">\n{en_n.strip()}\n</section>')
                if fr_n:
                    fr_parts.append(f'<section class="from-oldsite" id="{sub.name}-{nested.name}">\n{fr_n.strip()}\n</section>')

    vi = "\n\n".join(vi_parts) if vi_parts else None
    en = "\n\n".join(en_parts) if en_parts else None
    fr = "\n\n".join(fr_parts) if fr_parts else None
    return (vi, en, fr)


def main() -> None:
    if not OLDSITE.exists():
        print(f"ERROR: oldsite not found at {OLDSITE}", file=sys.stderr)
        sys.exit(1)

    v5 = load_v5_content()
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
        out["pages"].append({"slug": slug, "vi": vi, "en": en, "fr": fr})

    for slug, v5_path in DI_TICH:
        idx = V5_ROOT / v5_path / "index.html"
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
