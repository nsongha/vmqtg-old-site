// scripts/migrate-media.ts
import path from 'path'
import fs from 'fs'
import { fileURLToPath } from 'url'
import { getPayload } from 'payload'
import config from '../src/payload.config'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const IMAGES_DIR = path.resolve(__dirname, '../data/images')

async function getAllImages(dir: string): Promise<string[]> {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
  const files: string[] = []
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      files.push(...await getAllImages(fullPath))
    } else if (/\.(jpg|jpeg|png|webp)$/i.test(entry.name)) {
      files.push(fullPath)
    }
  }
  return files
}

async function main() {
  const payload = await getPayload({ config })
  const images = await getAllImages(IMAGES_DIR)
  console.log(`Migrating ${images.length} images...`)

  for (const imgPath of images) {
    const filename = path.basename(imgPath)
    const buffer = fs.readFileSync(imgPath)
    const ext = path.extname(filename).toLowerCase()
    const mimetype = ext === '.png' ? 'image/png' : ext === '.webp' ? 'image/webp' : 'image/jpeg'

    await payload.create({
      collection: 'media',
      data: { alt: filename.replace(/\.[^.]+$/, '').replace(/-/g, ' ') },
      file: { data: buffer, mimetype, name: filename, size: buffer.length },
    })
    process.stdout.write('.')
  }

  console.log(`\nDone. ${images.length} images uploaded.`)
  process.exit(0)
}

main().catch((err) => { console.error(err); process.exit(1) })
