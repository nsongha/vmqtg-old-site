import { MigrateUpArgs, MigrateDownArgs, sql } from '@payloadcms/db-postgres'

export async function up({ db }: MigrateUpArgs): Promise<void> {
  await db.execute(sql`
    DO $$ BEGIN
      CREATE TYPE "public"."enum_media_category" AS ENUM(
        'kien-truc', 'lich-su', 'danh-nhan', 'tuong-tho', 'hoat-dong', 'khac'
      );
    EXCEPTION WHEN duplicate_object THEN null;
    END $$;
  `)
  await db.execute(sql`
    ALTER TABLE "media" ADD COLUMN IF NOT EXISTS "category" "public"."enum_media_category";
  `)
}

export async function down({ db }: MigrateDownArgs): Promise<void> {
  await db.execute(sql`ALTER TABLE "media" DROP COLUMN IF EXISTS "category";`)
  await db.execute(sql`DROP TYPE IF EXISTS "public"."enum_media_category";`)
}
