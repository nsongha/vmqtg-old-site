// scripts/seed-on-build.ts
// Idempotent, best-effort seed run during Vercel build.
// Each collection is checked: if empty, seed it. If non-empty, skip.
// Errors are logged but never thrown — build must not fail because of seed.

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { getPayload } from 'payload'
import config from '../src/payload.config'
import { transformBiaTienSi } from './transforms'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const DATA_DIR = path.resolve(__dirname, '../data')

const CORE_PAGES = [
  { slug: 'home', title: 'Trang chủ', subtitle: 'Di tích lịch sử quốc gia đặc biệt · Hà Nội' },
  { slug: 'tham-quan', title: 'Thông tin tham quan', subtitle: 'Vé, giờ mở cửa, nội quy, đường đến và các tiện ích.' },
  { slug: 've-di-tich', title: 'Về di tích', subtitle: 'Lịch sử, phân khu, kiến trúc, danh nhân, tượng thờ và thư viện.' },
]

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

const NAV_ITEMS = [
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
]

async function getCount(payload: any, collection: string): Promise<number> {
  try {
    const result = await payload.count({ collection })
    return result.totalDocs ?? 0
  } catch {
    return 0
  }
}

async function seedBia(payload: any) {
  const jsonPath = path.join(DATA_DIR, 'bia-tien-si.json')
  if (!fs.existsSync(jsonPath)) {
    console.log('[seed] bia-tien-si.json not found, skip')
    return
  }
  const data: any[] = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'))
  console.log(`[seed] bia: creating ${data.length} records`)
  for (const item of data) {
    try {
      await payload.create({ collection: 'bia-tien-si', data: transformBiaTienSi(item) })
    } catch (e: any) {
      console.error(`[seed] bia ${item.id} failed:`, e.message)
    }
  }
}

async function seedPages(payload: any) {
  for (const page of CORE_PAGES) {
    try {
      await payload.create({ collection: 'pages', data: { ...page, status: 'published' } })
    } catch (e: any) {
      console.error(`[seed] page ${page.slug} failed:`, e.message)
    }
  }
}

async function seedDiTich(payload: any) {
  console.log(`[seed] di-tich: creating ${DI_TICH_ITEMS.length} records`)
  for (const item of DI_TICH_ITEMS) {
    try {
      await payload.create({ collection: 'di-tich-items', data: { ...item, status: 'published' } as any })
    } catch (e: any) {
      console.error(`[seed] di-tich ${item.id_code} failed:`, e.message)
    }
  }
}

async function seedNavigation(payload: any) {
  try {
    await payload.create({
      collection: 'navigation',
      data: { key: 'main-nav', items: NAV_ITEMS } as any,
    })
  } catch (e: any) {
    console.error('[seed] navigation failed:', e.message)
  }
}

async function getAllImages(dir: string): Promise<string[]> {
  if (!fs.existsSync(dir)) return []
  const out: string[] = []
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) out.push(...await getAllImages(full))
    else if (/\.(jpe?g|png|webp)$/i.test(entry.name)) out.push(full)
  }
  return out
}

async function seedMedia(payload: any) {
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    console.log('[seed] media: BLOB_READ_WRITE_TOKEN missing, skip (ephemeral filesystem would lose uploads)')
    return
  }
  const imagesDir = path.join(DATA_DIR, 'images')
  const files = await getAllImages(imagesDir)
  console.log(`[seed] media: uploading ${files.length} images to Vercel Blob`)
  for (const filepath of files) {
    const filename = path.basename(filepath)
    try {
      const buffer = fs.readFileSync(filepath)
      const ext = path.extname(filename).toLowerCase()
      const mimetype = ext === '.png' ? 'image/png' : ext === '.webp' ? 'image/webp' : 'image/jpeg'
      await payload.create({
        collection: 'media',
        data: { alt: filename.replace(/\.[^.]+$/, '').replace(/-/g, ' ') },
        file: { data: buffer, mimetype, name: filename, size: buffer.length },
      })
    } catch (e: any) {
      console.error(`[seed] media ${filename} failed:`, e.message)
    }
  }
}

async function main() {
  console.log('[seed] starting build-time seed check')
  const payload = await getPayload({ config })

  const counts = {
    bia: await getCount(payload, 'bia-tien-si'),
    pages: await getCount(payload, 'pages'),
    diTich: await getCount(payload, 'di-tich-items'),
    nav: await getCount(payload, 'navigation'),
    media: await getCount(payload, 'media'),
  }
  console.log('[seed] existing counts:', counts)

  if (counts.bia === 0) await seedBia(payload)
  else console.log('[seed] bia: already has data, skip')

  if (counts.pages === 0) await seedPages(payload)
  else console.log('[seed] pages: already has data, skip')

  if (counts.diTich === 0) await seedDiTich(payload)
  else console.log('[seed] di-tich: already has data, skip')

  if (counts.nav === 0) await seedNavigation(payload)
  else console.log('[seed] navigation: already has data, skip')

  if (counts.media === 0) await seedMedia(payload)
  else console.log('[seed] media: already has data, skip')

  console.log('[seed] done')
  process.exit(0)
}

main().catch((err) => {
  console.error('[seed] fatal error, but continuing build:', err)
  process.exit(0) // never fail the build
})
