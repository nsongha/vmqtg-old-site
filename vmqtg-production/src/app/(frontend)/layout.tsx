import type { Metadata } from 'next'
import { Lora, Inter, JetBrains_Mono } from 'next/font/google'
import React from 'react'
import '../globals.css'

const lora = Lora({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-lora',
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-inter',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Văn Miếu – Quốc Tử Giám',
  description: 'Di tích lịch sử quốc gia đặc biệt',
}

export default function FrontendRootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className={`${lora.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
        {children}
      </body>
    </html>
  )
}
