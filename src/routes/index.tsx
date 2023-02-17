/* comiro Routes - Index */

import { component$ } from '@builder.io/qwik';
import type { DocumentHead } from '@builder.io/qwik-city';

export default component$(() => {
  return ( <>
    comiroへようこそ。<br />
    これは、簡単にウェブページにある画像を取り出して、画像のみで表示するためのウェブツールです。<br />
    邪魔なものが多い漫画サイト等の閲覧にお使いください。
  </> );
});

export const head: DocumentHead = {title: '漫画サイト閲覧ツール'};