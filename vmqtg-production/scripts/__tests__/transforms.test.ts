import { describe, it, expect } from 'vitest'
import { transformBiaTienSi, transformHistoricalNotes } from '../transforms'

describe('Seed transforms', () => {
  it('transformHistoricalNotes chuyển string[] thành array objects', () => {
    const input = ['Note A', 'Note B']
    const result = transformHistoricalNotes(input)
    expect(result).toEqual([{ note: 'Note A' }, { note: 'Note B' }])
  })

  it('transformBiaTienSi map đúng fields', () => {
    const input = {
      id: 1,
      year: '1442',
      dynasty: 'Lê sơ',
      candidates_count: '450',
      passed_count: '33',
      erection_year: '1484',
      title: 'Văn bia đề danh Tiến sĩ khoa Nhâm Tuất',
      contributors: { author: 'Thân Nhân Trung', calligrapher: 'Nguyễn Tủng', editor: 'Không ghi', engraver: 'Tô Ngại' },
      historical_notes: ['Note 1'],
      biographies: [{ name: 'Nguyễn Trực', dates: '1417-1474', description: '...', hometown: 'Bối Khê', roles: ['Hàn lâm viện'] }],
    }
    const result = transformBiaTienSi(input)
    expect(result.order).toBe(1)
    expect(result.year).toBe('1442')
    expect(result.candidates_count).toBe(450)
    expect(result.historical_notes).toEqual([{ note: 'Note 1' }])
    expect(result.biographies[0].roles).toEqual([{ role: 'Hàn lâm viện' }])
  })
})
