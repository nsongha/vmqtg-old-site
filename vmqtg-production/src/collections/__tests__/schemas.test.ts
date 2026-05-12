import { describe, it, expect } from 'vitest'
import { Pages } from '../Pages'
import { BiaTienSi } from '../BiaTienSi'
import { DiTichItems } from '../DiTichItems'

// Tests use `as any` casts because Payload's Field type is a discriminated
// union — narrowing by `.name` isn't possible, and not every variant exposes
// the props we're asserting on (unique, options, localized, nested fields).
describe('Collection schemas', () => {
  it('Pages có slug field', () => {
    const slugField = (Pages.fields as any[]).find((f: any) => f.name === 'slug')
    expect(slugField).toBeDefined()
    expect(slugField.unique).toBe(true)
  })

  it('BiaTienSi có biographies array với roles', () => {
    const bioField = (BiaTienSi.fields as any[]).find((f: any) => f.name === 'biographies')
    expect(bioField?.type).toBe('array')
    const rolesField = bioField?.fields?.find((f: any) => f.name === 'roles')
    expect(rolesField?.type).toBe('array')
  })

  it('DiTichItems có đủ 6 section options', () => {
    const sectionField = (DiTichItems.fields as any[]).find((f: any) => f.name === 'section')
    expect(sectionField?.options).toHaveLength(6)
  })

  it('BiaTienSi historical_notes là localized', () => {
    const notesField = (BiaTienSi.fields as any[]).find((f: any) => f.name === 'historical_notes')
    expect(notesField?.localized).toBe(true)
  })
})
