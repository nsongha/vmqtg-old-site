'use client'
import { useState } from 'react'
import Link from 'next/link'
import type { Locale } from '@/lib/i18n'

type NavChild = { label: string; href: string; group_id?: string }
type NavItem = {
  label: string
  href: string
  mega_menu?: boolean
  children?: NavChild[]
}

type Props = { items: NavItem[]; locale: Locale }

export function MegaMenu({ items, locale }: Props) {
  const [openMenu, setOpenMenu] = useState<string | null>(null)

  return (
    <nav className="hidden lg:flex items-center gap-6">
      {items.map((item) => (
        <div
          key={item.href}
          className="relative"
          onMouseEnter={() => (item.children?.length ?? 0) > 0 ? setOpenMenu(item.href) : null}
          onMouseLeave={() => setOpenMenu(null)}
        >
          <Link
            href={`/${locale}${item.href}`}
            className="text-sm font-sans text-[--color-ink] hover:text-[--color-gold] transition-colors py-2"
          >
            {item.label}
          </Link>

          {/* Dropdown / mega menu */}
          {(item.children?.length ?? 0) > 0 && openMenu === item.href && (
            <div className={`absolute top-full left-0 z-50 bg-[--color-bg-primary] border border-[--color-border] shadow-lg
              ${item.mega_menu ? 'w-[640px] grid grid-cols-2 gap-0' : 'w-56'}`}
            >
              {item.children!.map((child) => (
                <Link
                  key={child.href}
                  href={`/${locale}${child.href}`}
                  className="block px-4 py-3 text-sm hover:bg-[--color-bg-subtle] hover:text-[--color-gold] transition-colors border-b border-[--color-border]"
                >
                  {child.group_id && (
                    <span className="font-mono text-xs text-[--color-ink-muted] block">{child.group_id}</span>
                  )}
                  {child.label}
                </Link>
              ))}
            </div>
          )}
        </div>
      ))}
    </nav>
  )
}
