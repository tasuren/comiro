# Comicker Frontend - Compile, Require: jinja2, Details: Jinja2を使ってj2ファイルをコンパイルします。

from jinja2 import Environment, FileSystemLoader, select_autoescape
from os import listdir


env = Environment(
    loader=FileSystemLoader("./"),
    autoescape=select_autoescape(("html", "j2"))
)
for file_name in listdir("./"):
    if file_name.endswith(".j2"):
        with open(f"{file_name[:-3]}.html", "w") as f:
            f.write(env.get_template(file_name).render())
        print(f"Compiled {file_name}")