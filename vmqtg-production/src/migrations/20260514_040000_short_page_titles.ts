import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

// v0.3 sitemap shortens nav labels — and the user asked for page headings to
// match. Forwards an explicit UPDATE for the two affected pages because the
// seed step's skip-if-set guard won't overwrite an existing title.

export async function up({ db }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
    UPDATE "pages_locales"
    SET "title" = 'Di tích'
    WHERE "_locale" = 'vi'
      AND "_parent_id" IN (SELECT id FROM "pages" WHERE slug = 've-di-tich')
  `)
  await db.execute(sql`
    UPDATE "pages_locales"
    SET "title" = 'Trưng bày'
    WHERE "_locale" = 'vi'
      AND "_parent_id" IN (SELECT id FROM "pages" WHERE slug = 'trung-bay-trien-lam')
  `)
}

export async function down(_: MigrateDownArgs): Promise<void> {
  // No-op: forward-only.
}
