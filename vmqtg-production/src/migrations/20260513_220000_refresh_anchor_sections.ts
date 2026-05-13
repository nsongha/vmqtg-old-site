import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

// One-shot: clear content_html (all locales) for pages whose extractor output
// changed. The new extractor labels each <section id="..."> with the v0.2
// sitemap id codes (D1..D7, C1..C3, E1..E6) instead of folder names so the
// mega-menu anchors (#D2, #C1.1, #E4...) actually scroll to the right place.
//
// seed-on-build's fillLocalized step (runs right after migrate) will refill
// these fields from oldsite-content.json. Per-field "skip if set" guard means
// only the affected pages get refreshed.

const SLUGS = ['hoat-dong', 'trung-bay-trien-lam', 'dich-vu']

export async function up({ db }: MigrateUpArgs): Promise<void> {
  for (const slug of SLUGS) {
    await db.execute(sql`
      UPDATE "pages_locales"
      SET "content_html" = NULL
      WHERE "_parent_id" IN (SELECT id FROM "pages" WHERE slug = ${slug})
    `)
  }
}

export async function down(_: MigrateDownArgs): Promise<void> {
  // No-op: forward-only refresh.
}
