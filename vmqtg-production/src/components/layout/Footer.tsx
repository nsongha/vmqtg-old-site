import Link from 'next/link'
import type { Locale } from '@/lib/i18n'

type Props = { locale: Locale }

const FOOTER_TEXT = {
  vi: {
    address: '58 Quốc Tử Giám, Văn Miếu, Đống Đa, Hà Nội',
    phone: '024.3747.1322',
    email: 'vanmieuqtg@hanoi.gov.vn',
    copy: '© Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám',
  },
  en: {
    address: '58 Quoc Tu Giam St., Van Mieu Ward, Dong Da, Hanoi',
    phone: '024.3747.1322',
    email: 'vanmieuqtg@hanoi.gov.vn',
    copy: '© Centre for Cultural and Scientific Activities of the Temple of Literature',
  },
  fr: {
    address: '58 rue Quoc Tu Giam, Quartier Van Mieu, Dong Da, Hanoï',
    phone: '024.3747.1322',
    email: 'vanmieuqtg@hanoi.gov.vn',
    copy: '© Centre des activités culturelles et scientifiques du Temple de la Littérature',
  },
}

export function Footer({ locale }: Props) {
  const t = FOOTER_TEXT[locale]
  return (
    <footer className="mt-[--spacing-section] border-t border-[--color-border] bg-[--color-bg-subtle]">
      <div className="container py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 className="font-serif text-sm font-semibold mb-3">Văn Miếu – Quốc Tử Giám</h3>
          <address className="not-italic text-xs text-[--color-ink-muted] leading-relaxed">
            {t.address}<br />
            {t.phone}<br />
            <a href={`mailto:${t.email}`} className="hover:text-[--color-gold]">{t.email}</a>
          </address>
        </div>
        <div>
          <h3 className="font-serif text-sm font-semibold mb-3">
            {locale === 'vi' ? 'Khám phá' : locale === 'en' ? 'Explore' : 'Explorer'}
          </h3>
          <ul className="space-y-2 text-xs text-[--color-ink-muted]">
            {[
              { href: '/tham-quan', label: { vi: 'Thông tin tham quan', en: 'Visitor info', fr: 'Informations' } },
              { href: '/ve-di-tich', label: { vi: 'Về di tích', en: 'About', fr: 'À propos' } },
              { href: '/bia-tien-si', label: { vi: '82 Bia Tiến Sĩ', en: '82 Doctoral Stelae', fr: '82 Stèles' } },
            ].map((link) => (
              <li key={link.href}>
                <Link href={`/${locale}${link.href}`} className="hover:text-[--color-gold]">
                  {link.label[locale]}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="flex items-end">
          <p className="text-xs text-[--color-ink-muted]">{t.copy}</p>
        </div>
      </div>
    </footer>
  )
}
