import { NextRequest, NextResponse } from 'next/server'
import { LOCALES, DEFAULT_LOCALE, getLocaleFromPathname } from './lib/i18n'

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Bỏ qua admin, API, và static files
  if (
    pathname.startsWith('/admin') ||
    pathname.startsWith('/api') ||
    pathname.startsWith('/_next') ||
    pathname.startsWith('/media') ||
    pathname.includes('.')
  ) {
    return NextResponse.next()
  }

  const locale = getLocaleFromPathname(pathname)
  if (!locale) {
    const url = request.nextUrl.clone()
    url.pathname = `/${DEFAULT_LOCALE}${pathname}`
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next|api|media|.*\\..*).*)'],
}
