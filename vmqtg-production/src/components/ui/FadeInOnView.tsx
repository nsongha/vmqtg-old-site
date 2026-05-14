'use client'
import { useEffect, useRef, useState, type ReactNode, type CSSProperties } from 'react'

type Props = {
  children: ReactNode
  /** Extra delay in ms (e.g. for cascading sections). */
  delay?: number
  /** Visibility threshold 0–1; default 0.05 (5% visible triggers). */
  threshold?: number
  className?: string
  /** Render as a different tag if needed (default: div). */
  as?: 'div' | 'section' | 'article'
  /** DOM id (useful for anchor jumps from nav). */
  id?: string
}

export function FadeInOnView({
  children,
  delay = 0,
  threshold = 0.05,
  className = '',
  as: Tag = 'div',
  id,
}: Props) {
  const ref = useRef<HTMLElement>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    // If we can't observe (older browsers, SSR fallback), show immediately.
    if (typeof IntersectionObserver === 'undefined') {
      setVisible(true)
      return
    }

    const obs = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            setVisible(true)
            obs.disconnect()
            break
          }
        }
      },
      { threshold, rootMargin: '0px 0px -40px 0px' },
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [threshold])

  const style = delay > 0 ? ({ '--delay': `${delay}ms` } as CSSProperties) : undefined

  return (
    <Tag
      ref={ref as any}
      id={id}
      style={style}
      className={`fade-in-on-view ${visible ? 'is-visible' : ''} ${className}`.trim()}
    >
      {children}
    </Tag>
  )
}
