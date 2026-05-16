import * as migration_20260512_084828 from './20260512_084828';
import * as migration_20260513_092854_add_content_html from './20260513_092854_add_content_html';
import * as migration_20260513_140000_polish_tham_quan_translations from './20260513_140000_polish_tham_quan_translations';
import * as migration_20260513_200000_refresh_hoat_dong_vi from './20260513_200000_refresh_hoat_dong_vi';
import * as migration_20260513_220000_refresh_anchor_sections from './20260513_220000_refresh_anchor_sections';
import * as migration_20260513_230000_refresh_dich_vu_drop_e6 from './20260513_230000_refresh_dich_vu_drop_e6';
import * as migration_20260514_040000_short_page_titles from './20260514_040000_short_page_titles';
import * as migration_20260516_041600_add_media_category from './20260516_041600_add_media_category';

export const migrations = [
  {
    up: migration_20260512_084828.up,
    down: migration_20260512_084828.down,
    name: '20260512_084828',
  },
  {
    up: migration_20260513_092854_add_content_html.up,
    down: migration_20260513_092854_add_content_html.down,
    name: '20260513_092854_add_content_html'
  },
  {
    up: migration_20260513_140000_polish_tham_quan_translations.up,
    down: migration_20260513_140000_polish_tham_quan_translations.down,
    name: '20260513_140000_polish_tham_quan_translations'
  },
  {
    up: migration_20260513_200000_refresh_hoat_dong_vi.up,
    down: migration_20260513_200000_refresh_hoat_dong_vi.down,
    name: '20260513_200000_refresh_hoat_dong_vi'
  },
  {
    up: migration_20260513_220000_refresh_anchor_sections.up,
    down: migration_20260513_220000_refresh_anchor_sections.down,
    name: '20260513_220000_refresh_anchor_sections'
  },
  {
    up: migration_20260513_230000_refresh_dich_vu_drop_e6.up,
    down: migration_20260513_230000_refresh_dich_vu_drop_e6.down,
    name: '20260513_230000_refresh_dich_vu_drop_e6'
  },
  {
    up: migration_20260514_040000_short_page_titles.up,
    down: migration_20260514_040000_short_page_titles.down,
    name: '20260514_040000_short_page_titles'
  },
  {
    up: migration_20260516_041600_add_media_category.up,
    down: migration_20260516_041600_add_media_category.down,
    name: '20260516_041600_add_media_category'
  },
];
