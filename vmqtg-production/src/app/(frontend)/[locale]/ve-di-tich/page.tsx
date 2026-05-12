import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { DiTichCard } from '@/components/features/DiTichCard'
import { Badge } from '@/components/ui/Badge'

export const dynamic = 'force-dynamic'

type Props = { params: Promise<{ locale: string }> }

const SECTION_LABELS: Record<string, Record<Locale, string>> = {
  B1: { vi: 'Lịch sử', en: 'History', fr: 'Histoire' },
  B2: { vi: 'Các phân khu', en: 'Site sectors', fr: 'Secteurs' },
  B3: { vi: 'Công trình kiến trúc', en: 'Architecture', fr: 'Architecture' },
  B4: { vi: 'Danh nhân', en: 'Eminent figures', fr: 'Personnages éminents' },
  B5: { vi: 'Tượng thờ', en: 'Statues of worship', fr: 'Statues vénérées' },
  B6: { vi: 'Thư viện', en: 'Library', fr: 'Bibliothèque' },
}

export default async function VeDiTichPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'di-tich-items',
    where: { status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 100,
    sort: 'order',
  })

  // Group by section
  const grouped = result.docs.reduce((acc: Record<string, any[]>, item: any) => {
    if (!acc[item.section]) acc[item.section] = []
    acc[item.section].push(item)
    return acc
  }, {})

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
        {locale === 'vi' ? 'Về di tích' : locale === 'en' ? 'About the Site' : 'À propos du site'}
      </h1>
      <p className="text-[--color-ink-muted] mb-12">
        {locale === 'vi' ? 'Lịch sử, phân khu, kiến trúc, danh nhân, tượng thờ và thư viện.'
         : locale === 'en' ? 'History, sectors, architecture, eminent figures, statues, and library.'
         : 'Histoire, secteurs, architecture, personnages, statues et bibliothèque.'}
      </p>

      {['B1', 'B2', 'B3', 'B4', 'B5', 'B6'].map((section) => {
        const items = grouped[section]
        if (!items?.length) return null
        return (
          <section key={section} className="mb-16">
            <div className="flex items-center gap-3 mb-6">
              <Badge variant="gold">{section}</Badge>
              <h2 className="font-serif text-xl font-semibold">
                {SECTION_LABELS[section]?.[locale as Locale] ?? section}
              </h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {items.map((item: any) => (
                <DiTichCard
                  key={item.id}
                  id_code={item.id_code}
                  title={item.title}
                  subtitle={item.subtitle}
                  section={item.section}
                  slug={item.slug}
                  locale={locale as Locale}
                />
              ))}
            </div>
            <div className="divider-motif" />
          </section>
        )
      })}
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
