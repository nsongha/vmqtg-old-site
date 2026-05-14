# VMQTG V5 — Design System

Tài liệu mô tả hệ thống thiết kế trích xuất từ mockup V5 (sitemap 09.05.2026).
Style chính: **wireframe monochrome**, đen / trắng / xám, không màu phụ, typography
sans-serif đơn giản, ảnh grayscale, không skeuomorphism, không gradient màu.

---

## 1. Nguyên tắc thiết kế

| # | Nguyên tắc | Giải thích |
|---|---|---|
| 1 | **Monochrome đơn sắc** | Chỉ dùng thang xám từ `#111110` đến `#ffffff`. Không có màu phụ (no accent color). Ảnh được áp `grayscale(100%)` để đồng nhất tông. |
| 2 | **Wireframe-first** | Mọi container có border 1px `#e4e4df`. Không shadow nặng, không radius (square corners), không glow. Cảm giác như bản vẽ kỹ thuật. |
| 3 | **Content trước, motion sau** | Header / footer paint instant. Chỉ content area fade-in nhẹ. Animation chỉ để soften, không drawing attention. |
| 4 | **Typography là nhân vật chính** | Letter-spacing siết (-0.02em với title), font-weight phân tầng rõ (400 / 500 / 600 / 700). Không dùng decoration ngoài bold. |
| 5 | **Information density vừa phải** | Padding container 1.5rem, gap grid 1.25rem. Không chật, không loãng — đọc thoải mái nhưng không lãng phí. |
| 6 | **Số / ID luôn hiển thị** | Mọi mục đều có ID (`B3.4`, `D1`, …) — màu xám nhạt, kích thước nhỏ, đứng trước label. Vừa là metadata vừa là wayfinding. |

---

## 2. Foundations

### 2.1 Color tokens

| Token | Hex | Dùng cho |
|---|---|---|
| `--ink-0` | `#111110` | Text chính, header bg, sidebar CTA bg, footer bg |
| `--ink-1` | `#222` | Border header |
| `--ink-2` | `#444` | Article body text, table text |
| `--ink-3` | `#666` | Dropdown text, breadcrumb link |
| `--ink-4` | `#777` | Card description, page-sub |
| `--ink-5` | `#888` | Section title overline |
| `--ink-6` | `#999` | Breadcrumb, card desc secondary |
| `--ink-7` | `#aaa` | Quick-label, sidebar overline |
| `--ink-8` | `#bbb` | Card num, dropdown num, label pill text |
| `--ink-9` | `#ccc` | Block num inactive |
| `--paper-0` | `#ffffff` | Card bg, header tools bg invert |
| `--paper-1` | `#f7f7f5` | Body bg, dropdown hover, info-table th bg |
| `--paper-2` | `#fafaf8` | Section-block hover bg |
| `--paper-3` | `#ececE8` | Placeholder image bg |
| `--paper-4` | `#ebebE8` | Card-img empty bg |
| `--paper-5` | `#e8e8e4` | Article-hero empty bg |
| `--line-0` | `#e4e4df` | Border chuẩn (card, table, breadcrumb, header tools…) |
| `--line-1` | `#f0f0ec` | Border row trong list (sidebar links, search results) |
| `--line-2` | `#dedeD9` | Cross-hatch placeholder pattern |
| **Inverse (trên nền đen)** | | |
| `rgba(255,255,255,.85)` | | Footer link hover |
| `rgba(255,255,255,.55)` | | Footer text, lang-btn idle |
| `rgba(255,255,255,.4)` | | Brand-sub, nav-cta border |
| `rgba(255,255,255,.35)` | | Brand-mark border |
| `rgba(255,255,255,.3)` | | Footer col-title |
| `rgba(255,255,255,.25)` | | Footer copy |
| `rgba(255,255,255,.18)` | | Search-input border, lang-switch border |
| `rgba(255,255,255,.12)` | | Search-input focus bg, lang-btn divider |
| `rgba(255,255,255,.08)` | | Footer top border |
| `rgba(255,255,255,.06)` | | Search-input idle bg |
| **Highlight (duy nhất)** | | |
| `--mark-yellow` | `#fff3a3` | `<mark>` highlight kết quả search — màu duy nhất không xám |

### 2.2 Typography

**Font family**
```css
'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif
```
Load qua Google Fonts: weights `300 / 400 / 500 / 600 / 700`.

**Scale**

| Token | Size | Weight | Letter-spacing | Line-height | Dùng cho |
|---|---|---|---|---|---|
| `display` | 2.2rem (35px) | 700 | -0.02em | 1.15 | Hero title homepage |
| `h1` / `page-title` | 1.95rem (31px) | 700 | -0.02em | 1.2 | Page title (hub/group/item) |
| `article-h1` | 1.7rem (27px) | 700 | -0.02em | 1.2 | H1 trong article body |
| `h2` | 1.2rem (19px) | 600 | -0.01em | 1.3 | H2 trong article |
| `body-lg` | 1.1rem (18px) | 600 | 0 | 1.4 | Price-value |
| `h3` | 1rem (16px) | 600 | 0 | 1.4 | H3 trong article |
| `hero-sub` | .95rem (15px) | 400 | 0 | 1.4 | Hero subtitle, page-sub |
| `card-title` | .92rem (15px) | 600 | 0 | 1.4 | Card title |
| `body` | .88rem (14px) | 400/500 | 0 | 1.65 | Quick-value, body chung |
| `card-desc` | .82rem (13px) | 400 | 0 | 1.55 | Note, info-table cell |
| `nav` | .8rem (13px) | 400 | 0 | 1.4 | Dropdown link, brand-name, sidebar link |
| `card-desc-sm` | .78rem (12px) | 400 | 0 | 1.55 | Card description, search result |
| `meta` | .76rem (12px) | 400/500 | 0 | 1.4 | Footer link, footer-address, nav-cta |
| `caption` | .74rem (12px) | 400 | 0 | 1.4 | Section-block-sub, search-input |
| `caption-sm` | .72rem (11px) | 400 | 0 | 1.4 | Footer-copy, card-arrow |
| `overline` | .68rem (11px) | 700 | .04em | 1.2 | Mega-col-title |
| `overline-sm` | .65rem–.62rem (10px) | 600/700 | .06–.10em | 1.2 | Card-num, quick-label, sidebar-title, label pill, section-title |
| `micro` | .58rem (9px) | 500/600 | .08em UPPERCASE | 1.2 | Brand-sub, ph-label trên ảnh |

**Quy tắc**
- Title luôn `letter-spacing: -0.02em` (siết để cảm giác chắc tay)
- Overline / metadata luôn `text-transform: UPPERCASE` + `letter-spacing: 0.06–0.10em` (giãn ra)
- Body luôn `line-height: 1.65–1.8` (đọc thoải mái)
- Không dùng `font-style: italic` ngoài `<em>` trong article

### 2.3 Spacing scale

Theo bậc **0.25rem (4px)** — dễ tính, đủ chia nhỏ.

| Token | Value | Dùng |
|---|---|---|
| `s-0` | 0 | reset |
| `s-1` | .25rem (4px) | letter padding, micro gap |
| `s-2` | .4rem (6px) | nav padding-y, list item gap |
| `s-3` | .5rem (8px) | inline gap nhỏ |
| `s-4` | .6rem (10px) | header-tools gap, dropdown padding-y |
| `s-5` | .75rem (12px) | table cell padding, sidebar title gap |
| `s-6` | .85rem (14px) | quick-bar gap, dropdown padding-x |
| `s-7` | 1rem (16px) | nav-cta padding-x, info-table padding-x |
| `s-8` | 1.25rem (20px) | card-body padding, gallery gap base, dropdown padding-x |
| `s-9` | 1.5rem (24px) | container padding, grid gap, mega padding |
| `s-10` | 1.75rem (28px) | section-block padding-y |
| `s-11` | 2rem (32px) | header gap, page-hd padding-bottom |
| `s-12` | 2.5rem (40px) | page-hd padding-top, hero-content padding |
| `s-13` | 3rem (48px) | hero-content padding-x, content gap, footer padding-y |

**Container**
```css
.container{max-width:1200px; margin:0 auto; padding:0 1.5rem}
```

**Grid**
```css
.grid-2{grid-template-columns:repeat(2,1fr); gap:1.25rem}
.grid-3{grid-template-columns:repeat(3,1fr); gap:1.25rem}
.grid-4{grid-template-columns:repeat(4,1fr); gap:1.25rem}
.sections-grid{grid-template-columns:repeat(5,1fr); gap:1px; bg:#e4e4df} /* divider grid */
```

> **Divider grid pattern**: gap = 1px + background = border-color tạo cảm giác bảng kẻ ô đều — không cần border per-cell.

### 2.4 Border, radius, shadow

| Token | Value |
|---|---|
| `border-base` | `1px solid #e4e4df` |
| `border-row` | `1px solid #f0f0ec` |
| `border-strong` | `1px solid #222` (header) |
| `border-light` | `1.5px solid rgba(255,255,255,.35)` (brand-mark) |
| `radius` | **0** — toàn bộ site không có border-radius |
| `shadow-dropdown` | `0 8px 24px rgba(0,0,0,.04)` |
| `shadow-search` | `0 12px 32px rgba(0,0,0,.08)` |

> Không có shadow trên card, button, hay container thông thường. Shadow chỉ dùng cho **floating layers** (dropdown, search results).

### 2.5 Image treatment

```css
filter: grayscale(100%) contrast(.85) brightness(1.06);
```
- Áp cho **mọi `<img>`** trong card, article-hero, gallery, hero-img
- Mục đích: ảnh tư liệu cũ / mới trộn lẫn vẫn cảm giác đồng nhất, không "đập" tông
- `aspect-ratio` chuẩn:
  - Hero (full-bleed): chiều cao cố định `420px`
  - Card-img: `16/9`
  - Card.compact card-img: `4/3`
  - Article-hero: `16/9`
  - Gallery-item: `4/3`

### 2.6 Z-index scale

| Layer | z-index |
|---|---|
| Base content | 0 |
| Dropdown menu | 50 |
| Sticky header | 100 |
| Search results | 200 |

### 2.7 Breakpoint

| Width | Tên | Hành vi |
|---|---|---|
| `> 900px` | Desktop | Full layout |
| `≤ 900px` | Mobile | Search box thu nhỏ, mega menu wrap, grid xuống 1-2 cột |

---

## 3. Components

### 3.1 Header (sticky)

```
[brand] [main-nav            ] [search] [VI EN FR] [Tickets]
```
- `position: sticky; top: 0; z-index: 100`
- `background: #111110; color: #fff`
- `height: 60px`
- `border-bottom: 1px solid #222`
- Brand mark: 34×34px, border 1.5px, text "VM"
- Nav-item hover/active → `color: #fff` (từ .65 alpha → 1)
- Dropdown indicator: `▾` Unicode sau label, opacity .6

### 3.2 Nav dropdown

**Simple** (C / D / E sections)
- Width auto, min 240px
- Background trắng, border `#e4e4df`
- Padding `.6rem 0`, items padding `.55rem 1.25rem`
- Dropdown number: `min-width: 1.8rem`, `color: #bbb`, font-weight 600

**Mega** (B section)
- Width 1100px, max `calc(100vw - 2rem)`
- Position `left: 50%; transform: translateX(-50%)`
- 6 cột, gap 1.5rem
- Mega-col-title: overline-sm, border-bottom

### 3.3 Search box

| State | Width | Background | Border |
|---|---|---|---|
| Idle | 180px | `rgba(255,255,255,.06)` | `rgba(255,255,255,.18)` |
| Focus | 260px | `rgba(255,255,255,.12)` | `rgba(255,255,255,.4)` |

- Height: 30px, transition `width .25s ease`
- Results dropdown: 360px width, max-height 60vh, bg trắng, border `#e4e4df`, shadow `0 12px 32px rgba(0,0,0,.08)`
- Result row: 3 phần — `sr-id` (mono-style ID), `sr-title` (bold), `sr-sub` (xám nhạt indent)
- Hover/selected row → bg `#f7f7f5`
- `<mark>`: bg `#fff3a3` (vàng nhạt — **màu duy nhất không xám** trong toàn site)

### 3.4 Language switch

```
[VI] [EN] [FR]
```
- 3 buttons trong container `border: 1px solid rgba(255,255,255,.18)`
- Height 30px (= search input)
- Active: bg trắng, color đen
- Idle: transparent, color `rgba(255,255,255,.55)`
- Hover: color `#fff`
- Divider giữa buttons: `border-right: 1px solid rgba(255,255,255,.12)`

### 3.5 Buy ticket CTA (header)

- Border `1px solid rgba(255,255,255,.4)`
- Padding `.4rem 1rem`
- Hover: invert (bg trắng, color đen)
- Font: caption + weight 500

### 3.6 Breadcrumb

```
Home › Activities › Hands-on experiences
```
- Background trắng, border-bottom
- Padding `.6rem 0`, font caption
- Color: `#999`, link `#666`
- Separator `›` color `#ccc`, margin `0 .4rem`

### 3.7 Hero (homepage only)

- Image full-width, height 420px, object-fit cover + grayscale filter
- Overlay: `linear-gradient(to top, rgba(0,0,0,.55) 0%, rgba(0,0,0,.1) 55%, transparent 100%)`
- Content position absolute bottom, padding `2.5rem 3rem`
- Title: display (2.2rem, 700, -.02em)
- Sub: hero-sub (.95rem, opacity .75, max-width 560px)

### 3.8 Quick info bar

```
[Giờ mở cửa     |  Địa chỉ          |  Điện thoại    |  Giá vé      ]
[07:30 – 18:00  |  58 Quốc Tử Giám  |  024.3747.1322 |  30.000đ/người]
```
- Flex row, 4 items equal flex
- Padding `1.2rem 1rem`, divider `border-right: 1px solid #e4e4df`
- Label: overline-sm (.62rem, UPPERCASE, color `#aaa`)
- Value: body (.88rem, font-weight 500)

### 3.9 Page header (hub/group/item)

```
[LABEL · ID]
Page title
Page subtitle text describing this section.
```
- Background trắng, border-bottom, padding `2.5rem 0 2rem`
- Label pill: overline-sm, border `1px solid #ddd`, padding `.2rem .55rem`
- Title: h1 (1.95rem, 700, -.02em)
- Sub: hero-sub, max-width 640px, color `#777`

### 3.10 Card

**Default**
```
┌─────────────┐
│   image     │  aspect 16:9, grayscale
│             │
├─────────────┤
│ B3.4         │  card-num: overline-sm xám
│ Khuê Văn Các │  card-title: 600
│ Mô tả ngắn… │  card-desc: xám 13px
└─────────────┘
```
- Background trắng, `border: 1px solid #e4e4df`
- Hover: border `#bbb` (chỉ đổi border, không lift, không shadow)
- Card-img: aspect-ratio 16/9, bg `#ebebE8`
- Card-body: padding 1.2rem

**Compact** (`.card.compact`)
- Card-img aspect 4/3
- Body padding nhỏ hơn `.85rem 1rem 1rem`
- Title 13px, desc 11.5px

### 3.11 Placeholder image

Khi không có ảnh:
- Background: ảnh `/assets/images/placeholder.jpg` (Khuê Văn Các, Wikimedia CC) cover
- Filter: cùng grayscale như ảnh thật
- Overlay gradient nhẹ bottom 18% black
- Label pill bottom-left: `rgba(0,0,0,.55)` + backdrop-blur 2px, text `.58rem` UPPERCASE màu trắng (ví dụ "B3.4 · KHUÊ VĂN CÁC")

JS fallback: `<img>` load fail → tự đổi `src` về `placeholder.jpg`.

### 3.12 Article body

```css
.article{max-width:720px}
```
- H1: 1.7rem, 700, margin-bottom 1.5rem
- H2: 1.2rem, 600, margin-top 2rem
- H3: 1rem, 600, margin-top 1.5rem
- P: color `#444`, line-height 1.8, margin-bottom .95rem
- UL/OL: bullet/decimal, margin-left ~1.25rem
- Article-hero: aspect 16/9, margin-bottom 2rem

### 3.13 Info table

| | |
|---|---|
| TH width 35% | bg `#f7f7f5`, weight 600, color `#444` |
| TD | color `#444` |
| Padding | `.75rem 1rem` |
| Border | `1px solid #e4e4df` outer + bottom per row, last row no bottom |

### 3.14 Price table

```
Người lớn               30.000đ
Học sinh – sinh viên    15.000đ
Trẻ em < 15 tuổi       Miễn phí
```
- Border `1px solid #e4e4df`, bg trắng
- Row: flex, padding `1rem 1.25rem`, border-bottom
- Category: flex 1, .9rem, color `#444`
- Value: 1.1rem, 600, color `#111`, white-space nowrap

### 3.15 Sidebar (right rail)

- Width 280px, grid-template-columns `1fr 280px` trong `.content-inner`
- Box: border `1px solid #e4e4df`, bg trắng, padding 1.25rem
- Title: overline-sm UPPERCASE `#aaa`
- Links: padding `.4rem 0`, border-row giữa, color `#444`, hover `#111`
- Active link: weight 600, color `#111`
- CTA: full-width block, bg `#111110`, color trắng, padding `.95rem 1.25rem`, text-align center

### 3.16 Section block (homepage grid)

```
[A]
Tham quan
Vé · Giờ · Đường đến
─────────────
Vé · Giờ · Đường đến
```
- 5 cột grid với 1px gap (divider effect)
- Bg trắng, padding `1.75rem 1.5rem`
- Hover bg `#fafaf8`
- Num: overline-sm `#ccc`
- Name: .95rem, 600
- Sub: caption `#999`
- Count footer: top-border `1px solid #f0f0ec`, padding-top, overline-sm `#bbb`

### 3.17 Gallery

- Grid 3 cột, gap 1px, bg `#e4e4df`, border outer
- Item: bg trắng, aspect 4/3, grayscale image

### 3.18 Footer

- Background `#111110`, padding `3rem 0 2rem`, color `rgba(255,255,255,.55)`
- Footer-grid: 5 cột `2fr 1fr 1fr 1fr 1fr` (cột đầu rộng cho address)
- Brand: weight 600, color trắng
- Address: `.76rem`, line-height 1.85
- Col-title: overline-sm UPPERCASE `rgba(255,255,255,.3)`
- Link: meta size, `rgba(255,255,255,.5)` → hover `.85`
- Copy: top-border `rgba(255,255,255,.08)`, padding-top 1.5rem, `.72rem` color `.25`

### 3.19 Note / callout

```css
.note{
  background:#fff;
  border-left:2px solid #ccc;
  border:1px solid #e4e4df;
  padding:.9rem 1.1rem;
  font-size:.82rem;color:#666;
  line-height:1.65;
  margin:1.25rem 0;
}
```

### 3.20 Label pill

```css
.label{
  font-size:.62rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
  border:1px solid #ddd;
  padding:.2rem .55rem;
  color:#888;
}
```

---

## 4. Patterns

### 4.1 i18n (VI / EN / FR live swap)

3 loại attribute build-time:
- `data-i18n="ui.buy_ticket"` → swap `textContent`
- `data-i18n-html="content.tham-quan"` → swap `innerHTML` (long-form)
- `data-i18n-attr="placeholder:ui.search_ph"` → swap attribute

Lookup: `window.I18N` dict (key → `{en, fr}`), VI là bản gốc → fallback khi thiếu key.
Lưu chọn vào `localStorage.vmqtg_lang`. Lần đầu: dò `navigator.language`.

### 4.2 Search autocomplete

- Index `window.SEARCH_INDEX` (64 entries phẳng, mỗi entry có `vi/en/fr/sub_*` field)
- Diacritic-insensitive: `String.prototype.normalize('NFD')` + strip combining marks
- Multi-lang: query đồng thời search VI + EN + FR
- Scoring: ngôn ngữ active +100, VI +80, ngôn ngữ khác +50; prefix > middle match
- Top 10 results; keyboard `↑ ↓ Enter Esc`
- URL prefix tự suy ra từ `<link rel=stylesheet href>` → search hoạt động ở mọi depth

### 4.3 Page transitions

**Phương án dùng:** pure-CSS fade-in cascade (không JS, không VT API).

```css
@keyframes pageFadeIn{
  from{opacity:0;transform:translate3d(0,8px,0)}
  to  {opacity:1;transform:none}
}
```

**Timeline khi load page:**

| Phần | Delay | Duration | Easing |
|---|---|---|---|
| `.breadcrumb` | 0ms | 360ms | `cubic-bezier(.2,.8,.2,1)` |
| `.hero` / `.page-hd` | 80ms | 360ms | ↑ |
| `.quick-bar` | 160ms | 360ms | ↑ |
| `.sections-overview` / `.content` (container) | 200ms | 360ms | ↑ |
| Child `:nth-child(n)` của container | 320ms + (n-1)×120ms, cap n=8 | 360ms | ↑ |
| `.site-footer` | 280ms | 360ms | ↑ |

**Persistent UI:** header & footer paint instant (không animate khi reload). Body bg = `#f7f7f5` set trên `<html>` → không có flash trắng giữa các trang.

### 4.4 Language transition (directional split)

Khi đổi ngôn ngữ (không reload):
- Menu/header: slide từ trái (translateX -12px → 0), 350ms, stagger 30ms × index, cap index 15
- Content/footer: slide từ trên (translateY -8px → 0), 350ms, static delay per section class:
  - breadcrumb 0ms · hero 80ms · quick-bar 160ms · page-hd 160ms · sections-overview/content 240ms · site-footer 320ms
- Cùng easing `cubic-bezier(.2,.8,.2,1)`
- `prefers-reduced-motion: reduce` → animation: none

### 4.5 Hover / interaction

- Card hover: `border-color: #e4e4df → #bbb` (chỉ border)
- Nav link hover: `color: rgba(255,255,255,.65) → #fff`
- Button invert (nav-cta hover): bg fill từ transparent → `#fff`, color invert
- Dropdown link hover: bg `#f7f7f5`, color `#111`
- Section-block hover: bg `#fafaf8`
- **Không có**: lift on hover, scale on hover, glow, color flash

### 4.6 Animation tokens

| Token | Value |
|---|---|
| `dur-fast` | 150ms |
| `dur-base` | 250ms (search box width) |
| `dur-page` | 360ms (page section fade) |
| `dur-lang` | 350ms (language swap slide) |
| `easing-out` | `cubic-bezier(.2,.8,.2,1)` (vào nhanh, giảm tốc) |
| `stagger-tight` | 30ms (menu items) |
| `stagger-loose` | 120ms (content cascade) |

### 4.7 Accessibility

- `<html lang="vi/en/fr">` được set runtime mỗi lần đổi ngôn ngữ
- Tất cả ảnh có `alt`
- `<button>` cho lang switch (không `<a>` giả button)
- Search input có `aria-label` qua placeholder, results có `role="listbox"`
- Keyboard support: search ↑↓ Enter Esc; tab navigation toàn site
- `prefers-reduced-motion: reduce` → tất cả animation tắt
- Contrast ratio: text chính `#111110` trên `#f7f7f5` ≈ 18:1, text phụ `#666` trên trắng ≈ 6:1

---

## 5. Layout templates

### 5.1 Homepage
```
Header (sticky)
Hero (420px image + overlay + title bottom-left)
Quick-bar (4 items)
Sections-overview (5-col grid: A B C D E)
Footer
```

### 5.2 Section hub (e.g. `/cac-hoat-dong/`)
```
Header
Breadcrumb
Page-hd (label + title + sub)
Sections-overview hoặc card grid (3-4 cột)
Footer
```

### 5.3 Group hub (e.g. `/ve-di-tich/kien-truc/`)
```
Header
Breadcrumb
Page-hd
Content-inner (2-col: card grid 3-cột | sidebar nhóm)
Footer
```

### 5.4 Item page (e.g. `/ve-di-tich/kien-truc/khue-van-cac/`)
```
Header
Breadcrumb
Page-hd (label + title)
Content-inner:
  ├─ Article (max 720px)
  │   ├─ Article-hero image (16:9)
  │   ├─ H2 / P / UL …
  │   ├─ Info-table (nếu cần)
  │   └─ Note callout (nếu cần)
  └─ Sidebar (280px: list items same group + Buy ticket CTA)
Footer
```

---

## 6. Iconography

**Phong cách:** monoline stroke 1.4–1.5px, không fill, vuông góc, viewBox 24×24.

Hiện chỉ có **1 icon** trong codebase: image placeholder (camera/mountain).
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"
     stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="5" width="18" height="14" rx="1.5"/>
  <circle cx="8.5" cy="10.5" r="1.6"/>
  <path d="M21 16.5l-5.2-5.2-8.8 8.7"/>
</svg>
```

Dropdown arrow & breadcrumb separator dùng **Unicode**:
- `▾` (U+25BE) — dropdown
- `›` (U+203A) — breadcrumb
- `→` (U+2192) — CTA arrow

---

## 7. Naming convention

- BEM-lite: `.block`, `.block-element`, `.block.modifier`
- ID prefix theo sitemap: `A`, `B`, `B3.4`, `C1`, `D2`… — số mục đầu là section, số sau là vị trí trong section
- File slug: kebab-case không dấu (`khue-van-cac`, `tham-quan`, `cac-hoat-dong`)
- Class component dùng prefix:
  - `.site-*` cho global (`.site-header`, `.site-footer`)
  - `.page-*` cho page-level (`.page-hd`, `.page-title`)
  - `.card-*`, `.dropdown-*`, `.search-*`, `.lang-*`, `.nav-*` cho components

---

## 8. Build constraints

- **Static HTML**: site sinh từ `build.py` (Python), không backend
- **Single CSS file**: `assets/css/style.css` (~13KB minify-ready, không có CSS reset thư viện ngoài)
- **Two JS files**: `data.js` (build artifact, ~50KB chứa I18N + search index) + `app.js` (~7KB logic)
- **Không framework**: vanilla JS, không React/Vue/jQuery
- **Không build step ngoài Python**: `python3 build.py` là toàn bộ pipeline
- **Image budget**: ảnh thật grayscale JPG ~400-1000KB, placeholder 485KB (Khuê Văn Các)
- **Font**: 1 family (Inter), 5 weights, qua Google Fonts CDN
