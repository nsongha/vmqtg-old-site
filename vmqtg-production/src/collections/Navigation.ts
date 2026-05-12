import type { CollectionConfig } from 'payload'

export const Navigation: CollectionConfig = {
  slug: 'navigation',
  admin: { useAsTitle: 'key' },
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
