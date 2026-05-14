'use client'

import Image from 'next/image'
import { useState, useMemo, useCallback } from 'react'

type MediaItem = {
  id: string
  url: string
  filename: string
  alt?: string
  caption?: string
  category?: string
  sizes?: {
    thumbnail?: { url: string }
    card?: { url: string }
  }
}

type Category = {
  value: string
  label: { vi: string; en: string; fr: string }
}

const CATEGORIES: Category[] = [
  { value: 'kien-truc', label: { vi: 'Kiến trúc', en: 'Architecture', fr: 'Architecture' } },
  { value: 'lich-su', label: { vi: 'Lịch sử', en: 'History', fr: 'Histoire' } },
  { value: 'danh-nhan', label: { vi: 'Danh nhân', en: 'Figures', fr: 'Personnages' } },
  { value: 'tuong-tho', label: { vi: 'Tượng thờ', en: 'Statues', fr: 'Statues' } },
  { value: 'hoat-dong', label: { vi: 'Hoạt động', en: 'Activities', fr: 'Activités' } },
  { value: 'khac', label: { vi: 'Khác', en: 'Other', fr: 'Autre' } },
]

const UI = {
  vi: {
    search: 'Tìm kiếm ảnh...',
    all: 'Tất cả',
    noResults: 'Không tìm thấy ảnh phù hợp.',
    close: 'Đóng',
    prev: 'Trước',
    next: 'Tiếp',
    count: (n: number) => `${n} ảnh`,
  },
  en: {
    search: 'Search photos...',
    all: 'All',
    noResults: 'No photos found.',
    close: 'Close',
    prev: 'Previous',
    next: 'Next',
    count: (n: number) => `${n} photo${n !== 1 ? 's' : ''}`,
  },
  fr: {
    search: 'Rechercher des photos...',
    all: 'Tout',
    noResults: 'Aucune photo trouvée.',
    close: 'Fermer',
    prev: 'Précédent',
    next: 'Suivant',
    count: (n: number) => `${n} photo${n !== 1 ? 's' : ''}`,
  },
}

type Locale = 'vi' | 'en' | 'fr'

export function SearchGallery({ items, locale }: { items: MediaItem[]; locale: Locale }) {
  const t = UI[locale]
  const [query, setQuery] = useState('')
  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [lightbox, setLightbox] = useState<{ index: number } | null>(null)

  const filtered = useMemo(() => {
    let result = items
    if (activeCategory) {
      result = result.filter((item) => item.category === activeCategory)
    }
    if (query.trim()) {
      const q = query.trim().toLowerCase()
      result = result.filter(
        (item) =>
          item.alt?.toLowerCase().includes(q) ||
          item.caption?.toLowerCase().includes(q) ||
          item.filename?.toLowerCase().includes(q),
      )
    }
    return result
  }, [items, query, activeCategory])

  const openLightbox = useCallback((index: number) => setLightbox({ index }), [])
  const closeLightbox = useCallback(() => setLightbox(null), [])
  const prevImage = useCallback(() =>
    setLightbox((lb) => lb ? { index: (lb.index - 1 + filtered.length) % filtered.length } : null), [filtered.length])
  const nextImage = useCallback(() =>
    setLightbox((lb) => lb ? { index: (lb.index + 1) % filtered.length } : null), [filtered.length])

  const currentItem = lightbox !== null ? filtered[lightbox.index] : null

  return (
    <>
      {/* Controls */}
      <div className="flex flex-col gap-4 mb-8">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t.search}
          className="w-full max-w-md px-4 py-2.5 border border-[--color-border] bg-white text-sm focus:outline-none focus:border-[--color-gold] rounded-none"
        />
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setActiveCategory(null)}
            className={`px-3 py-1.5 text-xs border transition-colors ${
              activeCategory === null
                ? 'bg-[--color-ink] text-white border-[--color-ink]'
                : 'border-[--color-border] text-[--color-ink-muted] hover:border-[--color-gold] hover:text-[--color-gold]'
            }`}
          >
            {t.all}
          </button>
          {CATEGORIES.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setActiveCategory(cat.value === activeCategory ? null : cat.value)}
              className={`px-3 py-1.5 text-xs border transition-colors ${
                activeCategory === cat.value
                  ? 'bg-[--color-gold] text-white border-[--color-gold]'
                  : 'border-[--color-border] text-[--color-ink-muted] hover:border-[--color-gold] hover:text-[--color-gold]'
              }`}
            >
              {cat.label[locale]}
            </button>
          ))}
        </div>
        <p className="text-xs text-[--color-ink-muted]">{t.count(filtered.length)}</p>
      </div>

      {/* Grid */}
      {filtered.length === 0 ? (
        <p className="text-sm text-[--color-ink-muted] py-12 text-center">{t.noResults}</p>
      ) : (
        <div className="columns-2 sm:columns-3 lg:columns-4 gap-3 space-y-3">
          {filtered.map((item, index) => (
            <button
              key={item.id}
              onClick={() => openLightbox(index)}
              className="relative w-full block overflow-hidden group focus:outline-none focus-visible:ring-2 focus-visible:ring-[--color-gold]"
              aria-label={item.alt || item.filename}
            >
              <div className="relative w-full">
                <Image
                  src={item.sizes?.thumbnail?.url || item.url}
                  alt={item.alt || item.filename}
                  width={400}
                  height={300}
                  className="w-full h-auto object-cover group-hover:opacity-90 transition-opacity"
                  unoptimized
                />
                {item.caption && (
                  <div className="absolute inset-x-0 bottom-0 bg-black/60 px-2 py-1.5 translate-y-full group-hover:translate-y-0 transition-transform">
                    <p className="text-white text-[11px] leading-snug line-clamp-2">{item.caption}</p>
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Lightbox */}
      {lightbox !== null && currentItem && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center"
          onClick={closeLightbox}
          role="dialog"
          aria-modal="true"
        >
          {/* Close */}
          <button
            onClick={closeLightbox}
            className="absolute top-4 right-4 text-white/70 hover:text-white text-sm px-3 py-1.5 border border-white/20 hover:border-white/60 transition-colors"
          >
            {t.close} ✕
          </button>

          {/* Prev */}
          {filtered.length > 1 && (
            <button
              onClick={(e) => { e.stopPropagation(); prevImage() }}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-white/70 hover:text-white text-sm px-3 py-2 border border-white/20 hover:border-white/60 transition-colors"
            >
              ← {t.prev}
            </button>
          )}

          {/* Image */}
          <div
            className="relative max-w-4xl max-h-[85vh] mx-16"
            onClick={(e) => e.stopPropagation()}
          >
            <Image
              src={currentItem.sizes?.card?.url || currentItem.url}
              alt={currentItem.alt || currentItem.filename}
              width={800}
              height={600}
              className="max-h-[80vh] w-auto h-auto object-contain"
              unoptimized
            />
            {(currentItem.alt || currentItem.caption) && (
              <div className="mt-3 text-center">
                {currentItem.alt && (
                  <p className="text-white font-serif text-sm">{currentItem.alt}</p>
                )}
                {currentItem.caption && (
                  <p className="text-white/60 text-xs mt-1">{currentItem.caption}</p>
                )}
              </div>
            )}
            <p className="text-center text-white/40 text-xs mt-2">
              {lightbox.index + 1} / {filtered.length}
            </p>
          </div>

          {/* Next */}
          {filtered.length > 1 && (
            <button
              onClick={(e) => { e.stopPropagation(); nextImage() }}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-white/70 hover:text-white text-sm px-3 py-2 border border-white/20 hover:border-white/60 transition-colors"
            >
              {t.next} →
            </button>
          )}
        </div>
      )}
    </>
  )
}
