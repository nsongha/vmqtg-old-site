import { buildConfig } from 'payload'
import { postgresAdapter } from '@payloadcms/db-postgres'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import { revalidatePath } from 'next/cache'
import sharp from 'sharp'
import path from 'path'
import { fileURLToPath } from 'url'

import { Users } from './collections/Users'
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
  admin: {
    user: 'users',
    importMap: {
      baseDir: path.resolve(dirname),
    },
  },
  collections: [
    Users,
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
