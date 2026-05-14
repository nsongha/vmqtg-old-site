import type { CollectionConfig } from 'payload'

export const Media: CollectionConfig = {
  slug: 'media',
  access: {
    read: () => true,
  },
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
    {
      name: 'category',
      type: 'select',
      admin: { position: 'sidebar' },
      options: [
        { label: 'Kiến trúc', value: 'kien-truc' },
        { label: 'Lịch sử', value: 'lich-su' },
        { label: 'Danh nhân', value: 'danh-nhan' },
        { label: 'Tượng thờ', value: 'tuong-tho' },
        { label: 'Hoạt động', value: 'hoat-dong' },
        { label: 'Khác', value: 'khac' },
      ],
    },
  ],
}
