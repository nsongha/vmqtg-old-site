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
