import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db, payload, req }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
   ALTER TABLE "pages_locales" ADD COLUMN "content_html" varchar;
  ALTER TABLE "di_tich_items_locales" ADD COLUMN "content_html" varchar;`)
}

export async function down({ db, payload, req }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`
   ALTER TABLE "pages_locales" DROP COLUMN "content_html";
  ALTER TABLE "di_tich_items_locales" DROP COLUMN "content_html";`)
}
