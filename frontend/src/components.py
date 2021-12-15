# Comicker Frontend - Components

from browser import document, html


def make_button(href, href2):
    return html.A(
        "見る", href=href, Class="btn btn-primary"
    ) + " " + html.A(
        "元ページに行く", href=href2, Class="btn btn-secondary", id=href2
    )


def get_card(title, make, close, *args):
    "本棚を作ります。"
    return html.DIV(
        html.DIV(
            (
                title + html.BUTTON(
                    type="button", Class="btn-close btn-close-white",
                    id=args[1], **{"aria-label": "Close"}
                )
                if close else title
            ),
            Class="card-header"
        ) + html.DIV(
            make(*args),
            Class="card-body"
        ),
        Class="card text-white bg-dark"
    )


TITLE_BRACKETS = (("【", "】"), ("〔", "〕"))
def get_name(title):
    for before, after in TITLE_BRACKETS:
        if title.startswith(before) and after in title:
            title = title[title.find(after) + 1:]
    return title


def get_bookshelf(datas, close=True):
    row = html.DIV(Class="row")
    before = ""
    for title, data in sorted(
        map(lambda x: (get_name(x["title"] or x["url"]), x), datas),
        key=lambda x: x[0]
    ):
        if (now := title[0]) != before:
            before = now
            row <= html.H3(f"{before}行")
        row <= html.DIV(
            get_card(
                data["title"], make_button, close,
                f"/bookshelf.html?view={data['url']}",
                data["url"]
            ), Class="col-sm-6"
        )
    return row


def get_loading(**kwargs):
    return html.DIV(
        (html.DIV(Class=f"sk-cube sk-cube{i+1}") for i in range(9)),
        Class="sk-cube-grid", **kwargs
    )


def remove_loading(id_):
    document[id_].attrs["hidden"] = "true"


def show_loading(id_):
    if "hidden" in document[id_].attrs:
        del document[id_].attrs["hidden"]