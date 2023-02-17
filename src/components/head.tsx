/* comiro Components - Head */

import { component$ } from '@builder.io/qwik';
import { useDocumentHead } from '@builder.io/qwik-city';


export const RouterHead = component$(() => {
  const head = useDocumentHead();

  return (
    <>
      <title>{`comiro - ${head.title}`}</title>

      <meta name="viewport" content="width=device-width, initial-scale=1.0" />

      <meta name="title" content="comiro" />
      <meta name="description" content="邪魔なものが多い漫画サイトの閲覧に便利なウェブツールです。" />
      {head.meta.map((m) => (
        <meta {...m} />
      ))}

      {head.links.map((l) => (
        <link {...l} />
      ))}

      {head.styles.map((s) => (
        <style {...s.props} dangerouslySetInnerHTML={s.style} />
      ))}
    </>
  );
});