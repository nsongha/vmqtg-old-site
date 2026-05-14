# VMQTG V5 — Tính năng tương tác

Tài liệu mô tả 2 tính năng JS được thêm vào website V5 (sitemap 09.05.2026):
**Tìm kiếm autocomplete** trên header, và **Đổi ngôn ngữ live VI / EN / FR**.

> Cả 2 tính năng đều chạy hoàn toàn ở client side, không cần server / backend.
> Site vẫn là static HTML — deploy lên Vercel/GitHub Pages như cũ.

---

## 1. Tìm kiếm autocomplete

### Mô tả

- Input search nằm ở góc phải header (cạnh nút ngôn ngữ và nút "Mua vé").
- Khi focus, ô input mở rộng từ 180px → 260px.
- Gõ tối thiểu 1 ký tự → dropdown gợi ý xuất hiện ngay phía dưới (debounce 80ms).
- Hiển thị tối đa 10 kết quả; mỗi kết quả gồm:
  - **ID mục** (ví dụ `B3.4`) — màu xám, monospace-style
  - **Tiêu đề** — highlight phần khớp bằng `<mark>`
  - **Mô tả phụ** (mục cha hoặc sub-text)
- Click hoặc nhấn `Enter` → đi tới trang tương ứng.
- Click ngoài / nhấn `Esc` → đóng dropdown.

### Đặc điểm tìm kiếm

| Tính năng | Mô tả |
|---|---|
| **Không dấu** | Gõ "thoi ly" → ra "Thời Lý"; "khue van" → "Khuê Văn Các". Dùng `String.prototype.normalize('NFD')` rồi loại bỏ dấu kết hợp. |
| **Đa ngôn ngữ** | Một query đồng thời search trên VI + EN + FR. Gõ "pavilion" hoặc "pavillon" cũng ra Khuê Văn Các. |
| **Ưu tiên ngôn ngữ hiện tại** | Match ở field thuộc ngôn ngữ active có trọng số cao nhất (100 điểm), VI 80, EN/FR khác 50. |
| **Ưu tiên prefix** | Match ở đầu chuỗi xếp trước match ở giữa chuỗi (trừ dần theo offset). |
| **Phím tắt** | `↑ / ↓` di chuyển; `Enter` mở; `Esc` đóng. |

### Search index

Build script tự động sinh `assets/js/data.js` chứa biến `window.SEARCH_INDEX`
là mảng phẳng tất cả 64 trang:

```js
[
  { id: "home", url: "index.html",
    vi: "Trang chủ", en: "Home", fr: "Accueil",
    sub_vi: "Văn Miếu – Quốc Tử Giám", ... },
  { id: "B3.4",  url: "ve-di-tich/kien-truc/khue-van-cac/index.html",
    vi: "Khuê Văn Các", en: "Khuê Văn Pavilion", fr: "Pavillon Khuê Văn",
    sub_vi: "Công trình kiến trúc", ... },
  ...
]
```

Khi thêm trang mới vào `SITEMAP` trong `build.py`, index tự cập nhật ở lần
build kế tiếp — không cần code thêm.

### Tính tương đối của URL

Search dropdown tự suy ra prefix `../` cần thiết bằng cách đọc `href` của
`<link rel="stylesheet">` đã render. Nhờ vậy search hoạt động đúng ở **mọi
độ sâu** trang (từ home tới trang `B3.4` sâu 4 cấp).

---

## 2. Đổi ngôn ngữ VI / EN / FR

### UI

- 3 nút `VI` `EN` `FR` đặt giữa search box và nút "Mua vé".
- Nút active có nền trắng, chữ đen; các nút khác mờ với chữ trắng.
- Click 1 nút → toàn bộ trang đổi ngôn ngữ **không reload**.
- Lựa chọn được lưu vào `localStorage` key `vmqtg_lang`, áp dụng cho tất cả trang khi điều hướng.
- Lần đầu vào: ưu tiên `localStorage`, sau đó dò `navigator.language` (en/fr → set tương ứng), mặc định VI.

### Cơ chế swap text

Build script gắn 3 loại attribute lên element cần dịch:

| Attribute | Dùng cho | JS swap |
|---|---|---|
| `data-i18n="ui.buy_ticket"` | Text ngắn (label, tiêu đề) | `el.textContent` |
| `data-i18n-html="content.tham-quan"` | Khối HTML dài (cả article body) | `el.innerHTML` |
| `data-i18n-attr="placeholder:ui.search_ph"` | Thuộc tính (placeholder, alt, title…) | `el.setAttribute()` |

Khi load trang lần đầu, JS lưu bản gốc tiếng Việt vào các attribute backup
(`data-vi-text`, `data-vi-html`, `data-vi-attr-{name}`) để có thể chuyển
ngược về VI mà không cần reload.

### Bảng dịch (`translations.py`)

Tách riêng khỏi `build.py` để dễ bảo trì. Cấu trúc:

```python
UI = {           # text giao diện chung
  "buy_ticket": {"en":"Tickets", "fr":"Billets"},
  "in_section": {"en":"In this section", "fr":"Dans cette section"},
  ...
}
LABELS = {       # nhãn của section/group/item theo ID
  "B3.4": {"en":"Khuê Văn Pavilion", "fr":"Pavillon Khuê Văn"},
  ...
}
SUBS = {         # mô tả phụ
  "B3":  {"en":"Twelve emblematic structures…", "fr":"Douze ouvrages…"},
  ...
}
CONTENT = {      # nội dung HTML dài, theo slug đường dẫn
  "tham-quan": {"en":"<h2>Opening hours</h2>…", "fr":"…"},
  ...
}
```

Build script gộp 4 dict này thành `window.I18N` trong `assets/js/data.js`,
key dạng `ui.*`, `label.*`, `sub.*`, `content.*` (125 keys hiện tại).

### Fallback

- Khi key không có bản dịch EN/FR → JS giữ nguyên text VI gốc.
- Trang `Tham quan` đã dịch đầy đủ EN+FR (long-form content).
- Toàn bộ navigation, breadcrumb, sidebar, footer, page title/sub đã dịch.
- Item content pages (`B1.1`, `B3.4`…) hiện hiển thị VI fallback — chỉ cần
  thêm entry vào `CONTENT[slug]` trong `translations.py` để có bản dịch.

### Hiệu ứng — Directional split (2 vùng song song)

Trang được chia thành **2 vùng animation độc lập, chạy đồng thời**:

| Vùng | Selector | Hướng | Duration / item | Stagger | Cap |
|---|---|---|---|---|---|
| **Menu / header** | `.site-header [data-i18n]` | trái → phải (`translateX -12px → 0`) | 350ms | 30ms × index | max index 15 |
| **Content + footer** | `.breadcrumb, .hero, .quick-bar, .page-hd, .content, .sections-overview, .site-footer` | trên → dưới (`translateY -8px → 0`) | 350ms | 25ms × index | max index 20 |

→ Tổng animation chỉ ≈ **800ms** (item cuối + duration), nhưng vì 2 vùng chạy
song song theo 2 trục **vuông góc**, mắt cảm nhận như "trang đang
re-organize" chứ không lộn xộn — pattern giống Linear / Stripe / Apple.

**Cùng easing** (`cubic-bezier(.2,.8,.2,1)`) cho cả 2 vùng → đồng bộ về cảm xúc.

### Cơ chế tối ưu performance

```css
.lang-entering .site-header [data-i18n]{
  animation: slideFromLeft .35s cubic-bezier(.2,.8,.2,1) both;
  animation-delay: calc(min(var(--i,0), 15) * 30ms);
  will-change: transform, opacity;
}
```

```js
function indexElements(){
  document.querySelectorAll(MENU_SEL).forEach((el,i) =>
    el.style.setProperty('--i', i));
  document.querySelectorAll(CONTENT_SEL).forEach((el,i) =>
    el.style.setProperty('--i', i));
}
```

| Tối ưu | Lý do |
|---|---|
| **Chỉ animate `transform` + `opacity`** | GPU compositor — không repaint/reflow, 60fps cả khi 50+ elements. |
| **CSS animation, không JS animate** | Browser schedule trên compositor thread, không block main thread. |
| **`--i` set qua `style.setProperty`** | CSS tính delay bằng `calc()`, JS không cần lặp tính delay. |
| **`min(var(--i), N)`** | Cap stagger để item thứ 50 không phải chờ 1.5s. |
| **`translate3d(...)` thay vì `translate(...)`** | Force GPU layer, mượt hơn trên mobile. |
| **`prefers-reduced-motion: reduce`** | Người dùng tắt animation OS-level → animation: none. |
| **Bỏ "leaving phase"** | Không chờ fade-out 180ms — đổi text + animate-in luôn → snappy hơn. |
| **Force reflow `void offsetWidth`** | Restart animation khi user click liên tiếp 2 nút ngôn ngữ. |

**Không dùng View Transitions API** trong Level B này — vì View Transitions
sẽ cross-fade toàn trang cùng nhau, conflict với hiệu ứng split 2 trục
đã thiết kế. Khi cần "smart-move morph" thì có thể bật riêng cho item
nào có `view-transition-name` (Level C, chưa triển khai).

### Cập nhật tiêu đề tab

Sau khi swap ngôn ngữ, JS đọc `<h1.page-title>` (đã được dịch) và gắn vào
`document.title` cùng tên di tích đã dịch — tab browser cũng đổi theo.

### Cập nhật `<html lang>`

`document.documentElement.setAttribute('lang', lang)` được set mỗi lần đổi
ngôn ngữ → tốt cho accessibility (screen reader) và SEO.

---

## 3. Files liên quan

```
vmqtg-v5/
├── translations.py          # bảng dịch UI / labels / subs / content
├── build.py                 # sinh i18n attributes + data.js + app.js
└── assets/js/
    ├── data.js              # AUTO-GENERATED — window.I18N + window.SEARCH_INDEX
    └── app.js               # logic search + i18n + animation
```

**Lưu ý**: `assets/js/data.js` là file build artifact, sửa thủ công sẽ bị ghi đè.

---

## 4. Cách thêm bản dịch mới

### Thêm 1 mục menu mới (ví dụ thêm item B3.13)

1. Thêm vào `SITEMAP` trong `build.py` như item bình thường (chỉ cần `id`, `label`, `slug`).
2. Thêm vào `LABELS` trong `translations.py`:
   ```python
   "B3.13": {"en":"New Building", "fr":"Nouveau bâtiment"},
   ```
3. Chạy `python3 build.py` — search index + i18n tự cập nhật.

### Thêm bản dịch nội dung dài

Thêm vào `CONTENT` trong `translations.py`, key = slug đường dẫn (không có `index.html`):

```python
CONTENT = {
    "ve-di-tich/lich-su/thoi-ly": {
        "en": "<p>The Văn Miếu was founded under King Lý Thánh Tông in 1070…</p>",
        "fr": "<p>Le Văn Miếu fut fondé sous le règne du roi Lý Thánh Tông en 1070…</p>",
    },
    ...
}
```

### Thêm UI string mới

Thêm vào `UI` trong `translations.py`:
```python
UI = {
    "my_new_label": {"en":"...", "fr":"..."},
    ...
}
```

Trong `build.py` emit element với:
```python
f'<span data-i18n="ui.my_new_label">Bản tiếng Việt</span>'
```

---

## 5. Giới hạn hiện tại

- **Bản dịch chưa đầy đủ** cho long-form content của các trang B/C/D/E item.
  VI sẽ hiển thị làm fallback — không hỏng giao diện, chỉ thiếu bản EN/FR.
- **Search không tìm trong nội dung article body** — chỉ index theo
  label / sub. Nếu cần full-text search, có thể parse `CONTENT` dict và
  thêm field `body_*` vào search index.
- **View Transitions API smart-move** chỉ hoạt động trên trình duyệt
  Chromium-based; Safari/Firefox dùng fallback animation đơn giản hơn.
- **Không có URL routing theo ngôn ngữ** (kiểu `/en/...`). Lựa chọn ngôn
  ngữ chỉ lưu trong `localStorage`. Share link cho người khác → họ vẫn
  thấy theo ngôn ngữ của họ. Nếu cần share theo ngôn ngữ, sau này có thể
  thêm `?lang=en` query param.
