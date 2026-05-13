import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { RichText } from '@/components/ui/RichText'
import { HtmlContent } from '@/components/ui/HtmlContent'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title: locale === 'vi' ? 'Thông tin tham quan | Văn Miếu'
      : locale === 'en' ? 'Visitor Information | Temple of Literature'
      : 'Informations pratiques | Temple de la Littérature',
  }
}

export default async function ThamQuanPage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'pages',
    where: { slug: { equals: 'tham-quan' }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 1,
  })

  const page = result.docs[0]

  const QUICK_INFO = {
    vi: [
      { label: 'Giờ mở cửa', value: 'Thứ 2–Chủ nhật: 8:00–17:00', sub: 'Mở cửa tất cả các ngày trong năm' },
      { label: 'Vé vào cửa', value: '30.000 đồng / người lớn', sub: '15.000 đồng / học sinh, sinh viên · Miễn phí trẻ em dưới 15 tuổi' },
      { label: 'Địa chỉ', value: '58 Quốc Tử Giám, Văn Miếu, Đống Đa, Hà Nội', sub: 'Cách Hồ Hoàn Kiếm ~3km' },
      { label: 'Điện thoại', value: '024.3747.1322', sub: 'vanmieuqtg@hanoi.gov.vn' },
    ],
    en: [
      { label: 'Opening hours', value: 'Mon–Sun: 8:00–17:00', sub: 'Open every day of the year' },
      { label: 'Admission', value: '30,000 VND / adult', sub: '15,000 VND / students · Free for children under 15' },
      { label: 'Address', value: '58 Quoc Tu Giam St., Van Mieu, Dong Da, Hanoi', sub: 'About 3km from Hoan Kiem Lake' },
      { label: 'Phone', value: '024.3747.1322', sub: 'vanmieuqtg@hanoi.gov.vn' },
    ],
    fr: [
      { label: 'Horaires', value: 'Lun–Dim : 8h00–17h00', sub: 'Ouvert tous les jours de l\'année' },
      { label: 'Tarifs', value: '30 000 VND / adulte', sub: '15 000 VND / étudiants · Gratuit enfants < 15 ans' },
      { label: 'Adresse', value: '58 rue Quoc Tu Giam, Quartier Van Mieu, Dong Da, Hanoï', sub: 'À environ 3 km du lac Hoan Kiem' },
      { label: 'Téléphone', value: '024.3747.1322', sub: 'vanmieuqtg@hanoi.gov.vn' },
    ],
  }

  const info = QUICK_INFO[locale as Locale]

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      {/* Page header */}
      <div className="mb-10">
        <h1 className="font-serif text-3xl md:text-4xl font-bold mb-3">
          {page?.title ?? (locale === 'vi' ? 'Thông tin tham quan' : locale === 'en' ? 'Visitor Information' : 'Informations pratiques')}
        </h1>
        {page?.subtitle && <p className="text-[--color-ink-muted]">{page.subtitle}</p>}
      </div>

      {/* Quick info grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-12">
        {info.map((item) => (
          <div key={item.label} className="border border-[--color-border] p-6">
            <dt className="text-xs text-[--color-ink-muted] uppercase tracking-wider mb-2">{item.label}</dt>
            <dd className="font-serif text-lg font-medium mb-1">{item.value}</dd>
            <p className="text-xs text-[--color-ink-muted]">{item.sub}</p>
          </div>
        ))}
      </div>

      <div className="divider-motif" />

      {/* Content từ Payload — content_html (legacy/seeded) ưu tiên hơn richText */}
      {(page as any)?.content_html ? (
        <HtmlContent html={(page as any).content_html} />
      ) : page?.content ? (
        <div className="prose max-w-none">
          <RichText content={page.content as any} />
        </div>
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
