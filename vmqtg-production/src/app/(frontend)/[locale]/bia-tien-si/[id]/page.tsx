import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { Badge } from '@/components/ui/Badge'
import type { Metadata } from 'next'

type Props = { params: Promise<{ locale: string; id: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, id } = await params
  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'bia-tien-si',
    where: { order: { equals: parseInt(id) } },
    locale: locale as Locale,
    limit: 1,
  })
  const bia = result.docs[0]
  return { title: bia?.title ? `${bia.title} | Văn Miếu` : 'Văn Miếu' }
}

export default async function BiaTienSiDetailPage({ params }: Props) {
  const { locale, id } = await params
  if (!isValidLocale(locale)) notFound()

  const order = parseInt(id)
  if (isNaN(order) || order < 1 || order > 82) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'bia-tien-si',
    where: { order: { equals: order } },
    locale: locale as Locale,
    limit: 1,
    depth: 1,
  })

  const bia = result.docs[0]
  if (!bia) notFound()

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      {/* Breadcrumb */}
      <nav className="flex gap-2 text-xs text-[--color-ink-muted] mb-8">
        <Link href={`/${locale}`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? 'Trang chủ' : 'Home'}
        </Link>
        <span>›</span>
        <Link href={`/${locale}/bia-tien-si`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? '82 Bia Tiến Sĩ' : locale === 'en' ? '82 Stelae' : '82 Stèles'}
        </Link>
        <span>›</span>
        <span>{locale === 'vi' ? `Bia số ${order}` : `Stele #${order}`}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2">
          {/* Header */}
          <div className="flex items-center gap-3 mb-4">
            <span className="font-mono text-4xl font-bold text-[--color-border]">
              {String(order).padStart(2, '0')}
            </span>
            <div>
              <Badge variant="muted">{bia.dynasty}</Badge>
              <div className="font-mono text-sm text-[--color-gold] mt-1">{bia.year}</div>
            </div>
          </div>
          <h1 className="font-serif text-2xl md:text-3xl font-bold mb-6 leading-snug">{bia.title}</h1>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-8">
            {[
              { label: locale === 'vi' ? 'Năm thi' : 'Exam year', value: bia.year },
              { label: locale === 'vi' ? 'Triều đại' : 'Dynasty', value: bia.dynasty },
              { label: locale === 'vi' ? 'Năm dựng bia' : 'Erected', value: bia.erection_year },
              { label: locale === 'vi' ? 'Số thí sinh' : 'Candidates', value: bia.candidates_count },
              { label: locale === 'vi' ? 'Số đỗ' : 'Graduates', value: bia.passed_count },
            ].filter((s) => s.value).map((stat) => (
              <div key={stat.label} className="border border-[--color-border] p-4">
                <dt className="text-xs text-[--color-ink-muted] mb-1">{stat.label}</dt>
                <dd className="font-mono text-sm font-semibold">{stat.value}</dd>
              </div>
            ))}
          </div>

          {/* Historical notes */}
          {bia.historical_notes?.length > 0 && (
            <>
              <div className="divider-motif" />
              <h2 className="font-serif text-lg font-semibold mb-4">
                {locale === 'vi' ? 'Ghi chú lịch sử' : locale === 'en' ? 'Historical notes' : 'Notes historiques'}
              </h2>
              <ul className="space-y-3">
                {bia.historical_notes.map((item: any, i: number) => (
                  <li key={i} className="flex gap-3 text-sm">
                    <span className="shrink-0 font-mono text-xs text-[--color-gold] mt-0.5">{String(i + 1).padStart(2, '0')}</span>
                    <p className="text-[--color-ink-muted] leading-relaxed">{item.note}</p>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

        {/* Sidebar — biographies */}
        <div>
          <h2 className="font-serif text-lg font-semibold mb-4 border-b border-[--color-border] pb-3">
            {locale === 'vi' ? 'Danh nhân tiêu biểu' : locale === 'en' ? 'Notable graduates' : 'Personnages notables'}
          </h2>
          <div className="space-y-6">
            {bia.biographies?.slice(0, 5).map((bio: any, i: number) => (
              <div key={i} className="border-b border-[--color-border] pb-4 last:border-0">
                <h3 className="font-serif text-sm font-semibold">{bio.name}</h3>
                {bio.dates && <p className="font-mono text-xs text-[--color-gold] mb-1">{bio.dates}</p>}
                {bio.description && <p className="text-xs text-[--color-ink-muted] leading-relaxed mb-2">{bio.description}</p>}
                {bio.roles?.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {bio.roles.slice(0, 3).map((r: any, j: number) => (
                      <Badge key={j} variant="muted">{r.role}</Badge>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Navigate prev/next */}
          <div className="flex justify-between mt-8 pt-4 border-t border-[--color-border]">
            {order > 1 && (
              <Link href={`/${locale}/bia-tien-si/${order - 1}`} className="text-xs text-[--color-gold] hover:underline">
                ← {locale === 'vi' ? `Bia ${order - 1}` : `Stele ${order - 1}`}
              </Link>
            )}
            {order < 82 && (
              <Link href={`/${locale}/bia-tien-si/${order + 1}`} className="text-xs text-[--color-gold] hover:underline ml-auto">
                {locale === 'vi' ? `Bia ${order + 1}` : `Stele ${order + 1}`} →
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export async function generateStaticParams() {
  const locales = ['vi', 'en', 'fr']
  return locales.flatMap((locale) =>
    Array.from({ length: 82 }, (_, i) => ({ locale, id: String(i + 1) }))
  )
}
