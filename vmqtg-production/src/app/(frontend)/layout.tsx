import React from 'react'
import '../globals.css'

export default function FrontendRootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  )
}
