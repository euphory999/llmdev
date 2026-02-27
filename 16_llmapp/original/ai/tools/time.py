from langchain.tools import tool
from datetime import datetime, timezone


# LLM に対して自作した外部ツールを定義することができます
# これは現在時刻を教えてくれるツールとなります
# このソースコードを雛形とすればおそらくツール追加を楽に行うことができると思います……


class CurrentTimeTool:

    # ============================
    # 機能を実装する
    # ============================
    # Langchain ではアノテーション (****:int) 部分で LLM に型を渡すので必須
    # ※ そうでなくても型の明示的な宣言は良い習慣ですね
    @tool
    @staticmethod
    def get_current_time(is_utc : bool = False) -> str:
        """現在時刻を返します
        Args:
            is_utc: もしも協定世界時(UTC)もしくはグリニッジ標準時(GMT)を指定された場合は true としてください、そうでなければ false を代入してください
        """
        # LLM へどんな機能かを説明してあげます
        # 上のドキュメントも必要です (ただし LLM にわたるので関数のドキュメント化とは少し違います)

        now = datetime.now(timezone.utc) if is_utc else datetime.now()
        now_str = now.strftime("%Y-%d-%m %H:%M%:%S")
        response = f"現在時刻は {now_str} です。 引数として utc={is_utc} を指定しました。"
        # 実際に LLM へわたる回答文です、わかりやすい文が良いと思います

        return response


    @classmethod
    def get_tool(cls):
        return cls.get_current_time
