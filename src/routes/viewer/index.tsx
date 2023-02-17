/* comiro - Viewer */

import { component$ } from '@builder.io/qwik';
import type { DocumentHead } from '@builder.io/qwik-city';

export default component$(() => {
  return ( <>
    Test
  </> );
});

export const head: DocumentHead = {title: "Viewer"};