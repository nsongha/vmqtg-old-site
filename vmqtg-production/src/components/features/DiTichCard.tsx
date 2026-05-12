// src/components/features/DiTichCard.tsx
import Link from 'next/link'
import Image from 'next/image'
import { Badge } from '@/components/ui/Badge'
import type { Locale } from '@/lib/i18n'

type Props = {
  id_code: string
  title: string
  subtitle?: string
  section: string
  slug: string
  locale: Locale
  imageUrl?: string
}

export function DiTichCard({ id_code, title, subtitle, section, slug, locale, imageUrl }: Props) {
  return (
    <Link
      href={`/${locale}/ve-di-tich/${slug}`}
      className="group block bg-[--color-bg-subtle] border border-[--color-border] hover:border-[--color-gold] transition-colors"
    >
      {imageUrl && (
        <div className="aspect-[4/3] overflow-hidden bg-[--color-border]">
          <Image
            src={imageUrl}
            alt={title}
            width={400}
            height={300}
            className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
          />
        </div>
      )}
      <div className="p-4">
        <div className="flex items-center gap-2 mb-2">
          <Badge variant="muted">{section}</Badge>
          <span className="font-mono text-xs text-[--color-ink-muted]">{id_code}</span>
        </div>
        <h3 className="font-serif text-base font-semibold text-[--color-ink] group-hover:text-[--color-gold] transition-colors">
          {title}
        </h3>
        {subtitle && <p className="mt-1 text-xs text-[--color-ink-muted] line-clamp-2">{subtitle}</p>}
      </div>
    </Link>
  )
}
