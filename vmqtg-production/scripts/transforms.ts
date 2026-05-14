// scripts/transforms.ts
export function transformHistoricalNotes(notes: string[]): { note: string }[] {
  return notes.map((note) => ({ note }))
}

export function transformBiaTienSi(raw: any) {
  return {
    order: raw.id,
    year: raw.year,
    dynasty: raw.dynasty,
    erection_year: raw.erection_year,
    candidates_count: parseInt(raw.candidates_count) || undefined,
    passed_count: parseInt(raw.passed_count) || undefined,
    title: raw.title,
    contributors: {
      author: raw.contributors?.author ?? '',
      calligrapher: raw.contributors?.calligrapher ?? '',
      editor: raw.contributors?.editor ?? '',
      engraver: raw.contributors?.engraver ?? '',
    },
    historical_notes: transformHistoricalNotes(raw.historical_notes ?? []),
    biographies: (raw.biographies ?? []).map((bio: any) => ({
      name: bio.name,
      dates: bio.dates ?? '',
      description: bio.description ?? '',
      hometown: bio.hometown ?? '',
      roles: (bio.roles ?? []).map((r: string) => ({ role: r })),
    })),
  }
}
