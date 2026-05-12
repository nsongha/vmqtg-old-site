import { notFound } from 'next/navigation'
import { isValidLocale, type Locale } from '@/lib/i18n'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'

type Props = {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params
  if (!isValidLocale(locale)) notFound()

  return (
    <>
      <Header locale={locale as Locale} />
      <main>{children}</main>
      <Footer locale={locale as Locale} />
    </>
  )
}

export function generateStaticParams() {
  return [{ locale: 'vi' }, { locale: 'en' }, { locale: 'fr' }]
}
