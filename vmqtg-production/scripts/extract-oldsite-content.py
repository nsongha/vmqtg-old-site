#!/usr/bin/env python3
"""
Extract content from vmqtg-v5 oldsite into data/oldsite-content.json.

Produces a JSON of:
{
  "pages": [{ "slug": str, "vi": str|None, "en": str|None, "fr": str|None }, ...],
  "diTich": [{ "slug": str, "vi": str|None, "en": str|None, "fr": str|None }, ...]
}

Vietnamese is read from the inner HTML of <div class="article" ...> in each oldsite
index.html. English/French come from vmqtg-v5/translations.py CONTENT dict.

Run once locally, commit the JSON. Seed-on-build will then upsert into Payload.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OLDSITE = REPO_ROOT.parent / "vmqtg-v5"
OUTPUT = REPO_ROOT / "data" / "oldsite-content.json"

# (our slug, oldsite path relative to vmqtg-v5)
PAGES = [
    ("tham-quan", "tham-quan", "tham-quan"),
    ("giao-duc-di-san", "cac-hoat-dong/giao-duc-di-san", "cac-hoat-dong/giao-duc-di-san"),
    ("hoat-dong", "cac-hoat-dong", None),  # landing, no CONTENT entry
    ("bia-tien-si", "ve-di-tich/bia-tien-si", None),  # has its own viewer
]

# DiTichItems: (our slug, oldsite path under vmqtg-v5/ve-di-tich, CONTENT key)
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
    r'<div\s+class="article"[^>]*>(.*?)</div>\s*</div>\s*</div>',
    re.DOTALL,
)


def extract_vi_html(html_path: Path) -> str | None:
    """Extract inner HTML of <div class="article">...</div> (closes at /div before footer)."""
    if not html_path.exists():
        return None
    text = html_path.read_text(encoding="utf-8")
    # Greedy match between `<div class="article" ...>` and the matching `</div>` followed by content close.
    # Simpler heuristic: capture from `<div class="article"` until `</div></div></div>` (article > container > content).
    m = ARTICLE_RE.search(text)
    if not m:
        return None
    return m.group(1).strip()


def load_translations_content() -> dict:
    """Load CONTENT dict from translations.py via exec."""
    trans_path = OLDSITE / "translations.py"
    if not trans_path.exists():
        return {}
    ns = {}
    code = trans_path.read_text(encoding="utf-8")
    exec(code, ns)
    return ns.get("CONTENT", {})


def main() -> None:
    if not OLDSITE.exists():
        print(f"ERROR: oldsite not found at {OLDSITE}", file=sys.stderr)
        sys.exit(1)

    content = load_translations_content()
    out = {"pages": [], "diTich": []}

    for slug, src_path, ck in PAGES:
        idx = OLDSITE / src_path / "index.html"
        entry = {
            "slug": slug,
            "vi": extract_vi_html(idx),
            "en": (content.get(ck) or {}).get("en") if ck else None,
            "fr": (content.get(ck) or {}).get("fr") if ck else None,
        }
        out["pages"].append(entry)

    for slug, ck in DI_TICH:
        idx = OLDSITE / ck / "index.html"
        entry = {
            "slug": slug,
            "vi": extract_vi_html(idx),
            "en": (content.get(ck) or {}).get("en"),
            "fr": (content.get(ck) or {}).get("fr"),
        }
        out["diTich"].append(entry)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUTPUT}")
    print(f"  pages: {sum(1 for p in out['pages'] if any(p[l] for l in ['vi','en','fr']))} with content / {len(out['pages'])}")
    print(f"  diTich: {sum(1 for p in out['diTich'] if any(p[l] for l in ['vi','en','fr']))} with content / {len(out['diTich'])}")


if __name__ == "__main__":
    main()
