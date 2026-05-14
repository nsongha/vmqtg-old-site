import Link from 'next/link'
import { Badge } from '@/components/ui/Badge'
import type { Locale } from '@/lib/i18n'

type Props = {
  order: number
  year: string
  dynasty: string
  title: string
  passed_count?: number
  locale: Locale
}

export function BiaTienSiCard({ order, year, dynasty, title, passed_count, locale }: Props) {
  return (
    <Link
      href={`/${locale}/bia-tien-si/${order}`}
      className="group block border border-[--color-border] hover:border-[--color-gold] p-5 transition-colors"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <span className="font-mono text-2xl font-bold text-[--color-border] group-hover:text-[--color-gold] transition-colors">
          {String(order).padStart(2, '0')}
        </span>
        <Badge variant="muted">{dynasty}</Badge>
      </div>
      <div className="font-mono text-xs text-[--color-gold] mb-1">{year}</div>
      <h3 className="font-serif text-sm leading-snug group-hover:text-[--color-gold] transition-colors line-clamp-3">
        {title}
      </h3>
      {passed_count && (
        <p className="mt-2 text-xs text-[--color-ink-muted]">
          {passed_count} {locale === 'vi' ? 'tiến sĩ' : locale === 'en' ? 'graduates' : 'docteurs'}
        </p>
      )}
    </Link>
  )
}
