import { RichText as PayloadRichText } from '@payloadcms/richtext-lexical/react'
import type { SerializedEditorState } from '@payloadcms/richtext-lexical/lexical'

type Props = { content: SerializedEditorState | null | undefined }

export function RichText({ content }: Props) {
  if (!content) return null
  return <PayloadRichText data={content} />
}
