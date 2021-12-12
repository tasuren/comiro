# Comicker Frontend - Compile
# Requires: jinja2, flask-misaka
# Details: Jinja2を使ってj2ファイルをコンパイルします。

from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask_misaka import Misaka
from os import listdir
from sys import argv


env = Environment(
    loader=FileSystemLoader("./"),
    autoescape=select_autoescape(("html", "j2"))
)
env.filters.setdefault("markdown", Misaka(autolink=True).render)
for file_name in listdir("./"):
    if file_name.endswith(".j2"):
        with open(f"{file_name[:-3]}.html", "w") as f:
            f.write(env.get_template(file_name).render())
        print(f"Compiled {file_name}")