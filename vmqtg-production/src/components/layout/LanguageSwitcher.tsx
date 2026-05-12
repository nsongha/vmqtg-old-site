'use client'
import { usePathname, useRouter } from 'next/navigation'
import { LOCALES, type Locale } from '@/lib/i18n'

export function LanguageSwitcher({ currentLocale }: { currentLocale: Locale }) {
  const pathname = usePathname()
  const router = useRouter()

  function switchLocale(locale: Locale) {
    // Thay thế locale segment đầu tiên trong pathname
    const segments = pathname.split('/')
    segments[1] = locale
    router.push(segments.join('/'))
  }

  return (
    <div className="flex gap-1">
      {LOCALES.map((locale) => (
        <button
          key={locale}
          onClick={() => switchLocale(locale)}
          className={`px-2 py-1 text-xs font-mono uppercase tracking-wider transition-colors
            ${locale === currentLocale
              ? 'bg-[--color-ink] text-[--color-bg-primary]'
              : 'text-[--color-ink-muted] hover:text-[--color-ink]'
            }`}
        >
          {locale}
        </button>
      ))}
    </div>
  )
}
