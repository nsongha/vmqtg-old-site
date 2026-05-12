type BadgeProps = {
  children: React.ReactNode
  variant?: 'gold' | 'red' | 'muted'
}

export function Badge({ children, variant = 'muted' }: BadgeProps) {
  const styles = {
    gold: 'bg-[--color-gold] text-white',
    red: 'bg-[--color-red-son] text-white',
    muted: 'bg-[--color-bg-subtle] text-[--color-ink-muted]',
  }
  return (
    <span className={`inline-block px-2 py-0.5 text-xs font-mono rounded-sm ${styles[variant]}`}>
      {children}
    </span>
  )
}
