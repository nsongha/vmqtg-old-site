# VMQTG Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild website Văn Miếu – Quốc Tử Giám từ static HTML sang Next.js 15 + Payload CMS monorepo với UI production-quality, i18n VI/EN/FR, và biên tập viên non-technical tự quản lý nội dung.

**Architecture:** Next.js 15 App Router + Payload v3 chạy embedded trong cùng repo. Frontend dùng local Payload API (không HTTP). Tất cả nội dung được quản lý qua `/admin` UI. ISR revalidation tự động khi biên tập viên save.

**Tech Stack:** Next.js 15, Payload CMS v3, TypeScript, Tailwind CSS v4, PostgreSQL (Neon), Vitest, pnpm

**Working directory:** Tạo `vmqtg-production/` là thư mục con trong repo hiện tại (sibling của `vmqtg-v5/`).

**Source data:**
- `vmqtg-v5/docs/82-van-bia-tien-si.json` — 82 bia tiến sĩ
- `vmqtg-v5/translations.py` — bảng dịch VI/EN/FR
- `vmqtg-v5/assets/images/` — 44 ảnh gốc

---

## File Map

```
vmqtg-production/
├── src/
│   ├── app/
│   │   ├── (frontend)/
│   │   │   └── [locale]/
│   │   │       ├── layout.tsx          ← locale layout (Header/Footer)
│   │   │       ├── page.tsx            ← trang chủ
│   │   │       ├── tham-quan/
│   │   │       │   └── page.tsx        ← Tham quan
│   │   │       ├── ve-di-tich/
│   │   │       │   ├── page.tsx        ← Về di tích overview
│   │   │       │   └── [slug]/
│   │   │       │       └── page.tsx    ← dynamic di tích item
│   │   │       └── bia-tien-si/
│   │   │           ├── page.tsx        ← danh sách 82 bia
│   │   │           └── [id]/
│   │   │               └── page.tsx    ← chi tiết 1 bia
│   │   ├── (payload)/
│   │   │   └── admin/[[...segments]]/
│   │   │       └── page.tsx            ← Payload admin UI (auto)
│   │   ├── globals.css                 ← Tailwind + design tokens
│   │   └── layout.tsx                  ← root layout
│   ├── collections/
│   │   ├── Users.ts                    ← Payload default (giữ nguyên)
│   │   ├── Media.ts                    ← media library
│   │   ├── Pages.ts                    ← trang tĩnh
│   │   ├── DiTichItems.ts              ← hạng mục di tích
│   │   ├── BiaTienSi.ts                ← 82 bia tiến sĩ
│   │   └── Navigation.ts              ← cấu trúc menu
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── MegaMenu.tsx
│   │   │   └── LanguageSwitcher.tsx
│   │   ├── ui/
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── RichText.tsx            ← Payload Lexical renderer
│   │   └── features/
│   │       ├── BiaTienSiCard.tsx
│   │       └── DiTichCard.tsx
│   ├── lib/
│   │   ├── payload.ts                  ← getPayloadClient singleton
│   │   └── i18n.ts                     ← locale utilities
│   ├── middleware.ts                   ← locale redirect
│   └── payload.config.ts              ← Payload config
├── scripts/
│   ├── seed-bia-tien-si.ts
│   ├── seed-di-tich.ts
│   └── migrate-media.ts
├── .env.local
├── next.config.ts
├── postcss.config.mjs
├── tsconfig.json
└── package.json
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `vmqtg-production/` (toàn bộ project)
- Create: `vmqtg-production/.env.local`
- Create: `vmqtg-production/postcss.config.mjs`
- Modify: `vmqtg-production/package.json` (thêm vitest + scripts)

- [ ] **Step 1: Scaffold Payload + Next.js project**

```bash
cd /Users/songha/Documents/Projects/Website\ VMQTG\ -\ olddata/.claude/worktrees/reverent-lamarr-5441b8
npx create-payload-app@latest vmqtg-production \
  --template blank \
  --db postgres \
  --no-git
cd vmqtg-production
```

Khi được hỏi package manager: chọn **pnpm**.

- [ ] **Step 2: Xác nhận project chạy được**

```bash
pnpm dev
```

Expected: Next.js server khởi động tại `localhost:3000`. Mở `localhost:3000/admin` → thấy Payload setup screen (tạo admin user). Ctrl+C dừng.

- [ ] **Step 3: Thêm Tailwind CSS v4 + Vitest**

```bash
pnpm add tailwindcss @tailwindcss/postcss
pnpm add -D vitest @vitejs/plugin-react
```

- [ ] **Step 4: Tạo postcss.config.mjs**

```js
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

- [ ] **Step 5: Thêm scripts vào package.json**

Mở `package.json`, thêm vào `"scripts"`:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "vitest run",
    "test:watch": "vitest",
    "seed:bia": "tsx scripts/seed-bia-tien-si.ts",
    "seed:ditich": "tsx scripts/seed-di-tich.ts",
    "migrate:media": "tsx scripts/migrate-media.ts"
  }
}
```

Thêm dependency:
```bash
pnpm add -D tsx
```

- [ ] **Step 6: Tạo .env.local**

```bash
# .env.local
DATABASE_URI=postgresql://neondb_owner:<password>@<host>.neon.tech/neondb?sslmode=require
PAYLOAD_SECRET=vmqtg-secret-change-in-production-min-32-chars
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

> Lấy `DATABASE_URI` từ [Neon console](https://neon.tech) (tạo project miễn phí). Hoặc dùng local Postgres: `postgresql://localhost/vmqtg_dev`.

- [ ] **Step 7: Tạo vitest.config.ts**

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'node',
    globals: true,
  },
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
})
```

- [ ] **Step 8: Chạy test (empty suite)**

```bash
pnpm test
```

Expected: `No test files found` — bình thường, chưa có test.

- [ ] **Step 9: Commit**

```bash
git add vmqtg-production/
git commit -m "feat: scaffold Next.js + Payload production project"
```

---

## Task 2: Design System

**Files:**
- Modify: `src/app/globals.css`
- Modify: `src/app/layout.tsx`

- [ ] **Step 1: Thay toàn bộ globals.css**

```css
/* src/app/globals.css */
@import "tailwindcss";

@theme {
  /* Colors */
  --color-bg-primary: #FAFAF7;
  --color-bg-subtle: #F2EFE9;
  --color-ink: #1A1A1A;
  --color-ink-muted: #5A5550;
  --color-gold: #8B6914;
  --color-gold-light: #C8A84B;
  --color-red-son: #C41E3A;
  --color-border: #E8E4DC;

  /* Typography */
  --font-serif: 'Lora', Georgia, serif;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --spacing-section: 80px;
  --spacing-section-mobile: 48px;

  /* Grid */
  --container-max: 1280px;
}

html {
  background-color: var(--color-bg-primary);
  color: var(--color-ink);
  font-family: var(--font-sans);
}

h1, h2, h3, h4 {
  font-family: var(--font-serif);
}

.container {
  max-width: var(--container-max);
  margin-inline: auto;
  padding-inline: 24px;
}

@media (max-width: 640px) {
  .container { padding-inline: 16px; }
}

/* Section divider — traditional motif */
.divider-motif {
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    var(--color-border) 20%,
    var(--color-gold) 50%,
    var(--color-border) 80%,
    transparent
  );
  margin-block: 48px;
}
```

- [ ] **Step 2: Cập nhật root layout.tsx với Google Fonts**

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next'
import { Lora, Inter, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const lora = Lora({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-lora',
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-inter',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Văn Miếu – Quốc Tử Giám',
  description: 'Di tích lịch sử quốc gia đặc biệt',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className={`${lora.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
        {children}
      </body>
    </html>
  )
}
```

- [ ] **Step 3: Cập nhật CSS variables để dùng next/font**

Thêm vào `globals.css` (sau `@theme`):

```css
:root {
  --font-serif: var(--font-lora), Georgia, serif;
  --font-sans: var(--font-inter), system-ui, sans-serif;
  --font-mono: var(--font-mono), monospace;
}
```

- [ ] **Step 4: Tạo base UI components**

```tsx
// src/components/ui/Badge.tsx
type BadgeProps = {
  children: React.ReactNode
  variant?: 'gold' | 'red' | 'muted'
}

export function Badge({ children, variant = 'muted' }: BadgeProps) {
  const styles = {
    gold: 'bg-[--color-gold] text-white',
    red: 'bg-[--color-red-son] text-white',
    muted: 'bg-[--color-bg-subtle] text-[--color-ink-muted]',
  }
  return (
    <span className={`inline-block px-2 py-0.5 text-xs font-mono rounded-sm ${styles[variant]}`}>
      {children}
    </span>
  )
}
```

```tsx
// src/components/ui/Card.tsx
type CardProps = {
  children: React.ReactNode
  className?: string
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-[--color-bg-subtle] border border-[--color-border] ${className}`}>
      {children}
    </div>
  )
}
```

- [ ] **Step 5: Tạo RichText renderer cho Payload Lexical**

```tsx
// src/components/ui/RichText.tsx
import type { SerializedEditorState } from '@payloadcms/richtext-lexical/lexical'

type Props = { content: SerializedEditorState | null | undefined }

export function RichText({ content }: Props) {
  if (!content) return null
  // Payload v3 ships a React renderer for Lexical
  // Import dynamically to avoid server/client mismatch
  const { RichText: PayloadRichText } = require('@payloadcms/richtext-lexical/react')
  return <PayloadRichText data={content} />
}
```

- [ ] **Step 6: Commit**

```bash
git add vmqtg-production/src/app/globals.css \
        vmqtg-production/src/app/layout.tsx \
        vmqtg-production/src/components/
git commit -m "feat: add design system tokens and base UI components"
```

---

## Task 3: Payload Config + Collections

**Files:**
- Modify: `src/payload.config.ts`
- Create: `src/collections/Media.ts`
- Create: `src/collections/Pages.ts`
- Create: `src/collections/DiTichItems.ts`
- Create: `src/collections/BiaTienSi.ts`
- Create: `src/collections/Navigation.ts`
- Create: `src/lib/payload.ts`

- [ ] **Step 1: Tạo Media collection**

```ts
// src/collections/Media.ts
import type { CollectionConfig } from 'payload'

export const Media: CollectionConfig = {
  slug: 'media',
  upload: {
    staticDir: '../public/media',
    imageSizes: [
      { name: 'thumbnail', width: 400, height: 300, fit: 'cover' },
      { name: 'card', width: 800, height: 600, fit: 'cover' },
      { name: 'hero', width: 1600, height: 900, fit: 'cover' },
    ],
    adminThumbnail: 'thumbnail',
  },
  fields: [
    { name: 'alt', type: 'text', localized: true },
    { name: 'caption', type: 'text', localized: true },
  ],
}
```

- [ ] **Step 2: Tạo Pages collection**

```ts
// src/collections/Pages.ts
import type { CollectionConfig } from 'payload'

export const Pages: CollectionConfig = {
  slug: 'pages',
  admin: { useAsTitle: 'title' },
  fields: [
    { name: 'slug', type: 'text', required: true, unique: true,
      admin: { description: 'URL path, ví dụ: tham-quan' } },
    { name: 'title', type: 'text', required: true, localized: true },
    { name: 'subtitle', type: 'text', localized: true },
    { name: 'hero_image', type: 'upload', relationTo: 'media' },
    { name: 'content', type: 'richText', localized: true },
    {
      name: 'meta',
      type: 'group',
      fields: [
        { name: 'title', type: 'text', localized: true },
        { name: 'description', type: 'text', localized: true },
      ],
    },
    {
      name: 'status', type: 'select', required: true, defaultValue: 'draft',
      options: [
        { label: 'Nháp', value: 'draft' },
        { label: 'Đã đăng', value: 'published' },
      ],
    },
  ],
}
```

- [ ] **Step 3: Tạo DiTichItems collection**

```ts
// src/collections/DiTichItems.ts
import type { CollectionConfig } from 'payload'

export const DiTichItems: CollectionConfig = {
  slug: 'di-tich-items',
  admin: { useAsTitle: 'title' },
  fields: [
    { name: 'id_code', type: 'text', required: true, unique: true,
      admin: { description: 'Ví dụ: B3.4, B1.1' } },
    { name: 'slug', type: 'text', required: true,
      admin: { description: 'URL path, ví dụ: kien-truc/khue-van-cac' } },
    {
      name: 'section', type: 'select', required: true,
      options: ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'].map(v => ({ label: v, value: v })),
    },
    { name: 'order', type: 'number', defaultValue: 0 },
    { name: 'title', type: 'text', required: true, localized: true },
    { name: 'subtitle', type: 'text', localized: true },
    { name: 'content', type: 'richText', localized: true },
    {
      name: 'images',
      type: 'array',
      fields: [
        { name: 'image', type: 'upload', relationTo: 'media', required: true },
        { name: 'caption', type: 'text', localized: true },
      ],
    },
    {
      name: 'status', type: 'select', required: true, defaultValue: 'published',
      options: [
        { label: 'Nháp', value: 'draft' },
        { label: 'Đã đăng', value: 'published' },
      ],
    },
  ],
}
```

- [ ] **Step 4: Tạo BiaTienSi collection**

```ts
// src/collections/BiaTienSi.ts
import type { CollectionConfig } from 'payload'

export const BiaTienSi: CollectionConfig = {
  slug: 'bia-tien-si',
  admin: { useAsTitle: 'title' },
  fields: [
    { name: 'order', type: 'number', required: true,
      admin: { description: 'Thứ tự bia (1–82)' } },
    { name: 'year', type: 'text', required: true,
      admin: { description: 'Năm thi, ví dụ: 1442' } },
    { name: 'dynasty', type: 'text', required: true },
    { name: 'erection_year', type: 'text' },
    { name: 'candidates_count', type: 'number' },
    { name: 'passed_count', type: 'number' },
    { name: 'title', type: 'text', required: true, localized: true },
    {
      name: 'contributors',
      type: 'group',
      fields: [
        { name: 'author', type: 'text' },
        { name: 'calligrapher', type: 'text' },
        { name: 'editor', type: 'text' },
        { name: 'engraver', type: 'text' },
      ],
    },
    {
      name: 'historical_notes',
      type: 'array',
      localized: true,
      fields: [{ name: 'note', type: 'textarea', required: true }],
    },
    {
      name: 'biographies',
      type: 'array',
      fields: [
        { name: 'name', type: 'text', required: true },
        { name: 'dates', type: 'text' },
        { name: 'description', type: 'textarea' },
        { name: 'hometown', type: 'text' },
        {
          name: 'roles',
          type: 'array',
          fields: [{ name: 'role', type: 'text', required: true }],
        },
      ],
    },
    { name: 'image', type: 'upload', relationTo: 'media' },
  ],
}
```

- [ ] **Step 5: Tạo Navigation collection**

```ts
// src/collections/Navigation.ts
import type { CollectionConfig } from 'payload'

export const Navigation: CollectionConfig = {
  slug: 'navigation',
  admin: { useAsTitle: 'label' },
  fields: [
    { name: 'key', type: 'text', required: true, unique: true,
      admin: { description: 'Ví dụ: main-nav, footer-nav' } },
    {
      name: 'items',
      type: 'array',
      fields: [
        { name: 'label', type: 'text', required: true, localized: true },
        { name: 'href', type: 'text', required: true },
        { name: 'mega_menu', type: 'checkbox', defaultValue: false },
        {
          name: 'children',
          type: 'array',
          fields: [
            { name: 'label', type: 'text', required: true, localized: true },
            { name: 'href', type: 'text', required: true },
            { name: 'group_id', type: 'text',
              admin: { description: 'B1, B2... để group trong mega menu' } },
          ],
        },
      ],
    },
  ],
}
```

- [ ] **Step 6: Cập nhật payload.config.ts với ISR revalidation hooks**

```ts
// src/payload.config.ts
import { buildConfig } from 'payload'
import { postgresAdapter } from '@payloadcms/db-postgres'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import { revalidatePath } from 'next/cache'
import sharp from 'sharp'
import path from 'path'
import { fileURLToPath } from 'url'

import { Media } from './collections/Media'
import { Pages } from './collections/Pages'
import { DiTichItems } from './collections/DiTichItems'
import { BiaTienSi } from './collections/BiaTienSi'
import { Navigation } from './collections/Navigation'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

// Revalidate tất cả locale paths khi content thay đổi
function revalidateLocales(path: string) {
  for (const locale of ['vi', 'en', 'fr']) {
    revalidatePath(`/${locale}${path}`)
  }
}

export default buildConfig({
  admin: { user: 'users' },
  collections: [
    Media,
    {
      ...Pages,
      hooks: {
        afterChange: [({ doc }) => revalidateLocales(`/${doc.slug}`)],
      },
    },
    {
      ...DiTichItems,
      hooks: {
        afterChange: [({ doc }) => {
          revalidateLocales('/ve-di-tich')
          revalidateLocales(`/ve-di-tich/${doc.slug}`)
        }],
      },
    },
    {
      ...BiaTienSi,
      hooks: {
        afterChange: [({ doc }) => {
          revalidateLocales('/bia-tien-si')
          revalidateLocales(`/bia-tien-si/${doc.order}`)
        }],
      },
    },
    Navigation,
  ],
  db: postgresAdapter({
    pool: { connectionString: process.env.DATABASE_URI },
  }),
  editor: lexicalEditor(),
  localization: {
    locales: [
      { label: 'Tiếng Việt', code: 'vi' },
      { label: 'English', code: 'en' },
      { label: 'Français', code: 'fr' },
    ],
    defaultLocale: 'vi',
    fallback: true,
  },
  secret: process.env.PAYLOAD_SECRET || '',
  sharp,
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
})
```

- [ ] **Step 7: Tạo lib/payload.ts**

```ts
// src/lib/payload.ts
import { getPayload } from 'payload'
import config from '@payload-config'

let cached: ReturnType<typeof getPayload> | null = null

export async function getPayloadClient() {
  if (!cached) {
    cached = getPayload({ config })
  }
  return cached
}
```

- [ ] **Step 8: Viết test cho collection schemas**

```ts
// src/collections/__tests__/schemas.test.ts
import { describe, it, expect } from 'vitest'
import { Pages } from '../Pages'
import { BiaTienSi } from '../BiaTienSi'
import { DiTichItems } from '../DiTichItems'

describe('Collection schemas', () => {
  it('Pages có slug field', () => {
    const slugField = Pages.fields.find((f: any) => f.name === 'slug')
    expect(slugField).toBeDefined()
    expect(slugField.unique).toBe(true)
  })

  it('BiaTienSi có biographies array với roles', () => {
    const bioField = BiaTienSi.fields.find((f: any) => f.name === 'biographies')
    expect(bioField?.type).toBe('array')
    const rolesField = bioField?.fields?.find((f: any) => f.name === 'roles')
    expect(rolesField?.type).toBe('array')
  })

  it('DiTichItems có đủ 6 section options', () => {
    const sectionField = DiTichItems.fields.find((f: any) => f.name === 'section')
    expect(sectionField?.options).toHaveLength(6)
  })

  it('BiaTienSi historical_notes là localized', () => {
    const notesField = BiaTienSi.fields.find((f: any) => f.name === 'historical_notes')
    expect(notesField?.localized).toBe(true)
  })
})
```

- [ ] **Step 9: Chạy test**

```bash
cd vmqtg-production && pnpm test
```

Expected: 4 tests pass.

- [ ] **Step 10: Khởi động dev, kiểm tra admin**

```bash
pnpm dev
```

Mở `http://localhost:3000/admin` → tạo admin user → kiểm tra 5 collections hiển thị đúng trong sidebar.

- [ ] **Step 11: Commit**

```bash
git add vmqtg-production/src/collections/ \
        vmqtg-production/src/lib/ \
        vmqtg-production/src/payload.config.ts
git commit -m "feat: add all Payload collections with localization and tests"
```

---

## Task 4: i18n Middleware + Locale Routing

**Files:**
- Create: `src/middleware.ts`
- Create: `src/lib/i18n.ts`
- Modify: `next.config.ts`

- [ ] **Step 1: Tạo i18n utility**

```ts
// src/lib/i18n.ts
export const LOCALES = ['vi', 'en', 'fr'] as const
export type Locale = typeof LOCALES[number]
export const DEFAULT_LOCALE: Locale = 'vi'

export function isValidLocale(locale: string): locale is Locale {
  return LOCALES.includes(locale as Locale)
}

export function getLocaleFromPathname(pathname: string): Locale | null {
  const segment = pathname.split('/')[1]
  return isValidLocale(segment) ? segment : null
}

export function localePath(locale: Locale, path: string): string {
  return `/${locale}${path.startsWith('/') ? path : '/' + path}`
}

export const LOCALE_NAMES: Record<Locale, string> = {
  vi: 'Tiếng Việt',
  en: 'English',
  fr: 'Français',
}
```

- [ ] **Step 2: Viết test cho i18n utils**

```ts
// src/lib/__tests__/i18n.test.ts
import { describe, it, expect } from 'vitest'
import {
  isValidLocale,
  getLocaleFromPathname,
  localePath,
} from '../i18n'

describe('i18n utilities', () => {
  it('isValidLocale nhận vi/en/fr', () => {
    expect(isValidLocale('vi')).toBe(true)
    expect(isValidLocale('en')).toBe(true)
    expect(isValidLocale('fr')).toBe(true)
    expect(isValidLocale('de')).toBe(false)
  })

  it('getLocaleFromPathname trả đúng locale', () => {
    expect(getLocaleFromPathname('/vi/tham-quan')).toBe('vi')
    expect(getLocaleFromPathname('/en/about')).toBe('en')
    expect(getLocaleFromPathname('/tham-quan')).toBeNull()
  })

  it('localePath tạo đúng URL', () => {
    expect(localePath('vi', '/tham-quan')).toBe('/vi/tham-quan')
    expect(localePath('en', 'tham-quan')).toBe('/en/tham-quan')
  })
})
```

- [ ] **Step 3: Chạy test**

```bash
pnpm test
```

Expected: 3 i18n tests pass (tổng 7 pass).

- [ ] **Step 4: Tạo middleware.ts**

```ts
// src/middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { LOCALES, DEFAULT_LOCALE, getLocaleFromPathname } from './lib/i18n'

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Bỏ qua admin, API, và static files
  if (
    pathname.startsWith('/admin') ||
    pathname.startsWith('/api') ||
    pathname.startsWith('/_next') ||
    pathname.startsWith('/media') ||
    pathname.includes('.')
  ) {
    return NextResponse.next()
  }

  const locale = getLocaleFromPathname(pathname)
  if (!locale) {
    const url = request.nextUrl.clone()
    url.pathname = `/${DEFAULT_LOCALE}${pathname}`
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next|api|media|.*\\..*).*)'],
}
```

- [ ] **Step 5: Cập nhật next.config.ts**

```ts
// next.config.ts
import { withPayload } from '@payloadcms/next/withPayload'
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Không cần next/i18n routing — dùng [locale] dynamic segment
}

export default withPayload(nextConfig)
```

- [ ] **Step 6: Commit**

```bash
git add vmqtg-production/src/middleware.ts \
        vmqtg-production/src/lib/i18n.ts \
        vmqtg-production/next.config.ts
git commit -m "feat: add i18n middleware and locale utilities with tests"
```

---

## Task 5: Layout Components

**Files:**
- Create: `src/components/layout/Header.tsx`
- Create: `src/components/layout/Footer.tsx`
- Create: `src/components/layout/LanguageSwitcher.tsx`
- Create: `src/components/layout/MegaMenu.tsx`
- Create: `src/app/(frontend)/[locale]/layout.tsx`

- [ ] **Step 1: Tạo LanguageSwitcher**

```tsx
// src/components/layout/LanguageSwitcher.tsx
'use client'
import { usePathname, useRouter } from 'next/navigation'
import { LOCALES, type Locale } from '@/lib/i18n'

export function LanguageSwitcher({ currentLocale }: { currentLocale: Locale }) {
  const pathname = usePathname()
  const router = useRouter()

  function switchLocale(locale: Locale) {
    // Thay thế locale segment đầu tiên trong pathname
    const segments = pathname.split('/')
    segments[1] = locale
    router.push(segments.join('/'))
  }

  return (
    <div className="flex gap-1">
      {LOCALES.map((locale) => (
        <button
          key={locale}
          onClick={() => switchLocale(locale)}
          className={`px-2 py-1 text-xs font-mono uppercase tracking-wider transition-colors
            ${locale === currentLocale
              ? 'bg-[--color-ink] text-[--color-bg-primary]'
              : 'text-[--color-ink-muted] hover:text-[--color-ink]'
            }`}
        >
          {locale}
        </button>
      ))}
    </div>
  )
}
```

- [ ] **Step 2: Tạo MegaMenu**

```tsx
// src/components/layout/MegaMenu.tsx
'use client'
import { useState } from 'react'
import Link from 'next/link'
import type { Locale } from '@/lib/i18n'

type NavChild = { label: string; href: string; group_id?: string }
type NavItem = {
  label: string
  href: string
  mega_menu?: boolean
  children?: NavChild[]
}

type Props = { items: NavItem[]; locale: Locale }

export function MegaMenu({ items, locale }: Props) {
  const [openMenu, setOpenMenu] = useState<string | null>(null)

  return (
    <nav className="hidden lg:flex items-center gap-6">
      {items.map((item) => (
        <div
          key={item.href}
          className="relative"
          onMouseEnter={() => item.children?.length ? setOpenMenu(item.href) : null}
          onMouseLeave={() => setOpenMenu(null)}
        >
          <Link
            href={`/${locale}${item.href}`}
            className="text-sm font-sans text-[--color-ink] hover:text-[--color-gold] transition-colors py-2"
          >
            {item.label}
          </Link>

          {/* Dropdown / mega menu */}
          {item.children?.length && openMenu === item.href && (
            <div className={`absolute top-full left-0 z-50 bg-[--color-bg-primary] border border-[--color-border] shadow-lg
              ${item.mega_menu ? 'w-[640px] grid grid-cols-2 gap-0' : 'w-56'}`}
            >
              {item.children.map((child) => (
                <Link
                  key={child.href}
                  href={`/${locale}${child.href}`}
                  className="block px-4 py-3 text-sm hover:bg-[--color-bg-subtle] hover:text-[--color-gold] transition-colors border-b border-[--color-border]"
                >
                  {child.group_id && (
                    <span className="font-mono text-xs text-[--color-ink-muted] block">{child.group_id}</span>
                  )}
                  {child.label}
                </Link>
              ))}
            </div>
          )}
        </div>
      ))}
    </nav>
  )
}
```

- [ ] **Step 3: Tạo Header**

```tsx
// src/components/layout/Header.tsx
import Link from 'next/link'
import { getPayloadClient } from '@/lib/payload'
import { MegaMenu } from './MegaMenu'
import { LanguageSwitcher } from './LanguageSwitcher'
import type { Locale } from '@/lib/i18n'

type Props = { locale: Locale }

export async function Header({ locale }: Props) {
  const payload = await getPayloadClient()

  const navData = await payload.find({
    collection: 'navigation',
    where: { key: { equals: 'main-nav' } },
    locale,
    limit: 1,
  })

  const navItems = navData.docs[0]?.items ?? []

  return (
    <header className="sticky top-0 z-40 bg-[--color-bg-primary] border-b border-[--color-border]">
      <div className="container flex items-center justify-between h-16 gap-8">
        {/* Logo */}
        <Link href={`/${locale}`} className="flex flex-col leading-tight">
          <span className="font-serif text-base font-semibold text-[--color-ink]">
            Văn Miếu – Quốc Tử Giám
          </span>
          <span className="text-xs text-[--color-ink-muted]">
            {locale === 'vi' ? 'Di tích lịch sử quốc gia đặc biệt'
             : locale === 'en' ? 'Special National Heritage Site'
             : 'Site du patrimoine national spécial'}
          </span>
        </Link>

        <MegaMenu items={navItems as any} locale={locale} />

        <div className="flex items-center gap-4">
          <LanguageSwitcher currentLocale={locale} />
          <Link
            href={`/${locale}/tham-quan`}
            className="hidden sm:block px-4 py-2 text-sm bg-[--color-red-son] text-white hover:opacity-90 transition-opacity"
          >
            {locale === 'vi' ? 'Mua vé' : locale === 'en' ? 'Tickets' : 'Billets'}
          </Link>
        </div>
      </div>
    </header>
  )
}
```

- [ ] **Step 4: Tạo Footer**

```tsx
// src/components/layout/Footer.tsx
import Link from 'next/link'
import type { Locale } from '@/lib/i18n'

type Props = { locale: Locale }

const FOOTER_TEXT = {
  vi: {
    address: '58 Quốc Tử Giám, Văn Miếu, Đống Đa, Hà Nội',
    phone: '024.3747.1322',
    email: 'vanmieuqtg@hanoi.gov.vn',
    copy: '© Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám',
  },
  en: {
    address: '58 Quoc Tu Giam St., Van Mieu Ward, Dong Da, Hanoi',
    phone: '024.3747.1322',
    email: 'vanmieuqtg@hanoi.gov.vn',
    copy: '© Centre for Cultural and Scientific Activities of the Temple of Literature',
  },
  fr: {
    address: '58 rue Quoc Tu Giam, Quartier Van Mieu, Dong Da, Hanoï',
    phone: '024.3747.1322',
    email: 'vanmieuqtg@hanoi.gov.vn',
    copy: '© Centre des activités culturelles et scientifiques du Temple de la Littérature',
  },
}

export function Footer({ locale }: Props) {
  const t = FOOTER_TEXT[locale]
  return (
    <footer className="mt-[--spacing-section] border-t border-[--color-border] bg-[--color-bg-subtle]">
      <div className="container py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 className="font-serif text-sm font-semibold mb-3">Văn Miếu – Quốc Tử Giám</h3>
          <address className="not-italic text-xs text-[--color-ink-muted] leading-relaxed">
            {t.address}<br />
            {t.phone}<br />
            <a href={`mailto:${t.email}`} className="hover:text-[--color-gold]">{t.email}</a>
          </address>
        </div>
        <div>
          <h3 className="font-serif text-sm font-semibold mb-3">
            {locale === 'vi' ? 'Khám phá' : locale === 'en' ? 'Explore' : 'Explorer'}
          </h3>
          <ul className="space-y-2 text-xs text-[--color-ink-muted]">
            {[
              { href: '/tham-quan', label: { vi: 'Thông tin tham quan', en: 'Visitor info', fr: 'Informations' } },
              { href: '/ve-di-tich', label: { vi: 'Về di tích', en: 'About', fr: 'À propos' } },
              { href: '/bia-tien-si', label: { vi: '82 Bia Tiến Sĩ', en: '82 Doctoral Stelae', fr: '82 Stèles' } },
            ].map((link) => (
              <li key={link.href}>
                <Link href={`/${locale}${link.href}`} className="hover:text-[--color-gold]">
                  {link.label[locale]}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="flex items-end">
          <p className="text-xs text-[--color-ink-muted]">{t.copy}</p>
        </div>
      </div>
    </footer>
  )
}
```

- [ ] **Step 5: Tạo locale layout**

```tsx
// src/app/(frontend)/[locale]/layout.tsx
import { notFound } from 'next/navigation'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'

type Props = {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  return (
    <>
      <Header locale={locale as Locale} />
      <main>{children}</main>
      <Footer locale={locale as Locale} />
    </>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
```

- [ ] **Step 6: Khởi động dev, kiểm tra layout**

```bash
pnpm dev
```

Mở `http://localhost:3000` → phải redirect về `/vi`. Mở `/vi` → thấy Header + Footer. Nếu Navigation collection chưa có data, mega menu trống là bình thường.

- [ ] **Step 7: Commit**

```bash
git add vmqtg-production/src/components/layout/ \
        vmqtg-production/src/app/\(frontend\)/
git commit -m "feat: add layout components with Header, Footer, MegaMenu, LanguageSwitcher"
```

---

## Task 6: Migration Scripts

**Files:**
- Create: `scripts/seed-bia-tien-si.ts`
- Create: `scripts/seed-di-tich.ts`
- Create: `scripts/migrate-media.ts`
- Create: `scripts/__tests__/transforms.test.ts`

- [ ] **Step 1: Viết test cho transform functions trước**

```ts
// scripts/__tests__/transforms.test.ts
import { describe, it, expect } from 'vitest'
import { transformBiaTienSi, transformHistoricalNotes } from '../transforms'

describe('Seed transforms', () => {
  it('transformHistoricalNotes chuyển string[] thành array objects', () => {
    const input = ['Note A', 'Note B']
    const result = transformHistoricalNotes(input)
    expect(result).toEqual([{ note: 'Note A' }, { note: 'Note B' }])
  })

  it('transformBiaTienSi map đúng fields', () => {
    const input = {
      id: 1,
      year: '1442',
      dynasty: 'Lê sơ',
      candidates_count: '450',
      passed_count: '33',
      erection_year: '1484',
      title: 'Văn bia đề danh Tiến sĩ khoa Nhâm Tuất',
      contributors: { author: 'Thân Nhân Trung', calligrapher: 'Nguyễn Tủng', editor: 'Không ghi', engraver: 'Tô Ngại' },
      historical_notes: ['Note 1'],
      biographies: [{ name: 'Nguyễn Trực', dates: '1417-1474', description: '...', hometown: 'Bối Khê', roles: ['Hàn lâm viện'] }],
    }
    const result = transformBiaTienSi(input)
    expect(result.order).toBe(1)
    expect(result.year).toBe('1442')
    expect(result.candidates_count).toBe(450)
    expect(result.historical_notes).toEqual([{ note: 'Note 1' }])
    expect(result.biographies[0].roles).toEqual([{ role: 'Hàn lâm viện' }])
  })
})
```

- [ ] **Step 2: Tạo transforms.ts**

```ts
// scripts/transforms.ts
export function transformHistoricalNotes(notes: string[]): { note: string }[] {
  return notes.map((note) => ({ note }))
}

export function transformBiaTienSi(raw: any) {
  return {
    order: raw.id,
    year: raw.year,
    dynasty: raw.dynasty,
    erection_year: raw.erection_year,
    candidates_count: parseInt(raw.candidates_count) || undefined,
    passed_count: parseInt(raw.passed_count) || undefined,
    title: raw.title,
    contributors: {
      author: raw.contributors?.author ?? '',
      calligrapher: raw.contributors?.calligrapher ?? '',
      editor: raw.contributors?.editor ?? '',
      engraver: raw.contributors?.engraver ?? '',
    },
    historical_notes: transformHistoricalNotes(raw.historical_notes ?? []),
    biographies: (raw.biographies ?? []).map((bio: any) => ({
      name: bio.name,
      dates: bio.dates ?? '',
      description: bio.description ?? '',
      hometown: bio.hometown ?? '',
      roles: (bio.roles ?? []).map((r: string) => ({ role: r })),
    })),
  }
}
```

- [ ] **Step 3: Chạy test**

```bash
pnpm test
```

Expected: transform tests pass (tổng 12 pass).

- [ ] **Step 4: Tạo seed-bia-tien-si.ts**

```ts
// scripts/seed-bia-tien-si.ts
import path from 'path'
import { fileURLToPath } from 'url'
import { getPayload } from 'payload'
import config from '../src/payload.config'
import { transformBiaTienSi } from './transforms'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const DATA_PATH = path.resolve(__dirname, '../vmqtg-v5/docs/82-van-bia-tien-si.json')

async function main() {
  const payload = await getPayload({ config })
  const raw = await import(DATA_PATH, { assert: { type: 'json' } })
  const data: any[] = raw.default

  console.log(`Seeding ${data.length} bia tiến sĩ...`)

  for (const item of data) {
    const transformed = transformBiaTienSi(item)
    await payload.create({
      collection: 'bia-tien-si',
      data: transformed,
    })
    process.stdout.write('.')
  }

  console.log(`\nDone. ${data.length} records created.`)
  process.exit(0)
}

main().catch((err) => { console.error(err); process.exit(1) })
```

- [ ] **Step 5: Tạo seed-di-tich.ts**

```ts
// scripts/seed-di-tich.ts
// Seed core pages + di-tich items từ dữ liệu vmqtg-v5
import { getPayload } from 'payload'
import config from '../src/payload.config'

// Core pages cần tạo
const CORE_PAGES = [
  {
    slug: 'home',
    title: 'Trang chủ',
    subtitle: 'Di tích lịch sử quốc gia đặc biệt · Hà Nội',
  },
  {
    slug: 'tham-quan',
    title: 'Thông tin tham quan',
    subtitle: 'Vé, giờ mở cửa, nội quy, đường đến và các tiện ích.',
  },
  {
    slug: 've-di-tich',
    title: 'Về di tích',
    subtitle: 'Lịch sử, phân khu, kiến trúc, danh nhân, tượng thờ và thư viện.',
  },
]

// Di tích items từ SITEMAP vmqtg-v5 (rút gọn — đầy đủ 35 items)
const DI_TICH_ITEMS = [
  { id_code: 'B1.1', slug: 'lich-su/thoi-ly', section: 'B1', order: 1, title: 'Thời Lý' },
  { id_code: 'B1.2', slug: 'lich-su/thoi-tran', section: 'B1', order: 2, title: 'Thời Trần' },
  { id_code: 'B1.3', slug: 'lich-su/thoi-le', section: 'B1', order: 3, title: 'Thời Lê' },
  { id_code: 'B1.4', slug: 'lich-su/thoi-nguyen', section: 'B1', order: 4, title: 'Thời Nguyễn' },
  { id_code: 'B2.1', slug: 'phan-khu/noi-tu', section: 'B2', order: 1, title: 'Nội tự' },
  { id_code: 'B2.2', slug: 'phan-khu/vuon-giam', section: 'B2', order: 2, title: 'Vườn Giám' },
  { id_code: 'B2.3', slug: 'phan-khu/ho-van', section: 'B2', order: 3, title: 'Hồ Văn' },
  { id_code: 'B3.1', slug: 'kien-truc/bia-ha-ma', section: 'B3', order: 1, title: 'Bia Hạ mã' },
  { id_code: 'B3.2', slug: 'kien-truc/cong-van-mieu', section: 'B3', order: 2, title: 'Cổng Văn Miếu' },
  { id_code: 'B3.3', slug: 'kien-truc/cong-dai-trung', section: 'B3', order: 3, title: 'Cổng Đại Trung' },
  { id_code: 'B3.4', slug: 'kien-truc/khue-van-cac', section: 'B3', order: 4, title: 'Khuê Văn Các' },
  { id_code: 'B3.5', slug: 'kien-truc/nha-che-bia', section: 'B3', order: 5, title: 'Nhà che bia' },
  { id_code: 'B3.6', slug: 'kien-truc/cong-dai-thanh', section: 'B3', order: 6, title: 'Cổng Đại Thành' },
  { id_code: 'B3.7', slug: 'kien-truc/bai-duong', section: 'B3', order: 7, title: 'Bái đường' },
  { id_code: 'B3.8', slug: 'kien-truc/cong-thai-hoc', section: 'B3', order: 8, title: 'Cổng Thái học' },
  { id_code: 'B3.9', slug: 'kien-truc/thai-hoc', section: 'B3', order: 9, title: 'Thái học' },
  { id_code: 'B3.10', slug: 'kien-truc/nha-chuong-trong', section: 'B3', order: 10, title: 'Nhà chuông, nhà trống' },
  { id_code: 'B3.11', slug: 'kien-truc/nha-bat-giac', section: 'B3', order: 11, title: 'Nhà Bát Giác' },
  { id_code: 'B3.12', slug: 'kien-truc/phuong-dinh', section: 'B3', order: 12, title: 'Phương đình' },
  { id_code: 'B4.1', slug: 'danh-nhan/vua-ly-thanh-tong', section: 'B4', order: 1, title: 'Vua Lý Thánh Tông' },
  { id_code: 'B4.2', slug: 'danh-nhan/vua-ly-nhan-tong', section: 'B4', order: 2, title: 'Vua Lý Nhân Tông' },
  { id_code: 'B4.3', slug: 'danh-nhan/vua-le-thanh-tong', section: 'B4', order: 3, title: 'Vua Lê Thánh Tông' },
  { id_code: 'B4.5', slug: 'danh-nhan/chu-van-an', section: 'B4', order: 5, title: 'Tư nghiệp Chu Văn An' },
  { id_code: 'B4.6', slug: 'danh-nhan/khoa-bang', section: 'B4', order: 6, title: 'Danh nhân khoa bảng' },
]

async function main() {
  const payload = await getPayload({ config })

  console.log('Seeding core pages...')
  for (const page of CORE_PAGES) {
    await payload.create({ collection: 'pages', data: { ...page, status: 'published' } })
    console.log(`  ✓ ${page.slug}`)
  }

  console.log('Seeding di tích items...')
  for (const item of DI_TICH_ITEMS) {
    await payload.create({
      collection: 'di-tich-items',
      data: { ...item, status: 'published' },
    })
    process.stdout.write('.')
  }

  // Seed main navigation
  console.log('Seeding navigation...')
  await payload.create({
    collection: 'navigation',
    data: {
      key: 'main-nav',
      items: [
        { label: 'Tham quan', href: '/tham-quan', mega_menu: false, children: [] },
        {
          label: 'Về di tích', href: '/ve-di-tich', mega_menu: true,
          children: [
            { label: 'Lịch sử', href: '/ve-di-tich', group_id: 'B1' },
            { label: 'Các phân khu', href: '/ve-di-tich', group_id: 'B2' },
            { label: 'Kiến trúc', href: '/ve-di-tich', group_id: 'B3' },
            { label: 'Danh nhân', href: '/ve-di-tich', group_id: 'B4' },
            { label: 'Tượng thờ', href: '/ve-di-tich', group_id: 'B5' },
            { label: 'Thư viện', href: '/ve-di-tich', group_id: 'B6' },
          ],
        },
        { label: '82 Bia Tiến Sĩ', href: '/bia-tien-si', mega_menu: false, children: [] },
      ],
    },
  })

  console.log(`\nDone. ${CORE_PAGES.length} pages + ${DI_TICH_ITEMS.length} items + 1 navigation created.`)
  process.exit(0)
}

main().catch((err) => { console.error(err); process.exit(1) })
```

- [ ] **Step 6: Tạo migrate-media.ts**

```ts
// scripts/migrate-media.ts
import path from 'path'
import fs from 'fs'
import { fileURLToPath } from 'url'
import { getPayload } from 'payload'
import config from '../src/payload.config'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const IMAGES_DIR = path.resolve(__dirname, '../vmqtg-v5/assets/images')

async function getAllImages(dir: string): Promise<string[]> {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
  const files: string[] = []
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      files.push(...await getAllImages(fullPath))
    } else if (/\.(jpg|jpeg|png|webp)$/i.test(entry.name)) {
      files.push(fullPath)
    }
  }
  return files
}

async function main() {
  const payload = await getPayload({ config })
  const images = await getAllImages(IMAGES_DIR)
  console.log(`Migrating ${images.length} images...`)

  for (const imgPath of images) {
    const filename = path.basename(imgPath)
    const buffer = fs.readFileSync(imgPath)
    const blob = new Blob([buffer])
    const file = new File([blob], filename, { type: 'image/jpeg' })

    await payload.create({
      collection: 'media',
      data: { alt: filename.replace(/\.[^.]+$/, '').replace(/-/g, ' ') },
      file: { data: buffer, mimetype: 'image/jpeg', name: filename, size: buffer.length },
    })
    process.stdout.write('.')
  }

  console.log(`\nDone. ${images.length} images uploaded.`)
  process.exit(0)
}

main().catch((err) => { console.error(err); process.exit(1) })
```

- [ ] **Step 7: Chạy seeds (sau khi DB đã setup)**

```bash
# Đảm bảo DATABASE_URI đã set trong .env.local và DB accessible
pnpm seed:bia
pnpm seed:ditich
pnpm migrate:media
```

Expected mỗi script: chạy xong in ra số records created, không có error.

- [ ] **Step 8: Commit**

```bash
git add vmqtg-production/scripts/
git commit -m "feat: add migration scripts for bia-tien-si, di-tich, and media"
```

---

## Task 7: Homepage

**Files:**
- Create: `src/app/(frontend)/[locale]/page.tsx`
- Create: `src/components/features/DiTichCard.tsx`

- [ ] **Step 1: Tạo DiTichCard component**

```tsx
// src/components/features/DiTichCard.tsx
import Link from 'next/link'
import Image from 'next/image'
import { Badge } from '@/components/ui/Badge'
import type { Locale } from '@/lib/i18n'

type Props = {
  id_code: string
  title: string
  subtitle?: string
  section: string
  slug: string
  locale: Locale
  imageUrl?: string
}

export function DiTichCard({ id_code, title, subtitle, section, slug, locale, imageUrl }: Props) {
  return (
    <Link
      href={`/${locale}/ve-di-tich/${slug}`}
      className="group block bg-[--color-bg-subtle] border border-[--color-border] hover:border-[--color-gold] transition-colors"
    >
      {imageUrl && (
        <div className="aspect-[4/3] overflow-hidden bg-[--color-border]">
          <Image
            src={imageUrl}
            alt={title}
            width={400}
            height={300}
            className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
          />
        </div>
      )}
      <div className="p-4">
        <div className="flex items-center gap-2 mb-2">
          <Badge variant="muted">{section}</Badge>
          <span className="font-mono text-xs text-[--color-ink-muted]">{id_code}</span>
        </div>
        <h3 className="font-serif text-base font-semibold text-[--color-ink] group-hover:text-[--color-gold] transition-colors">
          {title}
        </h3>
        {subtitle && <p className="mt-1 text-xs text-[--color-ink-muted] line-clamp-2">{subtitle}</p>}
      </div>
    </Link>
  )
}
```

- [ ] **Step 2: Tạo trang chủ**

```tsx
// src/app/(frontend)/[locale]/page.tsx
import Link from 'next/link'
import Image from 'next/image'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { DiTichCard } from '@/components/features/DiTichCard'
import type { Metadata } from 'next'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title: locale === 'en'
      ? 'Temple of Literature – Imperial Academy'
      : locale === 'fr'
      ? 'Temple de la Littérature – Académie Impériale'
      : 'Văn Miếu – Quốc Tử Giám',
  }
}

export default async function HomePage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()

  // Lấy 6 di tích items nổi bật (B3 kiến trúc)
  const featured = await payload.find({
    collection: 'di-tich-items',
    where: { section: { equals: 'B3' }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 6,
    sort: 'order',
  })

  const HERO_TEXTS = {
    vi: {
      title: 'Văn Miếu – Quốc Tử Giám',
      sub: 'Di tích lịch sử quốc gia đặc biệt · Trường đại học đầu tiên của Việt Nam · 82 Bia tiến sĩ — Di sản tư liệu UNESCO',
      cta: 'Tham quan',
      cta2: 'Khám phá di tích',
    },
    en: {
      title: 'Temple of Literature – Imperial Academy',
      sub: 'Special National Heritage · First university of Vietnam · 82 Doctoral Stelae — UNESCO Memory of the World',
      cta: 'Plan your visit',
      cta2: 'Explore the site',
    },
    fr: {
      title: 'Temple de la Littérature – Académie Impériale',
      sub: 'Patrimoine national spécial · Première université du Vietnam · 82 stèles doctorales — Mémoire du monde UNESCO',
      cta: 'Préparer votre visite',
      cta2: 'Explorer le site',
    },
  }

  const t = HERO_TEXTS[locale as Locale]

  return (
    <div>
      {/* Hero */}
      <section className="relative h-[70vh] min-h-[480px] flex items-end bg-[--color-ink]">
        <Image
          src="/media/hero.jpg"
          alt="Văn Miếu – Quốc Tử Giám"
          fill
          className="object-cover opacity-60"
          priority
        />
        <div className="relative container pb-16">
          <h1 className="font-serif text-4xl md:text-5xl font-bold text-white max-w-2xl leading-tight mb-4">
            {t.title}
          </h1>
          <p className="text-sm text-white/80 max-w-xl mb-8">{t.sub}</p>
          <div className="flex gap-4">
            <Link
              href={`/${locale}/tham-quan`}
              className="px-6 py-3 bg-[--color-red-son] text-white text-sm hover:opacity-90 transition-opacity"
            >
              {t.cta}
            </Link>
            <Link
              href={`/${locale}/ve-di-tich`}
              className="px-6 py-3 border border-white text-white text-sm hover:bg-white hover:text-[--color-ink] transition-colors"
            >
              {t.cta2}
            </Link>
          </div>
        </div>
      </section>

      {/* Featured architecture */}
      <section className="container mt-[--spacing-section]">
        <div className="flex items-baseline justify-between mb-8">
          <h2 className="font-serif text-2xl font-semibold">
            {locale === 'vi' ? 'Công trình kiến trúc' : locale === 'en' ? 'Architecture' : 'Architecture'}
          </h2>
          <Link href={`/${locale}/ve-di-tich`} className="text-sm text-[--color-gold] hover:underline">
            {locale === 'vi' ? 'Xem tất cả →' : locale === 'en' ? 'View all →' : 'Voir tout →'}
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {featured.docs.map((item: any) => (
            <DiTichCard
              key={item.id}
              id_code={item.id_code}
              title={item.title}
              subtitle={item.subtitle}
              section={item.section}
              slug={item.slug}
              locale={locale as Locale}
            />
          ))}
        </div>
      </section>

      {/* Quick info strip */}
      <section className="mt-[--spacing-section] bg-[--color-bg-subtle] border-y border-[--color-border]">
        <div className="container py-10 grid grid-cols-1 sm:grid-cols-3 gap-8">
          {[
            { label: locale === 'vi' ? 'Giờ mở cửa' : locale === 'en' ? 'Opening hours' : 'Horaires', value: '8:00 – 17:00' },
            { label: locale === 'vi' ? 'Địa chỉ' : locale === 'en' ? 'Address' : 'Adresse', value: '58 Quốc Tử Giám, Hà Nội' },
            { label: locale === 'vi' ? 'Vé vào cửa' : locale === 'en' ? 'Admission' : 'Entrée', value: '30.000 VND' },
          ].map((info) => (
            <div key={info.label}>
              <dt className="text-xs text-[--color-ink-muted] uppercase tracking-wider mb-1">{info.label}</dt>
              <dd className="font-serif text-lg">{info.value}</dd>
            </div>
          ))}
        </div>
      </section>

      {/* 82 Bia CTA */}
      <section className="container mt-[--spacing-section] mb-[--spacing-section]">
        <div className="border border-[--color-border] p-8 md:p-12 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <h2 className="font-serif text-2xl font-semibold mb-2">
              {locale === 'vi' ? '82 Bia Tiến Sĩ' : locale === 'en' ? '82 Doctoral Stelae' : '82 Stèles doctorales'}
            </h2>
            <p className="text-sm text-[--color-ink-muted] max-w-lg">
              {locale === 'vi'
                ? 'Ghi danh 1307 tiến sĩ từ năm 1442–1779. Di sản tư liệu thế giới UNESCO từ năm 2010.'
                : locale === 'en'
                ? '1,307 doctoral graduates from 1442–1779. UNESCO Memory of the World since 2010.'
                : '1 307 docteurs de 1442 à 1779. Mémoire du monde de l\'UNESCO depuis 2010.'}
            </p>
          </div>
          <Link
            href={`/${locale}/bia-tien-si`}
            className="shrink-0 px-6 py-3 bg-[--color-gold] text-white text-sm hover:opacity-90 transition-opacity"
          >
            {locale === 'vi' ? 'Khám phá bia tiến sĩ →' : locale === 'en' ? 'Explore stelae →' : 'Explorer les stèles →'}
          </Link>
        </div>
      </section>
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
```

- [ ] **Step 3: Kiểm tra trang chủ**

```bash
pnpm dev
```

Mở `http://localhost:3000/vi` → thấy hero section, featured cards (nếu đã seed), quick info strip, 82 bia CTA.

- [ ] **Step 4: Commit**

```bash
git add vmqtg-production/src/app/\(frontend\)/\[locale\]/page.tsx \
        vmqtg-production/src/components/features/DiTichCard.tsx
git commit -m "feat: add homepage with hero, featured architecture, and 82 bia CTA"
```

---

## Task 8: Tham Quan Page

**Files:**
- Create: `src/app/(frontend)/[locale]/tham-quan/page.tsx`

- [ ] **Step 1: Tạo trang Tham quan**

```tsx
// src/app/(frontend)/[locale]/tham-quan/page.tsx
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { RichText } from '@/components/ui/RichText'
import type { Metadata } from 'next'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title: locale === 'vi' ? 'Thông tin tham quan | Văn Miếu'
      : locale === 'en' ? 'Visitor Information | Temple of Literature'
      : 'Informations pratiques | Temple de la Littérature',
  }
}

export default async function ThamQuanPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'pages',
    where: { slug: { equals: 'tham-quan' }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 1,
  })

  const page = result.docs[0]

  const QUICK_INFO = {
    vi: [
      { label: 'Giờ mở cửa', value: 'Thứ 2–Chủ nhật: 8:00–17:00', sub: 'Mở cửa tất cả các ngày trong năm' },
      { label: 'Vé vào cửa', value: '30.000 đồng / người lớn', sub: '15.000 đồng / học sinh, sinh viên · Miễn phí trẻ em dưới 15 tuổi' },
      { label: 'Địa chỉ', value: '58 Quốc Tử Giám, Văn Miếu, Đống Đa, Hà Nội', sub: 'Cách Hồ Hoàn Kiếm ~3km' },
      { label: 'Điện thoại', value: '024.3747.1322', sub: 'vanmieuqtg@hanoi.gov.vn' },
    ],
    en: [
      { label: 'Opening hours', value: 'Mon–Sun: 8:00–17:00', sub: 'Open every day of the year' },
      { label: 'Admission', value: '30,000 VND / adult', sub: '15,000 VND / students · Free for children under 15' },
      { label: 'Address', value: '58 Quoc Tu Giam St., Van Mieu, Dong Da, Hanoi', sub: 'About 3km from Hoan Kiem Lake' },
      { label: 'Phone', value: '024.3747.1322', sub: 'vanmieuqtg@hanoi.gov.vn' },
    ],
    fr: [
      { label: 'Horaires', value: 'Lun–Dim : 8h00–17h00', sub: 'Ouvert tous les jours de l\'année' },
      { label: 'Tarifs', value: '30 000 VND / adulte', sub: '15 000 VND / étudiants · Gratuit enfants < 15 ans' },
      { label: 'Adresse', value: '58 rue Quoc Tu Giam, Quartier Van Mieu, Dong Da, Hanoï', sub: 'À environ 3 km du lac Hoan Kiem' },
      { label: 'Téléphone', value: '024.3747.1322', sub: 'vanmieuqtg@hanoi.gov.vn' },
    ],
  }

  const info = QUICK_INFO[locale as Locale]

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      {/* Page header */}
      <div className="mb-10">
        <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
          {page?.title ?? (locale === 'vi' ? 'Thông tin tham quan' : locale === 'en' ? 'Visitor Information' : 'Informations pratiques')}
        </h1>
        {page?.subtitle && <p className="text-[--color-ink-muted]">{page.subtitle}</p>}
      </div>

      {/* Quick info grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-12">
        {info.map((item) => (
          <div key={item.label} className="border border-[--color-border] p-6">
            <dt className="text-xs text-[--color-ink-muted] uppercase tracking-wider mb-2">{item.label}</dt>
            <dd className="font-serif text-lg font-medium mb-1">{item.value}</dd>
            <p className="text-xs text-[--color-ink-muted]">{item.sub}</p>
          </div>
        ))}
      </div>

      <div className="divider-motif" />

      {/* Rich text content từ Payload */}
      {page?.content ? (
        <div className="prose max-w-none">
          <RichText content={page.content as any} />
        </div>
      ) : (
        <p className="text-[--color-ink-muted] text-sm italic">
          {locale === 'vi' ? 'Nội dung đang được cập nhật.'
           : locale === 'en' ? 'Content is being updated.'
           : 'Contenu en cours de mise à jour.'}
        </p>
      )}
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
```

- [ ] **Step 2: Kiểm tra trang**

```bash
pnpm dev
```

Mở `/vi/tham-quan` → thấy 4 info cards (giờ mở cửa, vé, địa chỉ, điện thoại) và rich text content (hoặc placeholder nếu chưa có content trong Payload).

- [ ] **Step 3: Commit**

```bash
git add vmqtg-production/src/app/\(frontend\)/\[locale\]/tham-quan/
git commit -m "feat: add Tham Quan page with visitor info cards"
```

---

## Task 9: Về Di Tích Pages

**Files:**
- Create: `src/app/(frontend)/[locale]/ve-di-tich/page.tsx`
- Create: `src/app/(frontend)/[locale]/ve-di-tich/[slug]/page.tsx`

- [ ] **Step 1: Tạo Về di tích overview page**

```tsx
// src/app/(frontend)/[locale]/ve-di-tich/page.tsx
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { DiTichCard } from '@/components/features/DiTichCard'
import { Badge } from '@/components/ui/Badge'

type Props = { params: Promise<{ locale: string }> }

const SECTION_LABELS: Record<string, Record<Locale, string>> = {
  B1: { vi: 'Lịch sử', en: 'History', fr: 'Histoire' },
  B2: { vi: 'Các phân khu', en: 'Site sectors', fr: 'Secteurs' },
  B3: { vi: 'Công trình kiến trúc', en: 'Architecture', fr: 'Architecture' },
  B4: { vi: 'Danh nhân', en: 'Eminent figures', fr: 'Personnages éminents' },
  B5: { vi: 'Tượng thờ', en: 'Statues of worship', fr: 'Statues vénérées' },
  B6: { vi: 'Thư viện', en: 'Library', fr: 'Bibliothèque' },
}

export default async function VeDiTichPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'di-tich-items',
    where: { status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 100,
    sort: 'order',
  })

  // Group by section
  const grouped = result.docs.reduce((acc: Record<string, any[]>, item: any) => {
    if (!acc[item.section]) acc[item.section] = []
    acc[item.section].push(item)
    return acc
  }, {})

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
        {locale === 'vi' ? 'Về di tích' : locale === 'en' ? 'About the Site' : 'À propos du site'}
      </h1>
      <p className="text-[--color-ink-muted] mb-12">
        {locale === 'vi' ? 'Lịch sử, phân khu, kiến trúc, danh nhân, tượng thờ và thư viện.'
         : locale === 'en' ? 'History, sectors, architecture, eminent figures, statues, and library.'
         : 'Histoire, secteurs, architecture, personnages, statues et bibliothèque.'}
      </p>

      {['B1', 'B2', 'B3', 'B4', 'B5', 'B6'].map((section) => {
        const items = grouped[section]
        if (!items?.length) return null
        return (
          <section key={section} className="mb-16">
            <div className="flex items-center gap-3 mb-6">
              <Badge variant="gold">{section}</Badge>
              <h2 className="font-serif text-xl font-semibold">
                {SECTION_LABELS[section]?.[locale as Locale] ?? section}
              </h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {items.map((item: any) => (
                <DiTichCard
                  key={item.id}
                  id_code={item.id_code}
                  title={item.title}
                  subtitle={item.subtitle}
                  section={item.section}
                  slug={item.slug}
                  locale={locale as Locale}
                />
              ))}
            </div>
            <div className="divider-motif" />
          </section>
        )
      })}
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
```

- [ ] **Step 2: Tạo dynamic item page**

```tsx
// src/app/(frontend)/[locale]/ve-di-tich/[slug]/page.tsx
import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { RichText } from '@/components/ui/RichText'
import { Badge } from '@/components/ui/Badge'
import type { Metadata } from 'next'

type Props = { params: Promise<{ locale: string; slug: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params
  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'di-tich-items',
    where: { slug: { equals: slug } },
    locale: locale as Locale,
    limit: 1,
  })
  const item = result.docs[0]
  return { title: item?.title ? `${item.title} | Văn Miếu` : 'Văn Miếu' }
}

export default async function DiTichItemPage({ params }: Props) {
  const { locale, slug } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'di-tich-items',
    where: { slug: { equals: slug }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 1,
    depth: 2,
  })

  const item = result.docs[0]
  if (!item) notFound()

  const firstImage = item.images?.[0]?.image

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      {/* Breadcrumb */}
      <nav className="flex gap-2 text-xs text-[--color-ink-muted] mb-8">
        <Link href={`/${locale}`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? 'Trang chủ' : 'Home'}
        </Link>
        <span>›</span>
        <Link href={`/${locale}/ve-di-tich`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? 'Về di tích' : locale === 'en' ? 'About' : 'À propos'}
        </Link>
        <span>›</span>
        <span>{item.title}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2">
          <div className="flex items-center gap-3 mb-4">
            <Badge variant="gold">{item.section}</Badge>
            <span className="font-mono text-xs text-[--color-ink-muted]">{item.id_code}</span>
          </div>
          <h1 className="font-serif text-3xl md:text-4xl font-bold mb-4">{item.title}</h1>
          {item.subtitle && <p className="text-lg text-[--color-ink-muted] mb-8">{item.subtitle}</p>}

          <div className="divider-motif" />

          {item.content ? (
            <div className="prose max-w-none">
              <RichText content={item.content as any} />
            </div>
          ) : (
            <p className="text-[--color-ink-muted] text-sm italic">
              {locale === 'vi' ? 'Nội dung đang được cập nhật.'
               : locale === 'en' ? 'Content is being updated.'
               : 'Contenu en cours de mise à jour.'}
            </p>
          )}
        </div>

        {/* Sidebar images */}
        <div className="space-y-4">
          {item.images?.map((img: any, i: number) => (
            img.image && (
              <div key={i} className="border border-[--color-border]">
                <Image
                  src={`/media/${img.image.filename}`}
                  alt={img.image.alt ?? item.title}
                  width={400}
                  height={300}
                  className="w-full object-cover"
                />
                {img.caption && (
                  <p className="text-xs text-[--color-ink-muted] p-3">{img.caption}</p>
                )}
              </div>
            )
          ))}
        </div>
      </div>
    </div>
  )
}

export async function generateStaticParams() {
  const payload = await getPayloadClient()
  const result = await payload.find({ collection: 'di-tich-items', limit: 100 })
  return result.docs.flatMap((item: any) =>
    ['vi', 'en', 'fr'].map((locale) => ({ locale, slug: item.slug }))
  )
}
```

- [ ] **Step 3: Kiểm tra pages**

```bash
pnpm dev
```

Mở `/vi/ve-di-tich` → thấy items grouped theo section (nếu đã seed). Click vào một item → trang chi tiết với breadcrumb, title, content placeholder.

- [ ] **Step 4: Commit**

```bash
git add vmqtg-production/src/app/\(frontend\)/\[locale\]/ve-di-tich/
git commit -m "feat: add Ve Di Tich overview and dynamic item pages"
```

---

## Task 10: Bia Tiến Sĩ Pages

**Files:**
- Create: `src/app/(frontend)/[locale]/bia-tien-si/page.tsx`
- Create: `src/app/(frontend)/[locale]/bia-tien-si/[id]/page.tsx`
- Create: `src/components/features/BiaTienSiCard.tsx`

- [ ] **Step 1: Tạo BiaTienSiCard**

```tsx
// src/components/features/BiaTienSiCard.tsx
import Link from 'next/link'
import { Badge } from '@/components/ui/Badge'
import type { Locale } from '@/lib/i18n'

type Props = {
  order: number
  year: string
  dynasty: string
  title: string
  passed_count?: number
  locale: Locale
}

export function BiaTienSiCard({ order, year, dynasty, title, passed_count, locale }: Props) {
  return (
    <Link
      href={`/${locale}/bia-tien-si/${order}`}
      className="group block border border-[--color-border] hover:border-[--color-gold] p-5 transition-colors"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <span className="font-mono text-2xl font-bold text-[--color-border] group-hover:text-[--color-gold] transition-colors">
          {String(order).padStart(2, '0')}
        </span>
        <Badge variant="muted">{dynasty}</Badge>
      </div>
      <div className="font-mono text-xs text-[--color-gold] mb-1">{year}</div>
      <h3 className="font-serif text-sm leading-snug group-hover:text-[--color-gold] transition-colors line-clamp-3">
        {title}
      </h3>
      {passed_count && (
        <p className="mt-2 text-xs text-[--color-ink-muted]">
          {passed_count} {locale === 'vi' ? 'tiến sĩ' : locale === 'en' ? 'graduates' : 'docteurs'}
        </p>
      )}
    </Link>
  )
}
```

- [ ] **Step 2: Tạo trang danh sách 82 bia**

```tsx
// src/app/(frontend)/[locale]/bia-tien-si/page.tsx
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { BiaTienSiCard } from '@/components/features/BiaTienSiCard'
import type { Metadata } from 'next'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title: locale === 'vi' ? '82 Bia Tiến Sĩ | Văn Miếu'
      : locale === 'en' ? '82 Doctoral Stelae | Temple of Literature'
      : '82 Stèles doctorales | Temple de la Littérature',
  }
}

export default async function BiaTienSiPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'bia-tien-si',
    locale: locale as Locale,
    limit: 82,
    sort: 'order',
  })

  // Group by dynasty
  const dynasties = [...new Set(result.docs.map((b: any) => b.dynasty))]

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      <div className="max-w-2xl mb-12">
        <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
          {locale === 'vi' ? '82 Bia Tiến Sĩ' : locale === 'en' ? '82 Doctoral Stelae' : '82 Stèles doctorales'}
        </h1>
        <p className="text-[--color-ink-muted]">
          {locale === 'vi'
            ? 'Ghi danh 1.307 tiến sĩ từ năm 1442 đến 1779. Di sản tư liệu thế giới UNESCO từ năm 2010.'
            : locale === 'en'
            ? '1,307 doctoral graduates from 1442 to 1779. UNESCO Memory of the World since 2010.'
            : '1 307 docteurs de 1442 à 1779. Mémoire du monde de l\'UNESCO depuis 2010.'}
        </p>
      </div>

      {dynasties.map((dynasty) => {
        const biaOfDynasty = result.docs.filter((b: any) => b.dynasty === dynasty)
        return (
          <section key={dynasty as string} className="mb-12">
            <h2 className="font-serif text-lg font-semibold mb-4 flex items-center gap-3">
              <span className="h-px flex-1 bg-[--color-border]" />
              <span>{dynasty as string}</span>
              <span className="h-px flex-1 bg-[--color-border]" />
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {biaOfDynasty.map((bia: any) => (
                <BiaTienSiCard
                  key={bia.id}
                  order={bia.order}
                  year={bia.year}
                  dynasty={bia.dynasty}
                  title={bia.title}
                  passed_count={bia.passed_count}
                  locale={locale as Locale}
                />
              ))}
            </div>
          </section>
        )
      })}
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
```

- [ ] **Step 3: Tạo trang chi tiết 1 bia**

```tsx
// src/app/(frontend)/[locale]/bia-tien-si/[id]/page.tsx
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { Badge } from '@/components/ui/Badge'
import type { Metadata } from 'next'

type Props = { params: Promise<{ locale: string; id: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, id } = await params
  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'bia-tien-si',
    where: { order: { equals: parseInt(id) } },
    locale: locale as Locale,
    limit: 1,
  })
  const bia = result.docs[0]
  return { title: bia?.title ? `${bia.title} | Văn Miếu` : 'Văn Miếu' }
}

export default async function BiaTienSiDetailPage({ params }: Props) {
  const { locale, id } = await params
  if (!isValidLocale(locale)) notFound()

  const order = parseInt(id)
  if (isNaN(order) || order < 1 || order > 82) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'bia-tien-si',
    where: { order: { equals: order } },
    locale: locale as Locale,
    limit: 1,
    depth: 1,
  })

  const bia = result.docs[0]
  if (!bia) notFound()

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      {/* Breadcrumb */}
      <nav className="flex gap-2 text-xs text-[--color-ink-muted] mb-8">
        <Link href={`/${locale}`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? 'Trang chủ' : 'Home'}
        </Link>
        <span>›</span>
        <Link href={`/${locale}/bia-tien-si`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? '82 Bia Tiến Sĩ' : locale === 'en' ? '82 Stelae' : '82 Stèles'}
        </Link>
        <span>›</span>
        <span>{locale === 'vi' ? `Bia số ${order}` : `Stele #${order}`}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2">
          {/* Header */}
          <div className="flex items-center gap-3 mb-4">
            <span className="font-mono text-4xl font-bold text-[--color-border]">
              {String(order).padStart(2, '0')}
            </span>
            <div>
              <Badge variant="muted">{bia.dynasty}</Badge>
              <div className="font-mono text-sm text-[--color-gold] mt-1">{bia.year}</div>
            </div>
          </div>
          <h1 className="font-serif text-2xl md:text-3xl font-bold mb-6 leading-snug">{bia.title}</h1>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-8">
            {[
              { label: locale === 'vi' ? 'Năm thi' : 'Exam year', value: bia.year },
              { label: locale === 'vi' ? 'Triều đại' : 'Dynasty', value: bia.dynasty },
              { label: locale === 'vi' ? 'Năm dựng bia' : 'Erected', value: bia.erection_year },
              { label: locale === 'vi' ? 'Số thí sinh' : 'Candidates', value: bia.candidates_count },
              { label: locale === 'vi' ? 'Số đỗ' : 'Graduates', value: bia.passed_count },
            ].filter((s) => s.value).map((stat) => (
              <div key={stat.label} className="border border-[--color-border] p-4">
                <dt className="text-xs text-[--color-ink-muted] mb-1">{stat.label}</dt>
                <dd className="font-mono text-sm font-semibold">{stat.value}</dd>
              </div>
            ))}
          </div>

          {/* Historical notes */}
          {bia.historical_notes?.length > 0 && (
            <>
              <div className="divider-motif" />
              <h2 className="font-serif text-lg font-semibold mb-4">
                {locale === 'vi' ? 'Ghi chú lịch sử' : locale === 'en' ? 'Historical notes' : 'Notes historiques'}
              </h2>
              <ul className="space-y-3">
                {bia.historical_notes.map((item: any, i: number) => (
                  <li key={i} className="flex gap-3 text-sm">
                    <span className="shrink-0 font-mono text-xs text-[--color-gold] mt-0.5">{String(i + 1).padStart(2, '0')}</span>
                    <p className="text-[--color-ink-muted] leading-relaxed">{item.note}</p>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

        {/* Sidebar — biographies */}
        <div>
          <h2 className="font-serif text-lg font-semibold mb-4 border-b border-[--color-border] pb-3">
            {locale === 'vi' ? 'Danh nhân tiêu biểu' : locale === 'en' ? 'Notable graduates' : 'Personnages notables'}
          </h2>
          <div className="space-y-6">
            {bia.biographies?.slice(0, 5).map((bio: any, i: number) => (
              <div key={i} className="border-b border-[--color-border] pb-4 last:border-0">
                <h3 className="font-serif text-sm font-semibold">{bio.name}</h3>
                {bio.dates && <p className="font-mono text-xs text-[--color-gold] mb-1">{bio.dates}</p>}
                {bio.description && <p className="text-xs text-[--color-ink-muted] leading-relaxed mb-2">{bio.description}</p>}
                {bio.roles?.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {bio.roles.slice(0, 3).map((r: any, j: number) => (
                      <Badge key={j} variant="muted">{r.role}</Badge>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Navigate prev/next */}
          <div className="flex justify-between mt-8 pt-4 border-t border-[--color-border]">
            {order > 1 && (
              <Link href={`/${locale}/bia-tien-si/${order - 1}`} className="text-xs text-[--color-gold] hover:underline">
                ← {locale === 'vi' ? `Bia ${order - 1}` : `Stele ${order - 1}`}
              </Link>
            )}
            {order < 82 && (
              <Link href={`/${locale}/bia-tien-si/${order + 1}`} className="text-xs text-[--color-gold] hover:underline ml-auto">
                {locale === 'vi' ? `Bia ${order + 1}` : `Stele ${order + 1}`} →
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export async function generateStaticParams() {
  const locales = ['vi', 'en', 'fr']
  return locales.flatMap((locale) =>
    Array.from({ length: 82 }, (_, i) => ({ locale, id: String(i + 1) }))
  )
}
```

- [ ] **Step 4: Kiểm tra**

```bash
pnpm dev
```

Mở `/vi/bia-tien-si` → thấy 82 bia grouped theo triều đại. Click vào bia 1 → thấy stats, historical notes, biographies, prev/next navigation.

- [ ] **Step 5: Commit**

```bash
git add vmqtg-production/src/app/\(frontend\)/\[locale\]/bia-tien-si/ \
        vmqtg-production/src/components/features/BiaTienSiCard.tsx
git commit -m "feat: add 82 Bia Tien Si list and detail pages"
```

---

## Task 11: Vercel Deployment

**Files:**
- Create: `vmqtg-production/vercel.json`
- Modify: `vmqtg-production/.env.local` → set production env vars in Vercel dashboard

- [ ] **Step 1: Tạo vercel.json**

```json
{
  "buildCommand": "pnpm build",
  "installCommand": "pnpm install",
  "framework": "nextjs",
  "regions": ["sin1"]
}
```

> `sin1` = Singapore — gần Việt Nam nhất trong Vercel regions.

- [ ] **Step 2: Build local để kiểm tra lỗi**

```bash
cd vmqtg-production && pnpm build
```

Expected: build thành công, không có TypeScript errors. Fix bất kỳ lỗi nào trước khi deploy.

- [ ] **Step 3: Push lên GitHub**

```bash
git add vmqtg-production/vercel.json
git commit -m "feat: add Vercel deployment config"
git push origin claude/reverent-lamarr-5441b8
```

- [ ] **Step 4: Deploy lên Vercel**

1. Mở [vercel.com](https://vercel.com) → Add New Project
2. Import repo từ GitHub
3. Set **Root Directory**: `vmqtg-production`
4. Set environment variables:
   ```
   DATABASE_URI     = <Neon connection string>
   PAYLOAD_SECRET   = <random 32+ char string>
   NEXT_PUBLIC_SITE_URL = https://<your-vercel-url>.vercel.app
   ```
5. Click Deploy

- [ ] **Step 5: Kiểm tra deploy**

Sau khi deploy xong:
- Mở `https://<project>.vercel.app` → redirect về `/vi`
- Mở `/vi/admin` → tạo admin user, xác nhận 5 collections có mặt
- Chạy seeds từ local (trỏ vào Neon DB production):
  ```bash
  DATABASE_URI="<neon-url>" pnpm seed:bia
  DATABASE_URI="<neon-url>" pnpm seed:ditich
  ```
- Mở `/vi/bia-tien-si` → thấy 82 bia
- Mở `/vi/ve-di-tich` → thấy di tích items

- [ ] **Step 6: Commit final**

```bash
git add -A && git commit -m "feat: complete MVP production deployment"
```

---

## Checklist tổng

- [ ] Project scaffolding + Tailwind + Vitest
- [ ] Design tokens, fonts, base components
- [ ] Payload config + 5 collections + tests
- [ ] i18n middleware + locale utilities + tests
- [ ] Layout: Header, Footer, MegaMenu, LanguageSwitcher
- [ ] Migration scripts: bia-tien-si, di-tich, media
- [ ] Homepage
- [ ] Tham quan page
- [ ] Về di tích overview + dynamic [slug] page
- [ ] 82 Bia tiến sĩ list + [id] detail page
- [ ] Vercel deployment
