import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { SearchGallery } from './SearchGallery'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title:
      locale === 'vi'
        ? 'Thư viện ảnh | Văn Miếu – Quốc Tử Giám'
        : locale === 'en'
          ? 'Photo Library | Temple of Literature'
          : 'Photothèque | Temple de la Littérature',
    description:
      locale === 'vi'
        ? 'Bộ sưu tập ảnh về kiến trúc, lịch sử, danh nhân và hoạt động tại Văn Miếu – Quốc Tử Giám.'
        : locale === 'en'
          ? 'Photo collection of architecture, history, figures and activities at the Temple of Literature.'
          : 'Collection de photos de l\'architecture, de l\'histoire et des activités du Temple de la Littérature.',
  }
}

const HEADING = {
  vi: { title: 'Thư viện ảnh', sub: 'Bộ sưu tập hình ảnh về di tích Văn Miếu – Quốc Tử Giám' },
  en: { title: 'Photo Library', sub: 'Image collection of the Temple of Literature – Imperial Academy' },
  fr: { title: 'Photothèque', sub: 'Collection d\'images du Temple de la Littérature – Académie Impériale' },
}

export default async function ThuVienAnhPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()

  const result = await payload.find({
    collection: 'media',
    locale: locale as Locale,
    limit: 200,
    sort: '-createdAt',
    depth: 0,
  })

  const items = result.docs.map((doc: any) => ({
    id: String(doc.id),
    url: doc.url ?? '',
    filename: doc.filename ?? '',
    alt: doc.alt ?? '',
    caption: doc.caption ?? '',
    category: doc.category ?? null,
    sizes: {
      thumbnail: doc.sizes?.thumbnail?.url ? { url: doc.sizes.thumbnail.url } : undefined,
      card: doc.sizes?.card?.url ? { url: doc.sizes.card.url } : undefined,
    },
  }))

  const t = HEADING[locale as Locale]

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      <div className="mb-10">
        <h1 className="font-serif text-3xl font-semibold mb-2">{t.title}</h1>
        <p className="text-sm text-[--color-ink-muted]">{t.sub}</p>
      </div>
      <SearchGallery items={items} locale={locale as Locale} />
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
