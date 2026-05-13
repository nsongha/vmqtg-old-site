import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { RichText } from '@/components/ui/RichText'
import { HtmlContent } from '@/components/ui/HtmlContent'
import { Badge } from '@/components/ui/Badge'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

type Props = { params: Promise<{ locale: string; slug: string[] }> }

function joinSlug(parts: string[]): string {
  return parts.join('/')
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params
  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'di-tich-items',
    where: { slug: { equals: joinSlug(slug) } },
    locale: locale as Locale,
    limit: 1,
  })
  const item = result.docs[0]
  return { title: item?.title ? `${item.title} | Văn Miếu` : 'Văn Miếu' }
}

export default async function DiTichItemPage({ params }: Props) {
  const { locale, slug } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()
  const result = await payload.find({
    collection: 'di-tich-items',
    where: { slug: { equals: joinSlug(slug) }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 1,
    depth: 2,
  })

  const item = result.docs[0]
  if (!item) notFound()

  return (
    <div className="container mt-12 mb-[--spacing-section]">
      {/* Breadcrumb */}
      <nav className="flex gap-2 text-xs text-[--color-ink-muted] mb-8">
        <Link href={`/${locale}`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? 'Trang chủ' : 'Home'}
        </Link>
        <span>›</span>
        <Link href={`/${locale}/ve-di-tich`} className="hover:text-[--color-gold]">
          {locale === 'vi' ? 'Về di tích' : locale === 'en' ? 'About' : 'À propos'}
        </Link>
        <span>›</span>
        <span>{item.title}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2">
          <div className="flex items-center gap-3 mb-4">
            <Badge variant="gold">{item.section}</Badge>
            <span className="font-mono text-xs text-[--color-ink-muted]">{item.id_code}</span>
          </div>
          <h1 className="font-serif text-3xl md:text-4xl font-bold mb-4">{item.title}</h1>
          {item.subtitle && <p className="text-lg text-[--color-ink-muted] mb-8">{item.subtitle}</p>}

          <div className="divider-motif" />

          {(item as any).content_html ? (
            <HtmlContent html={(item as any).content_html} />
          ) : item.content ? (
            <div className="prose max-w-none">
              <RichText content={item.content as any} />
            </div>
          ) : (
            <p className="text-[--color-ink-muted] text-sm italic">
              {locale === 'vi' ? 'Nội dung đang được cập nhật.'
               : locale === 'en' ? 'Content is being updated.'
               : 'Contenu en cours de mise à jour.'}
            </p>
          )}
        </div>

        {/* Sidebar images */}
        <div className="space-y-4">
          {item.images?.map((img: any, i: number) => (
            img.image && (
              <div key={i} className="border border-[--color-border]">
                <Image
                  src={img.image.url ?? `/media/${img.image.filename}`}
                  alt={img.image.alt ?? item.title}
                  width={400}
                  height={300}
                  className="w-full object-cover"
                />
                {img.caption && (
                  <p className="text-xs text-[--color-ink-muted] p-3">{img.caption}</p>
                )}
              </div>
            )
          ))}
        </div>
      </div>
    </div>
  )
}

export async function generateStaticParams() {
  try {
    const payload = await getPayloadClient()
    const result = await payload.find({ collection: 'di-tich-items', limit: 100 })
    return result.docs.flatMap((item: any) =>
      ['vi', 'en', 'fr'].map((locale) => ({ locale, slug: String(item.slug).split('/') }))
    )
  } catch {
    return []
  }
}
