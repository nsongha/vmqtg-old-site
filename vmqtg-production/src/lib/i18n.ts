export const LOCALES = ['vi', 'en', 'fr'] as const
export type Locale = typeof LOCALES[number]
export const DEFAULT_LOCALE: Locale = 'vi'

export function isValidLocale(locale: string): locale is Locale {
  return LOCALES.includes(locale as Locale)
}

export function getLocaleFromPathname(pathname: string): Locale | null {
  const segment = pathname.split('/')[1]
  return isValidLocale(segment) ? segment : null
}

export function localePath(locale: Locale, path: string): string {
  return `/${locale}${path.startsWith('/') ? path : '/' + path}`
}

export const LOCALE_NAMES: Record<Locale, string> = {
  vi: 'Tiếng Việt',
  en: 'English',
  fr: 'Français',
}
