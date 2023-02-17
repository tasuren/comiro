/* comiro Components - Header */

import { component$ } from "@builder.io/qwik";
import { Link } from "@builder.io/qwik-city";


export const menu = {
  display: "flex", fontSize: "16px",
  justifyContent: "space-around"
};


type itemProps = {href: string, label: string};

export const Item = (({href, label}: itemProps) => <li>
  <Link href={href}>{label}</Link>
</li>);


export default component$(() => {
  return (
    <header>
      <h1 style={{textAlign: "center"}}>comiro</h1>
      <nav>
        <ul style={menu}>
          <Item href="/" label="ホーム" />
          <Item href="/viewer" label="ビュワー" />
        </ul>
      </nav>
    </header>
  );
});