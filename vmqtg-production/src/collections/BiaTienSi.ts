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
