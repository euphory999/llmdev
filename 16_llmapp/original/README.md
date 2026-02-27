# アプリの構造

```
┣ app.py          ... サーバアプリケーションを起動するためのスクリプト
┗ ai/             ... AI を稼働させるためのライブラリ群
    ┣ graph.py        ... LangChain を利用して作成される Graph (生成AIに質問できます)
    ┣ keytool.py  
    ┣ nodes/          ... Graph で利用するノード
    ┗ tools/          ... Graph で利用する外部ツール (LLMと連携して呼び出せる外部機能)
┗ data/           ... RAG 検索の対象となるデータ
    ┣ pdf/
    ┗ text/
┗ routes/         ... サーバアプリケーションの各エンドポイントのルート
    ┣ clear.py
    ┗ root.py
┗ static/         ... サーバアプリケーションで利用する静的ファイル置き場 (css, js, 画像ファイルなど...)
┗ templates/      ... サーバアプリケーションで利用するテンプレートファイル
```

# 起動方法について

Python 3.12 にて動作確認を行っております

```bash
$ python3 app.py
```

※ もしもライブラリをインストールしていない場合は以下でインストールしてください

```bash
$ pip install -r ../../requirements.txt
```

