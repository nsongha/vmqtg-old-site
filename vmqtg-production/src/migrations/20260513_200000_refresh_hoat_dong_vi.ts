import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

// One-shot: clears the hoat-dong page's vi content_html. The subsequent
// seed-on-build step (which runs right after `payload migrate` in the build
// pipeline) will refill it from the updated oldsite-content.json — which now
// aggregates all 8 cac-hoat-dong/ sub-categories from vmqtg-v5 instead of the
// two site/hoat-dong/ articles that were captured previously.
//
// Why a migration: fillContentFromOldsite preserves any existing content_html
// per locale ("don't clobber admin edits"). To opt-in to a refresh for one
// specific row, we null it here so the seed step fills it fresh.

export async function up({ db }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
    UPDATE "pages_locales"
    SET "content_html" = NULL
    WHERE "_locale" = 'vi'
      AND "_parent_id" IN (SELECT id FROM "pages" WHERE slug = 'hoat-dong')
  `)
}

export async function down(_: MigrateDownArgs): Promise<void> {
  // No-op: forward-only refresh.
}
