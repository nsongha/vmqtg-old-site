import { buildConfig } from 'payload'
import { postgresAdapter } from '@payloadcms/db-postgres'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import { vercelBlobStorage } from '@payloadcms/storage-vercel-blob'
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
    push: true,
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
  plugins: [
    vercelBlobStorage({
      enabled: Boolean(process.env.BLOB_READ_WRITE_TOKEN),
      collections: { media: true },
      token: process.env.BLOB_READ_WRITE_TOKEN,
    }),
  ],
  secret: process.env.PAYLOAD_SECRET || '',
  sharp,
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
})
