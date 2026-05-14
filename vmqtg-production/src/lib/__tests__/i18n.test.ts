import { describe, it, expect } from 'vitest'
import {
  isValidLocale,
  getLocaleFromPathname,
  localePath,
} from '../i18n'

describe('i18n utilities', () => {
  it('isValidLocale nhận vi/en/fr', () => {
    expect(isValidLocale('vi')).toBe(true)
    expect(isValidLocale('en')).toBe(true)
    expect(isValidLocale('fr')).toBe(true)
    expect(isValidLocale('de')).toBe(false)
  })

  it('getLocaleFromPathname trả đúng locale', () => {
    expect(getLocaleFromPathname('/vi/tham-quan')).toBe('vi')
    expect(getLocaleFromPathname('/en/about')).toBe('en')
    expect(getLocaleFromPathname('/tham-quan')).toBeNull()
  })

  it('localePath tạo đúng URL', () => {
    expect(localePath('vi', '/tham-quan')).toBe('/vi/tham-quan')
    expect(localePath('en', 'tham-quan')).toBe('/en/tham-quan')
  })
})
