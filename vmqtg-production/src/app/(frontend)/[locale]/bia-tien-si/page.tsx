import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { BiaTienSiCard } from '@/components/features/BiaTienSiCard'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title: locale === 'vi' ? '82 Bia Tiến Sĩ | Văn Miếu'
      : locale === 'en' ? '82 Doctoral Stelae | Temple of Literature'
      : '82 Stèles doctorales | Temple de la Littérature',
  }
}

export default async function BiaTienSiPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'bia-tien-si',
    locale: locale as Locale,
    limit: 82,
    sort: 'order',
  })

  // Group by dynasty
  const dynasties = [...new Set(result.docs.map((b: any) => b.dynasty))] as string[]

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      <div className="max-w-2xl mb-12">
        <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
          {locale === 'vi' ? '82 Bia Tiến Sĩ' : locale === 'en' ? '82 Doctoral Stelae' : '82 Stèles doctorales'}
        </h1>
        <p className="text-[--color-ink-muted]">
          {locale === 'vi'
            ? 'Ghi danh 1.307 tiến sĩ từ năm 1442 đến 1779. Di sản tư liệu thế giới UNESCO từ năm 2010.'
            : locale === 'en'
            ? '1,307 doctoral graduates from 1442 to 1779. UNESCO Memory of the World since 2010.'
            : '1 307 docteurs de 1442 à 1779. Mémoire du monde de l\'UNESCO depuis 2010.'}
        </p>
      </div>

      {dynasties.map((dynasty) => {
        const biaOfDynasty = result.docs.filter((b: any) => b.dynasty === dynasty)
        return (
          <section key={dynasty} className="mb-12">
            <h2 className="font-serif text-lg font-semibold mb-4 flex items-center gap-3">
              <span className="h-px flex-1 bg-[--color-border]" />
              <span>{dynasty}</span>
              <span className="h-px flex-1 bg-[--color-border]" />
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {biaOfDynasty.map((bia: any) => (
                <BiaTienSiCard
                  key={bia.id}
                  order={bia.order}
                  year={bia.year}
                  dynasty={bia.dynasty}
                  title={bia.title}
                  passed_count={bia.passed_count}
                  locale={locale as Locale}
                />
              ))}
            </div>
          </section>
        )
      })}
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
