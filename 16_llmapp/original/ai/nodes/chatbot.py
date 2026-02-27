from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

# Stateクラス: メッセージのリストを保持する辞書型
# Note. 余りお行儀がよろしくないですが今回はインナークラスとします
class ChatBotState(TypedDict):
    messages: Annotated[list, add_messages]


class ChatBot:

    def __init__(self, model_name, tools):
        self.name = "chatbot"
        self.model_name = model_name

        llm = ChatOpenAI(model_name=self.model_name)
        self.llm = llm.bind_tools(tools)


    def chatbot(self, state: ChatBotState):
        return {
            "messages": [
                self.llm.invoke(state["messages"])
            ]
        }


    def get_node(self):
        return self.chatbot


    def get_name(self):
        return self.name
        