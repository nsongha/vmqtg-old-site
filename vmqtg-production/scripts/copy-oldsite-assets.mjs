#!/usr/bin/env node
// Copy ../site/assets into public/oldsite/assets at build time so the
// content_html (which references /oldsite/assets/...) resolves on Vercel.
// Idempotent: skip files already present + identical size.

import { mkdirSync, readdirSync, statSync, copyFileSync, existsSync } from 'node:fs'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const SRC = resolve(__dirname, '../../site/assets')
const DST = resolve(__dirname, '../public/oldsite/assets')

let copied = 0
let skipped = 0

function walk(src, dst) {
  if (!existsSync(src)) {
    console.warn(`[copy-oldsite] source not found: ${src} — skipping`)
    return
  }
  mkdirSync(dst, { recursive: true })
  for (const entry of readdirSync(src, { withFileTypes: true })) {
    const s = join(src, entry.name)
    const d = join(dst, entry.name)
    if (entry.isDirectory()) {
      walk(s, d)
    } else if (entry.isFile()) {
      const srcStat = statSync(s)
      if (existsSync(d) && statSync(d).size === srcStat.size) {
        skipped++
        continue
      }
      copyFileSync(s, d)
      copied++
    }
  }
}

console.log(`[copy-oldsite] ${SRC} → ${DST}`)
walk(SRC, DST)
console.log(`[copy-oldsite] copied ${copied}, skipped ${skipped} (already present)`)
