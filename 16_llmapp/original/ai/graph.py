# builtin modules
import os

# my modules
from ai.nodes.chatbot import ChatBot, ChatBotState

# 3rd party modules
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# from langchain_community.tools.tavily_search import TavilySearchResults
class LangChainGraph:

    # グラフをここで作成します
    def __init__(self,
                 tools: list = [],
                 model_name: str = "gpt-4o-mini",
                 embedding_model_name: str = "text-embedding-3-small"):
        # Set instance variables
        self.model_name = model_name
        self.embedding_model = embedding_model_name
        self.tools = tools

        # MemorySaverインスタンスの作成
        self.memory = MemorySaver()

        # LangChain のテレメトリ無効化??
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        os.environ["LANGCHAIN_ANALYTICS"] = "false"
        
        # Chroma のテレメトリ無効化
        os.environ["ANONYMIZED_TELEMETRY"] = "False"

        # グラフの作成
        self.graph = self.__build_graph()
        

    def clear_memory(self):
        self.memory.storage.clear()


    # ===== グラフの構築 =====
    def __build_graph(self):
        """
        グラフのインスタンスを作成し、ツールノードやチャットボットノードを追加します。
        モデル名とメモリを使用して、実行可能なグラフを作成します。
        """

        # グラフのインスタンスを作成
        graph_builder = StateGraph(ChatBotState)

        # ツールノードの作成
        tool_node = ToolNode(self.tools)
        graph_builder.add_node("tools", tool_node)
        
        # ノードの追加
        chatbot = ChatBot(self.model_name, self.tools)
        graph_builder.add_node(chatbot.get_name(), chatbot.get_node())

        # 実行可能なグラフの作成
        graph_builder.add_conditional_edges(
            chatbot.get_name(),
            tools_condition,
        )
        graph_builder.add_edge("tools", chatbot.get_name())
        graph_builder.set_entry_point(chatbot.get_name())
        return graph_builder.compile(checkpointer=self.memory)


    # ===== グラフを実行する関数 =====
    def invoke(self, user_message: str, thread_id: str):
        """
        ユーザーからのメッセージを元に、グラフを実行し、チャットボットの応答をストリーミングします。
        """

        # 基本的にユーザのプロンプト
        messages = {
            "messages": [
                ("user", user_message)
            ]
        }

        # ユーザごとに保持するスレッド
        configurable = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        response = self.graph.invoke(
            messages, configurable,
            stream_mode="values"
        )
        return response["messages"][-1].content


    # ===== メッセージの一覧を取得する関数 =====
    def get_messages_list(self, thread_id: str):
        """
        メモリからメッセージ一覧を取得し、ユーザーとボットのメッセージを分類します。
        """
        messages = []
        # メモリからメッセージを取得
        memories = self.memory.get({"configurable": {"thread_id": thread_id}})['channel_values']['messages']
        for message in memories:
            if isinstance(message, HumanMessage):
                # ユーザーからのメッセージ
                messages.append({'class': 'user-message', 'text': message.content.replace('\n', '<br>')})
            elif isinstance(message, AIMessage) and message.content != "":
                # ボットからのメッセージ（最終回答）
                messages.append({'class': 'bot-message', 'text': message.content.replace('\n', '<br>')})
        return messages


# =====================================
# from pathlib import Path
# from tools.rag import ChromaRag
# from keytool import KeyTool
#
# pdf_data_path = Path(__file__).parent.parent / "data/pdf"
# chroma_db_path = Path(__file__).parent / "SAMPLE_DB"
# model_name = "gpt-4o-mini"
# embedding_model_name = "text-embedding-3-small"

# KeyTool.enable_api_key()

# graph_tools = [
#     ChromaRag(pdf_data_path, chroma_db_path, model_name, embedding_model_name).get_tool()
# ]

# graph = LangChainGraph(tools=graph_tools)

# thread_id = "user1"
# response = graph.invoke("こんにちは", thread_id)
# print(response)

# thread_id = "user2"
# response = graph.invoke("はじめまして", thread_id)
# print(response)

# print("===============")
# for message in graph.get_messages_list(thread_id):
#     print(message)
# ======================================