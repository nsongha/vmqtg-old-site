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

type Column = { header: NavChild | null; items: NavChild[]; key: string }

/**
 * Groups mega-menu children by the first segment of group_id. A bare group_id
 * (e.g. "B1") marks the column header; dotted ids (e.g. "B1.1") are list items
 * within that column.
 */
function groupChildren(children: NavChild[]): Column[] {
  const order: string[] = []
  const groups = new Map<string, Column>()

  for (const child of children) {
    const gid = child.group_id ?? '__'
    const key = gid.includes('.') ? gid.split('.')[0] : gid
    let col = groups.get(key)
    if (!col) {
      col = { header: null, items: [], key }
      groups.set(key, col)
      order.push(key)
    }
    if (gid === key) col.header = child
    else col.items.push(child)
  }
  return order.map((k) => groups.get(k)!)
}

function localizedHref(locale: Locale, href: string): string {
  if (!href.startsWith('/')) return href
  const [path, hash] = href.split('#', 2)
  const prefixed = `/${locale}${path}`
  return hash ? `${prefixed}#${hash}` : prefixed
}

export function MegaMenu({ items, locale }: Props) {
  const [openMenu, setOpenMenu] = useState<string | null>(null)

  return (
    <nav className="hidden lg:flex items-center gap-6">
      {items.map((item) => {
        const hasChildren = (item.children?.length ?? 0) > 0
        const isMega = hasChildren && item.mega_menu === true
        const isSimple = hasChildren && item.mega_menu !== true
        const columns = isMega ? groupChildren(item.children!) : []

        return (
          <div
            key={item.href}
            className="relative"
            onMouseEnter={() => (hasChildren ? setOpenMenu(item.href) : null)}
            onMouseLeave={() => setOpenMenu(null)}
          >
            <Link
              href={localizedHref(locale, item.href)}
              className="text-sm font-sans text-[--color-ink] hover:text-[--color-gold] transition-colors py-2"
            >
              {item.label}
            </Link>

            {/* Mega menu — column grid grouped by group_id */}
            {isMega && openMenu === item.href && (
              <div
                className="absolute top-full left-0 z-50 bg-[--color-bg-primary] border border-[--color-border] shadow-lg p-6"
                style={{
                  gridTemplateColumns: `repeat(${Math.min(columns.length, 7)}, minmax(180px, 1fr))`,
                  display: 'grid',
                  gap: '24px',
                  maxWidth: '90vw',
                }}
              >
                {columns.map((col) => (
                  <div key={col.key} className="min-w-0">
                    {col.header && (
                      <Link
                        href={localizedHref(locale, col.header.href)}
                        className="block font-serif text-sm font-semibold text-[--color-ink] hover:text-[--color-gold] mb-2 border-b border-[--color-border] pb-2"
                      >
                        {col.header.label}
                      </Link>
                    )}
                    {col.items.length > 0 && (
                      <ul className="space-y-1.5">
                        {col.items.map((child) => (
                          <li key={child.href}>
                            <Link
                              href={localizedHref(locale, child.href)}
                              className="block text-xs text-[--color-ink-muted] hover:text-[--color-gold] transition-colors"
                            >
                              <span className="font-mono mr-1.5 opacity-60">{child.group_id}</span>
                              {child.label}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Simple dropdown — single vertical list */}
            {isSimple && openMenu === item.href && (
              <div className="absolute top-full left-0 z-50 bg-[--color-bg-primary] border border-[--color-border] shadow-lg w-64">
                {item.children!.map((child) => (
                  <Link
                    key={child.href}
                    href={localizedHref(locale, child.href)}
                    className="block px-4 py-3 text-sm hover:bg-[--color-bg-subtle] hover:text-[--color-gold] transition-colors border-b border-[--color-border] last:border-b-0"
                  >
                    {child.group_id && (
                      <span className="font-mono text-xs text-[--color-ink-muted] mr-2">{child.group_id}</span>
                    )}
                    {child.label}
                  </Link>
                ))}
              </div>
            )}
          </div>
        )
      })}
    </nav>
  )
}
