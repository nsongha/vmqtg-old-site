type Props = { html: string | null | undefined }

export function HtmlContent({ html }: Props) {
  if (!html) return null
  return (
    <div
      className="prose-html"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
