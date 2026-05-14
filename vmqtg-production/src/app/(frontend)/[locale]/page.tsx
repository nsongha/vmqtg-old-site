// src/app/(frontend)/[locale]/page.tsx
import Link from 'next/link'
import Image from 'next/image'
import { notFound } from 'next/navigation'
import { getPayloadClient } from '@/lib/payload'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { DiTichCard } from '@/components/features/DiTichCard'
import { FadeInOnView } from '@/components/ui/FadeInOnView'
import type { Metadata } from 'next'

export const dynamic = 'force-dynamic'

type Props = { params: Promise<{ locale: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params
  return {
    title: locale === 'en'
      ? 'Temple of Literature – Imperial Academy'
      : locale === 'fr'
      ? 'Temple de la Littérature – Académie Impériale'
      : 'Văn Miếu – Quốc Tử Giám',
  }
}

export default async function HomePage({ params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  const payload = await getPayloadClient()

  // Lấy 6 di tích items nổi bật (B3 kiến trúc) + populate images relation
  const featured = await payload.find({
    collection: 'di-tich-items',
    where: { section: { equals: 'B3' }, status: { equals: 'published' } },
    locale: locale as Locale,
    limit: 6,
    sort: 'order',
    depth: 2,
  })

  // Hero image — first try a Media record named hero.jpg (uploaded by seed)
  const heroMedia = await payload.find({
    collection: 'media',
    where: { filename: { equals: 'hero.jpg' } },
    limit: 1,
  })
  const heroUrl: string | undefined = (heroMedia.docs[0] as any)?.url

  const HERO_TEXTS = {
    vi: {
      title: 'Văn Miếu – Quốc Tử Giám',
      sub: 'Di tích lịch sử quốc gia đặc biệt · Trường đại học đầu tiên của Việt Nam · 82 Bia tiến sĩ — Di sản tư liệu UNESCO',
      cta: 'Tham quan',
      cta2: 'Khám phá di tích',
    },
    en: {
      title: 'Temple of Literature – Imperial Academy',
      sub: 'Special National Heritage · First university of Vietnam · 82 Doctoral Stelae — UNESCO Memory of the World',
      cta: 'Plan your visit',
      cta2: 'Explore the site',
    },
    fr: {
      title: 'Temple de la Littérature – Académie Impériale',
      sub: 'Patrimoine national spécial · Première université du Vietnam · 82 stèles doctorales — Mémoire du monde UNESCO',
      cta: 'Préparer votre visite',
      cta2: 'Explorer le site',
    },
  }

  const t = HERO_TEXTS[locale as Locale]

  return (
    <div>
      {/* Hero */}
      <section className="relative h-[70vh] min-h-[480px] flex items-end bg-[--color-ink]">
        {heroUrl && (
          <Image
            src={heroUrl}
            alt="Văn Miếu – Quốc Tử Giám"
            fill
            className="object-cover opacity-60"
            priority
          />
        )}
        <div className="relative container pb-16">
          <h1 className="font-serif text-4xl md:text-5xl font-bold text-white max-w-2xl leading-tight mb-4">
            {t.title}
          </h1>
          <p className="text-sm text-white/80 max-w-xl mb-8">{t.sub}</p>
          <div className="flex gap-4">
            <Link
              href={`/${locale}/tham-quan`}
              className="px-6 py-3 bg-[--color-red-son] text-white text-sm hover:opacity-90 transition-opacity"
            >
              {t.cta}
            </Link>
            <Link
              href={`/${locale}/ve-di-tich`}
              className="px-6 py-3 border border-white text-white text-sm hover:bg-white hover:text-[--color-ink] transition-colors"
            >
              {t.cta2}
            </Link>
          </div>
        </div>
      </section>

      {/* Featured architecture */}
      <FadeInOnView as="section" className="container mt-[--spacing-section]">
        <div className="flex items-baseline justify-between mb-8">
          <h2 className="font-serif text-2xl font-semibold">
            {locale === 'vi' ? 'Công trình kiến trúc' : locale === 'en' ? 'Architecture' : 'Architecture'}
          </h2>
          <Link href={`/${locale}/ve-di-tich`} className="text-sm text-[--color-gold] hover:underline">
            {locale === 'vi' ? 'Xem tất cả →' : locale === 'en' ? 'View all →' : 'Voir tout →'}
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {featured.docs.map((item: any, i: number) => (
            <div key={item.id} className="animate-fade-up" style={{ '--i': i } as React.CSSProperties}>
              <DiTichCard
                id_code={item.id_code}
                title={item.title}
                subtitle={item.subtitle}
                section={item.section}
                slug={item.slug}
                locale={locale as Locale}
                imageUrl={item.images?.[0]?.image?.url}
              />
            </div>
          ))}
        </div>
      </FadeInOnView>

      {/* Quick info strip */}
      <FadeInOnView as="section" className="mt-[--spacing-section] bg-[--color-bg-subtle] border-y border-[--color-border]">
        <div className="container py-10 grid grid-cols-1 sm:grid-cols-3 gap-8">
          {[
            { label: locale === 'vi' ? 'Giờ mở cửa' : locale === 'en' ? 'Opening hours' : 'Horaires', value: '8:00 – 17:00' },
            { label: locale === 'vi' ? 'Địa chỉ' : locale === 'en' ? 'Address' : 'Adresse', value: '58 Quốc Tử Giám, Hà Nội' },
            { label: locale === 'vi' ? 'Vé vào cửa' : locale === 'en' ? 'Admission' : 'Entrée', value: '30.000 VND' },
          ].map((info) => (
            <div key={info.label}>
              <dt className="text-xs text-[--color-ink-muted] uppercase tracking-wider mb-1">{info.label}</dt>
              <dd className="font-serif text-lg">{info.value}</dd>
            </div>
          ))}
        </div>
      </FadeInOnView>

      {/* 82 Bia CTA */}
      <FadeInOnView as="section" className="container mt-[--spacing-section] mb-[--spacing-section]">
        <div className="border border-[--color-border] p-8 md:p-12 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <h2 className="font-serif text-2xl font-semibold mb-2">
              {locale === 'vi' ? '82 Bia Tiến Sĩ' : locale === 'en' ? '82 Doctoral Stelae' : '82 Stèles doctorales'}
            </h2>
            <p className="text-sm text-[--color-ink-muted] max-w-lg">
              {locale === 'vi'
                ? 'Ghi danh 1307 tiến sĩ từ năm 1442–1779. Di sản tư liệu thế giới UNESCO từ năm 2010.'
                : locale === 'en'
                ? '1,307 doctoral graduates from 1442–1779. UNESCO Memory of the World since 2010.'
                : '1 307 docteurs de 1442 à 1779. Mémoire du monde de l\'UNESCO depuis 2010.'}
            </p>
          </div>
          <Link
            href={`/${locale}/bia-tien-si`}
            className="shrink-0 px-6 py-3 bg-[--color-gold] text-white text-sm hover:opacity-90 transition-opacity"
          >
            {locale === 'vi' ? 'Khám phá bia tiến sĩ →' : locale === 'en' ? 'Explore stelae →' : 'Explorer les stèles →'}
          </Link>
        </div>
      </FadeInOnView>
    </div>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
