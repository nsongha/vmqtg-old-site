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
  { slug: 'giao-duc-di-san', title: 'Giáo dục di sản', subtitle: 'Các chương trình giáo dục dành cho mọi lứa tuổi từ mầm non đến THPT.' },
  { slug: 'hoat-dong', title: 'Các hoạt động', subtitle: 'Hoạt động trưng bày, triển lãm thường xuyên tại di tích.' },
  { slug: 'bia-tien-si', title: '82 Bia Tiến Sĩ', subtitle: 'Di sản tư liệu thế giới UNESCO · 1.307 tiến sĩ từ 1442–1779.' },
  { slug: 've-chung-toi', title: 'Về chúng tôi', subtitle: 'Trung tâm hoạt động VHKH Văn Miếu – Quốc Tử Giám.' },
  { slug: 'trung-bay-trien-lam', title: 'Trưng bày, triển lãm', subtitle: 'Trưng bày cố định, chuyên đề và các triển lãm tại di tích.' },
  { slug: 'dich-vu', title: 'Dịch vụ', subtitle: 'Tour đêm, audio guide, thuyết minh, quà lưu niệm, viết thư pháp.' },
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
  // B5 — tượng thờ (statues of worship)
  { id_code: 'B5.1', slug: 'tuong-tho/khong-tu', section: 'B5', order: 1, title: 'Khổng Tử' },
  { id_code: 'B5.2', slug: 'tuong-tho/nhan-tu', section: 'B5', order: 2, title: 'Nhan Tử' },
  { id_code: 'B5.3', slug: 'tuong-tho/tu-tu', section: 'B5', order: 3, title: 'Tử Tư' },
  { id_code: 'B5.4', slug: 'tuong-tho/tang-tu', section: 'B5', order: 4, title: 'Tăng Tử' },
  { id_code: 'B5.5', slug: 'tuong-tho/manh-tu', section: 'B5', order: 5, title: 'Mạnh Tử' },
  // B6 — thư viện (library)
  { id_code: 'B6.1', slug: 'thu-vien/thu-vien-anh', section: 'B6', order: 1, title: 'Thư viện ảnh' },
  { id_code: 'B6.2', slug: 'thu-vien/video', section: 'B6', order: 2, title: 'Video' },
]

// Map di-tich slug → media filename (in data/images/) for cover image
const DI_TICH_IMAGE_MAP: Record<string, string> = {
  // B1 - lich-su
  'lich-su/thoi-ly': '1-toan-canh-van-mieu-quoc-tu-giam-dau-the-ky-xx-copy.jpg',
  'lich-su/thoi-tran': '2-tu-tru-va-ho-van-phia-truoc-van-mieu-quoc-tu-giam.jpg',
  'lich-su/thoi-le': '10-nha-bia-tien-si-ben-tay.jpg',
  'lich-su/thoi-nguyen': '30-cong-thai-hoc.jpg',
  // B2 - phan-khu
  'phan-khu/noi-tu': 'san-dai-bai-va-nha-dai-bai.jpg',
  'phan-khu/vuon-giam': 'khu-vuon-bia-ts-ben-dong.jpg',
  'phan-khu/ho-van': 'ho-van.jpg',
  // B3 - kien-truc
  'kien-truc/bia-ha-ma': '5-bia-ha-ma.jpg',
  'kien-truc/cong-van-mieu': 'cong-vm-mat-truoc.jpg',
  'kien-truc/cong-dai-trung': 'cong-dai-trung.jpg',
  'kien-truc/khue-van-cac': 'kvc-va-gieng-thien-quang.jpg',
  'kien-truc/nha-che-bia': 'nha-bia.jpg',
  'kien-truc/cong-dai-thanh': 'cong-dai-thanh.jpg',
  'kien-truc/bai-duong': 'toa-bai-duong.jpg',
  'kien-truc/cong-thai-hoc': 'cong-thai-hoc-2.jpg',
  'kien-truc/thai-hoc': 'cong-dat-tai.jpg',
  'kien-truc/nha-chuong-trong': 'lau-trong.jpg',
  'kien-truc/nha-bat-giac': 'nha-bat-giac-vuon-giam.jpg',
  'kien-truc/phuong-dinh': 'gieng-thien-quang.jpg',
  // B4 - danh-nhan
  'danh-nhan/vua-ly-thanh-tong': '7-ly-thanh-tong.jpg',
  'danh-nhan/vua-ly-nhan-tong': '8-ly-nhan-tong.jpg',
  'danh-nhan/vua-le-thanh-tong': '9-lethanhtong.jpg',
  'danh-nhan/chu-van-an': '6-chu-van-an.jpg',
  'danh-nhan/khoa-bang': '1-nha-tho-trang-nguyen-nguyen-truc-xa-tam-hung-thanh-oai-ha-noi-anh-p-ncst.jpg',
}

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
  { label: 'Giáo dục di sản', href: '/giao-duc-di-san', mega_menu: false, children: [] },
  { label: 'Các hoạt động', href: '/hoat-dong', mega_menu: false, children: [] },
  { label: 'Trưng bày, triển lãm', href: '/trung-bay-trien-lam', mega_menu: false, children: [] },
  { label: 'Dịch vụ', href: '/dich-vu', mega_menu: false, children: [] },
  { label: 'Về chúng tôi', href: '/ve-chung-toi', mega_menu: false, children: [] },
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
  // Idempotent: create each page only if its slug is missing.
  for (const page of CORE_PAGES) {
    try {
      const existing = await payload.find({
        collection: 'pages',
        where: { slug: { equals: page.slug } },
        limit: 1,
        depth: 0,
      })
      if (existing.docs.length > 0) continue
      await payload.create({ collection: 'pages', data: { ...page, status: 'published' } })
      console.log(`[seed] created page ${page.slug}`)
    } catch (e: any) {
      console.error(`[seed] page ${page.slug} failed:`, e.message)
    }
  }
}

async function seedDiTich(payload: any) {
  // Idempotent upsert: skip records whose id_code already exists.
  let created = 0
  for (const item of DI_TICH_ITEMS) {
    try {
      const existing = await payload.find({
        collection: 'di-tich-items',
        where: { id_code: { equals: item.id_code } },
        limit: 1,
        depth: 0,
      })
      if (existing.docs.length > 0) continue
      await payload.create({ collection: 'di-tich-items', data: { ...item, status: 'published' } as any })
      created++
    } catch (e: any) {
      console.error(`[seed] di-tich ${item.id_code} failed:`, e.message)
    }
  }
  console.log(`[seed] di-tich: created ${created} new records (${DI_TICH_ITEMS.length - created} already present)`)
}

async function seedNavigation(payload: any) {
  // Idempotent: upsert by key='main-nav'. Refresh items so newly added Pages
  // (giao-duc-di-san, hoat-dong, ve-chung-toi…) appear in the menu after redeploy.
  try {
    const existing = await payload.find({
      collection: 'navigation',
      where: { key: { equals: 'main-nav' } },
      limit: 1,
      depth: 0,
    })
    if (existing.docs.length > 0) {
      await payload.update({
        collection: 'navigation',
        id: existing.docs[0].id,
        data: { items: NAV_ITEMS } as any,
      })
      console.log('[seed] navigation: refreshed main-nav items')
    } else {
      await payload.create({
        collection: 'navigation',
        data: { key: 'main-nav', items: NAV_ITEMS } as any,
      })
      console.log('[seed] navigation: created main-nav')
    }
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

async function linkDiTichImages(payload: any) {
  // Idempotent: only update items where images is empty
  const items = await payload.find({ collection: 'di-tich-items', limit: 100 })
  let linked = 0
  for (const item of items.docs) {
    const hasImage = Array.isArray(item.images) && item.images.length > 0
    if (hasImage) continue
    const filename = DI_TICH_IMAGE_MAP[item.slug]
    if (!filename) continue
    try {
      const media = await payload.find({
        collection: 'media',
        where: { filename: { equals: filename } },
        limit: 1,
      })
      if (media.docs.length === 0) {
        console.log(`[seed] link: media ${filename} not found for ${item.slug}`)
        continue
      }
      await payload.update({
        collection: 'di-tich-items',
        id: item.id,
        data: { images: [{ image: media.docs[0].id }] } as any,
      })
      linked++
    } catch (e: any) {
      console.error(`[seed] link ${item.slug} failed:`, e.message)
    }
  }
  console.log(`[seed] linked ${linked} di-tich items to images`)
}

type LocalizedHtml = { slug: string; vi: string | null; en: string | null; fr: string | null }
type OldsiteContent = { pages: LocalizedHtml[]; diTich: LocalizedHtml[] }

function loadOldsiteContent(): OldsiteContent | null {
  const p = path.resolve(DATA_DIR, 'oldsite-content.json')
  if (!fs.existsSync(p)) return null
  try {
    return JSON.parse(fs.readFileSync(p, 'utf-8'))
  } catch (e: any) {
    console.error('[seed] failed to parse oldsite-content.json:', e.message)
    return null
  }
}

// Fill empty content_html fields per locale from oldsite extraction.
// Preserves any admin-edited content_html. Safe to re-run.
async function fillContentFromOldsite(
  payload: any,
  collection: 'pages' | 'di-tich-items',
  entries: LocalizedHtml[],
) {
  let filled = 0
  for (const entry of entries) {
    const existing = await payload.find({
      collection,
      where: { slug: { equals: entry.slug } },
      limit: 1,
      depth: 0,
    })
    if (existing.docs.length === 0) continue
    const docId = existing.docs[0].id
    for (const locale of ['vi', 'en', 'fr'] as const) {
      const html = entry[locale]
      if (!html) continue
      try {
        const current = await payload.findByID({ collection, id: docId, locale, depth: 0 })
        if (current?.content_html) continue
        await payload.update({
          collection,
          id: docId,
          locale,
          data: { content_html: html },
        })
        filled++
      } catch (e: any) {
        console.error(`[seed] fill ${collection}/${entry.slug}/${locale} failed:`, e.message)
      }
    }
  }
  console.log(`[seed] ${collection}: filled ${filled} localized content_html fields`)
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

  // Pages: always run — seedPages is now idempotent and adds new slugs over time.
  await seedPages(payload)

  // di-tich: always run — seedDiTich is now idempotent and adds new sections
  // (B5 tượng thờ, B6 thư viện) over time.
  await seedDiTich(payload)

  // Navigation: always run — seedNavigation is now idempotent and refreshes items.
  await seedNavigation(payload)

  if (counts.media === 0) await seedMedia(payload)
  else console.log('[seed] media: already has data, skip')

  // After media + di-tich both seeded, link them (idempotent — fills only empty images)
  if (counts.media > 0 || (await getCount(payload, 'media')) > 0) {
    await linkDiTichImages(payload)
  }

  // Fill localized content_html from oldsite extraction (idempotent)
  const oldsite = loadOldsiteContent()
  if (oldsite) {
    await fillContentFromOldsite(payload, 'pages', oldsite.pages)
    await fillContentFromOldsite(payload, 'di-tich-items', oldsite.diTich)
  } else {
    console.log('[seed] no oldsite-content.json found, skip content fill')
  }

  console.log('[seed] done')
  process.exit(0)
}

main().catch((err) => {
  console.error('[seed] fatal error, but continuing build:', err)
  process.exit(0) // never fail the build
})
