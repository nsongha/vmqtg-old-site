type CardProps = {
  children: React.ReactNode
  className?: string
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-[--color-bg-subtle] border border-[--color-border] ${className}`}>
      {children}
    </div>
  )
}
