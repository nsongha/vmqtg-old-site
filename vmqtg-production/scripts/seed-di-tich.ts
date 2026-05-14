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
      data: { ...item, status: 'published' } as any,
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
