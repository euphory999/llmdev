#! /usr/bin/env python3

from routes.root import IndexPage
from routes.clear import Clear
from routes.stream import Stream

from flask import Flask
from pathlib import Path
from ai.keytool import KeyTool

from ai.graph import LangChainGraph

from ai.tools.rag import ChromaRag
from ai.tools.calc import CalculatorTool
from ai.tools.time import CurrentTimeTool

from pathlib import Path

# ======== 注意点 ========
# インスタンス変数には個人情報をいれてはいけません
# 他人同士で個人情報が共有されてしまいます
# 代わりにユーザごとに固有に用意される session を使ってください
#
# *** NGな例 ***
# self.username = "alice"
#
# ↓↓↓
# 
# *** OKな例 ***
# session["username"] = "alice"

###
### Flask アプリケーションを定義したクラス
###
class FlaskWebApplication:

    # アプリを作るコンストラクタ
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'your_secret_key'
        self.routing_table = {}

        self.app_dir = Path(__file__).parent
        self.app.config.app_dir = self.app_dir
        self.app.config.graph = self.__create_graph()


    def __create_graph(self):
        pdf_data_path = self.app_dir / "data/pdf"
        chroma_db_path = self.app_dir / "chroma_db"

        model_name = "gpt-4o-mini"
        embedding_model_name = "text-embedding-3-small"

        # LLM と連携したいツールを以下に列挙していきます
        # ***.get_tool() で関数を返してくれるように統合しています
        graph_tools = [
            ChromaRag(pdf_data_path, chroma_db_path, model_name, embedding_model_name).get_tool(),
            CalculatorTool.get_tool(),
            CurrentTimeTool.get_tool()
        ]

        graph = LangChainGraph(tools=graph_tools)
        return graph


    # ルーティングを追加する
    def add_route(self, cls, path):
        self.app.add_url_rule(
            path, 
            view_func=cls.as_view(cls.API_NAME, self.app))

    
    # アプリを起動するクラス
    def launch(self):
        self.app.run(debug=True, host='127.0.0.1')


def main():
    # 以下を有効化することで ../.env から API Key を入手して
    # 環境変数 (os.environ) へストアします
    KeyTool.enable_api_key()

    # 新しく Flask app のインスタンスをつくります
    app = FlaskWebApplication()

    # 以下のメソッドでルーティングを追加できます
    app.add_route(IndexPage, "/")
    app.add_route(Clear,     "/clear")
    app.add_route(Stream,    "/stream")

    # アプリケーションを起動します
    app.launch()


if __name__ == "__main__":
    main()
