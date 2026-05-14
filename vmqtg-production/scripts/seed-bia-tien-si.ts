// scripts/seed-bia-tien-si.ts
import path from 'path'
import fs from 'fs'
import { fileURLToPath } from 'url'
import { getPayload } from 'payload'
import config from '../src/payload.config'
import { transformBiaTienSi } from './transforms'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const DATA_PATH = path.resolve(__dirname, '../data/bia-tien-si.json')

async function main() {
  const payload = await getPayload({ config })
  const data: any[] = JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'))

  console.log(`Seeding ${data.length} bia tiến sĩ...`)

  for (const item of data) {
    const transformed = transformBiaTienSi(item)
    await payload.create({
      collection: 'bia-tien-si',
      data: transformed,
    })
    process.stdout.write('.')
  }

  console.log(`\nDone. ${data.length} records created.`)
  process.exit(0)
}

main().catch((err) => { console.error(err); process.exit(1) })
