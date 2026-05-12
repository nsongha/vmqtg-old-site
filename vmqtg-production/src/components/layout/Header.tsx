import Link from 'next/link'
import { getPayloadClient } from '@/lib/payload'
import { MegaMenu } from './MegaMenu'
import { LanguageSwitcher } from './LanguageSwitcher'
import type { Locale } from '@/lib/i18n'

type Props = { locale: Locale }

export async function Header({ locale }: Props) {
  const payload = await getPayloadClient()

  const navData = await payload.find({
    collection: 'navigation',
    where: { key: { equals: 'main-nav' } },
    locale,
    limit: 1,
  })

  const navItems = navData.docs[0]?.items ?? []

  return (
    <header className="sticky top-0 z-40 bg-[--color-bg-primary] border-b border-[--color-border]">
      <div className="container flex items-center justify-between h-16 gap-8">
        {/* Logo */}
        <Link href={`/${locale}`} className="flex flex-col leading-tight">
          <span className="font-serif text-base font-semibold text-[--color-ink]">
            Văn Miếu – Quốc Tử Giám
          </span>
          <span className="text-xs text-[--color-ink-muted]">
            {locale === 'vi' ? 'Di tích lịch sử quốc gia đặc biệt'
             : locale === 'en' ? 'Special National Heritage Site'
             : 'Site du patrimoine national spécial'}
          </span>
        </Link>

        <MegaMenu items={navItems as any} locale={locale} />

        <div className="flex items-center gap-4">
          <LanguageSwitcher currentLocale={locale} />
          <Link
            href={`/${locale}/tham-quan`}
            className="hidden sm:block px-4 py-2 text-sm bg-[--color-red-son] text-white hover:opacity-90 transition-opacity"
          >
            {locale === 'vi' ? 'Mua vé' : locale === 'en' ? 'Tickets' : 'Billets'}
          </Link>
        </div>
      </div>
    </header>
  )
}
