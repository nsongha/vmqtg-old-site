import * as migration_20260512_084828 from './20260512_084828';
import * as migration_20260513_092854_add_content_html from './20260513_092854_add_content_html';
import * as migration_20260513_140000_polish_tham_quan_translations from './20260513_140000_polish_tham_quan_translations';

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
];
