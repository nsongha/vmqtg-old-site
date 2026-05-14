import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

// One-shot: clear dich-vu content_html (all locales) so seed-on-build refills
// it from the updated oldsite-content.json — which no longer includes the
// dich-vu/nuoc-uong section (E6 was dropped from the v0.3 sitemap).

export async function up({ db }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
    UPDATE "pages_locales"
    SET "content_html" = NULL
    WHERE "_parent_id" IN (SELECT id FROM "pages" WHERE slug = 'dich-vu')
  `)
}

export async function down(_: MigrateDownArgs): Promise<void> {
  // No-op: forward-only refresh.
}
