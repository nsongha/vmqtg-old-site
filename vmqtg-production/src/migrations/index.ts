import * as migration_20260512_084828 from './20260512_084828';
import * as migration_20260513_092854_add_content_html from './20260513_092854_add_content_html';

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
];
