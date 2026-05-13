import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { HtmlContent } from '@/components/ui/HtmlContent'
import { RichText } from '@/components/ui/RichText'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

const SLUG = 'hoat-dong'
const TITLES = {
  vi: 'Các hoạt động | Văn Miếu',
  en: 'Activities | Temple of Literature',
  fr: 'Activités | Temple de la Littérature',
} as const

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return { title: TITLES[locale as Locale] ?? TITLES.vi }
}

export default async function Page({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'pages',
    where: { slug: { equals: SLUG }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 1,
  })
  const page = result.docs[0]

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      <div className="mb-10">
        <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
          {page?.title ?? 'Các hoạt động'}
        </h1>
        {page?.subtitle && <p className="text-[--color-ink-muted]">{page.subtitle}</p>}
      </div>
      <div className="divider-motif" />
      {(page as any)?.content_html ? (
        <HtmlContent html={(page as any).content_html} />
      ) : page?.content ? (
        <div className="prose max-w-none"><RichText content={page.content as any} /></div>
      ) : (
        <p className="text-[--color-ink-muted] text-sm italic">
          {locale === 'vi' ? 'Nội dung đang được cập nhật.'
            : locale === 'en' ? 'Content is being updated.'
            : 'Contenu en cours de mise à jour.'}
        </p>
      )}
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
