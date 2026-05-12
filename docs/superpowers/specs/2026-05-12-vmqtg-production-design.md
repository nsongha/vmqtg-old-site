# VMQTG Production — Design Spec
**Date:** 2026-05-12
**Status:** Approved

## Overview

Rebuild website Văn Miếu – Quốc Tử Giám từ static HTML (vmqtg-v5) sang Next.js + Payload CMS, đồng thời nâng cấp UI/design lên production-quality. Mục tiêu: biên tập viên non-technical của Văn Miếu tự quản lý nội dung, site hỗ trợ VI/EN/FR, extensible cho mobile app tương lai.

---

## 1. Architecture

### Pattern: Next.js + Payload Monorepo

Payload chạy embedded trong Next.js App Router — cùng một repo, một deployment. Frontend dùng local API (không qua HTTP), admin UI tự động tại `/admin`.

```
vmqtg-production/
├── app/
│   ├── (frontend)/              ← trang visitor
│   │   ├── [locale]/
│   │   │   ├── page.tsx         ← trang chủ
│   │   │   ├── tham-quan/page.tsx
│   │   │   ├── ve-di-tich/[slug]/page.tsx
│   │   │   └── bia-tien-si/[id]/page.tsx
│   └── (payload)/
│       └── admin/[[...segments]]/  ← Payload admin UI
├── collections/
│   ├── Pages.ts
│   ├── DiTichItems.ts
│   ├── BiaTienSi.ts
│   ├── Media.ts
│   └── Navigation.ts
├── components/
├── scripts/
│   ├── seed-bia-tien-si.ts
│   ├── seed-di-tich.ts
│   └── migrate-media.ts
├── payload.config.ts
└── next.config.ts
```

### Runtime Flow

```
Visitor request
  → Next.js App Router (SSG/ISR)
  → payload.find() [local, zero HTTP]
  → render HTML → browser

Editor saves in /admin
  → Payload writes to Postgres
  → Next.js ISR revalidation (trang cập nhật trong vài giây)

Mobile app
  → GET /api/payload/bia-tien-si (REST)
  → hoặc /api/graphql
```

### Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 15+ (App Router) |
| CMS | Payload CMS (latest) |
| Database | PostgreSQL (Neon dev / managed production) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Media storage | Cloudflare R2 |
| Deploy (dev) | Vercel + Neon free tier |
| Deploy (production) | Hetzner CX22 VPS + Docker + Nginx |

---

## 2. Payload Collections

### 2.1 `pages` — Nội dung trang tĩnh

Dùng cho: Trang chủ, Tham quan, Về di tích overview.

| Field | Type | Localized | Notes |
|---|---|---|---|
| `slug` | text | no | URL path, unique |
| `title` | text | yes | VI/EN/FR |
| `subtitle` | text | yes | mô tả ngắn |
| `hero_image` | upload | no | relation → media |
| `content` | richText | yes | nội dung chính |
| `meta_title` | text | yes | SEO |
| `meta_description` | text | yes | SEO |
| `status` | select | no | draft / published |

### 2.2 `di-tich-items` — Hạng mục di tích

Dùng cho: toàn bộ sub-pages của "Về di tích" (B1 Lịch sử, B2 Phân khu, B3 Kiến trúc, B4 Danh nhân, B5 Tượng thờ, B6 Thư viện).

| Field | Type | Localized | Notes |
|---|---|---|---|
| `id_code` | text | no | `B3.4`, `B1.1`... |
| `slug` | text | no | URL path |
| `section` | select | no | B1/B2/B3/B4/B5/B6 |
| `order` | number | no | thứ tự trong section |
| `title` | text | yes | VI/EN/FR |
| `subtitle` | text | yes | mô tả ngắn |
| `content` | richText | yes | nội dung đầy đủ |
| `images` | array | no | nhiều ảnh, relation → media |
| `status` | select | no | draft / published |

### 2.3 `bia-tien-si` — 82 Bia Tiến Sĩ

Map đầy đủ từ `docs/82-van-bia-tien-si.json`.

| Field | Type | Localized | Notes |
|---|---|---|---|
| `order` | number | no | 1–82 |
| `year` | text | no | năm thi (e.g. "1442") |
| `dynasty` | text | no | triều đại |
| `erection_year` | text | no | năm dựng bia |
| `candidates_count` | number | no | số thí sinh |
| `passed_count` | number | no | số đỗ |
| `title` | text | yes | tên bia (VI/EN/FR) |
| `contributors` | group | no | author, calligrapher, editor, engraver |
| `historical_notes` | array of text | yes | ghi chú lịch sử |
| `biographies` | array | no | danh sách tiến sĩ (xem dưới) |
| `image` | upload | no | ảnh bia |

**`biographies` array item:**

| Field | Type |
|---|---|
| `name` | text |
| `dates` | text |
| `description` | text |
| `hometown` | text |
| `roles` | array of text |

### 2.4 `media` — Thư viện ảnh

Payload built-in Media collection. Tự động resize, optimize. Upload từ admin hoặc script.

| Field | Notes |
|---|---|
| `alt` | localized, VI/EN/FR |
| `caption` | localized |

### 2.5 `navigation` — Cấu trúc menu

Quản lý cấu trúc mega menu "Về di tích" và top nav qua admin.

| Field | Type | Notes |
|---|---|---|
| `label` | text (localized) | tên hiển thị |
| `href` | text | URL |
| `children` | array | sub-items (1 cấp) |
| `mega_menu` | checkbox | dùng mega menu layout |

---

## 3. i18n

### Approach: URL-based localization

```
vmqtg.vn/vi/...   ← Vietnamese (default)
vmqtg.vn/en/...   ← English
vmqtg.vn/fr/...   ← French
vmqtg.vn/...      ← redirect → /vi/...
```

Next.js i18n routing + Payload localization fields.

### Payload localization config

```typescript
// payload.config.ts
localization: {
  locales: ['vi', 'en', 'fr'],
  defaultLocale: 'vi',
  fallback: true,   // EN/FR chưa dịch → hiển thị VI
}
```

### Admin UX cho biên tập viên

Dropdown chọn ngôn ngữ trong admin. Biên tập viên thêm bản EN/FR dần — fallback về VI tự động, không block publish.

---

## 4. UI/Design System

### Color Palette

| Token | Value | Dùng cho |
|---|---|---|
| `bg-primary` | `#FAFAF7` | nền chính (off-white ấm) |
| `ink` | `#1A1A1A` | chữ chính |
| `gold` | `#8B6914` | accent chính, heading underline |
| `red-son` | `#C41E3A` | CTA, badge (dùng tiết kiệm) |
| `border` | `#E8E4DC` | divider, border |
| `bg-subtle` | `#F2EFE9` | card background |

### Typography

| Role | Font | Weight |
|---|---|---|
| Display / H1-H2 | Lora (serif) | 600–700 |
| H3-H4 | Lora | 500 |
| Body | Inter | 400 |
| UI / caption | Inter | 400–500 |
| ID / code | JetBrains Mono | 400 |

### Layout

- 12-column grid, max-width 1280px, gutter 24px
- Mobile: single column, padding 16px
- Base spacing unit: 8px
- Section gap: 80px desktop / 48px mobile
- Cards: square corners (không bo góc — cảm giác cổ kính)

### Motif truyền thống

- Đường kẻ mảnh dạng hoa văn cổ làm section divider
- Không dùng làm background texture
- Tham khảo hoa văn bia tiến sĩ, đầu rồng Thăng Long

### Design references

| Element | Reference |
|---|---|
| Grid + whitespace | British Museum |
| Typography hierarchy | National Palace Museum Taiwan |
| Hero treatment | V&A Museum |

---

## 5. Data Migration

### Script tự động

| Nguồn | Target | Method |
|---|---|---|
| `docs/82-van-bia-tien-si.json` | `bia-tien-si` collection | `scripts/seed-bia-tien-si.ts` |
| `translations.py` (labels/subs/content) | `di-tich-items` + `pages` | `scripts/seed-di-tich.ts` |
| `vmqtg-v5/assets/images/` | `media` collection | `scripts/migrate-media.ts` |

### Sau migration — trạng thái ban đầu trong Payload

- 82 bia tiến sĩ đầy đủ dữ liệu
- ~35 di tích items (B1–B6) với nội dung VI + EN/FR từ `translations.py`
- Core pages (Trang chủ, Tham quan) nội dung VI, EN/FR từ `translations.py`
- Toàn bộ ảnh trong Media library

### Không migrate

- `build.py`, `translations.py` — thay bằng Payload
- Generated HTML pages — rebuild bằng Next.js
- `assets/js/data.js`, `app.js` — logic viết lại trong Next.js

---

## 6. MVP Scope

### Launch với

- Trang chủ
- Tham quan (giờ mở cửa, vé, đường đến)
- Về di tích (B1–B6, ~35 pages)
- Bia tiến sĩ viewer (82 bia, search, filter theo triều đại)
- Admin: biên tập viên quản lý tất cả nội dung trên
- i18n: VI đầy đủ, EN/FR từ migration (fallback VI cho nội dung chưa dịch)

### Sau MVP (backlog)

- Section C: Trưng bày, triển lãm
- Section D: Các hoạt động
- Section E: Dịch vụ
- Tin tức / sự kiện (`news`, `events` collections)
- Search full-text (Algolia hoặc built-in Payload search)
- Mobile app (React Native, dùng REST API sẵn có)

---

## 7. Deployment

### Giai đoạn 1: Dev & Demo

| Resource | Service | Chi phí |
|---|---|---|
| Hosting | Vercel | Miễn phí |
| Database | Neon (Postgres free tier) | Miễn phí |
| Media | Local filesystem (dev only) | Miễn phí |

URL demo: `vmqtg-demo.vercel.app`

### Giai đoạn 2: Production

| Resource | Service | Chi phí |
|---|---|---|
| VPS | Hetzner CX22 | ~$6/tháng |
| Database | Postgres trên VPS | Included |
| Media | Cloudflare R2 | Miễn phí (< 10GB) |
| SSL | Let's Encrypt | Miễn phí |
| **Tổng** | | **~$6/tháng** |

Infrastructure: Docker Compose + Nginx trên VPS. CI/CD: GitHub Actions → auto deploy khi push main.

### ISR Revalidation

Biên tập viên save trong admin → Payload `afterChange` hook gọi `revalidatePath()` trực tiếp (trong monorepo, không cần webhook) → trang cập nhật trong vài giây, không cần redeploy.
