# comicker
Comickerとは漫画等のウェブサイトの画像のみを閲覧することができるウェブサービスです。  
ウェブサイト：Comming soon...

## Installation
1. `auth.json.template`のコピーである`auth.json`を作りその中身を適切なものに交換する。
2. `auth.json`で書き換えたMySQLのユーザーなどが動作するようにMySQLをセットアップする。
3. `frontend/brython`にBrythonをインストールする。
4. `requirements.txt`にあるライブラリをPythonにインストールする。
5. `cd frontend`で`frontend`に移動した後に`compile.py`をPythonで実行し、ウェブページのJinja2のファイルをHTMLにコンパイルする。
6. `frontend`フォルダ内でComickerのウェブサイトを渡すサーバーを起動する。(例：`python3 -m http.server`)
7. 画像データをスクレイピングしたりするためのバックエンドの`main.py`を実行する。
8. バックエンドのURLを`frontend/src/constants.py`の`URL`に書き込む。この際に`localhost`で試す場合は上の変数に入れましょう。(例：`URL = "http://localhost:801`)
9. セットアップ終了