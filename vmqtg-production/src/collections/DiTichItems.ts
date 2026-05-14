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
      name: 'content_html',
      type: 'textarea',
      localized: true,
      admin: {
        description: 'Raw HTML (sanitized at render). Takes precedence over richText when set.',
        rows: 12,
      },
    },
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
