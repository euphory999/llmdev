from pathlib import Path


import tiktoken
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool


class ChromaRag:
    def __init__(self,
                 pdf_data_path: Path,
                 chroma_db_path: Path,
                 model_name: str,
                 embedding_model_name: str):
        self.pdf_data_path = pdf_data_path
        self.chroma_db_path = chroma_db_path
        self.model = model_name
        self.embedding_model = embedding_model_name
        self.db = self.__struct_db()


    # インデックスの構築
    def __create_brand_new_db(self):
        # pathlib.Path に対応していないので絶対パスの文字列に直す
        pdf_data_str_path = str(self.pdf_data_path.resolve())

        # PDF ファイルを読込
        loader = DirectoryLoader(pdf_data_str_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()

        # チャンクに分割
        encoding_name = tiktoken.encoding_for_model(self.model).name
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(encoding_name)
        texts = text_splitter.split_documents(documents)

        # 新規にIndexを構築
        embedding_model = OpenAIEmbeddings(model=self.embedding_model)
        chroma_db_str_abspath = str(self.chroma_db_path.resolve())
        db = Chroma.from_documents(texts, embedding_model, persist_directory=chroma_db_str_abspath)
        return db
    

    def __struct_db(self):
        if self.chroma_db_path.is_dir():
            # もしも既に DB が存在するならばストレージから復元
            try:
                embedding_model = OpenAIEmbeddings(model=self.embedding_model)
                chroma_db_str_abspath = str(self.chroma_db_path.resolve())
                db = Chroma(persist_directory=chroma_db_str_abspath,
                            embedding_function=embedding_model)
            except Exception as e:
                db = self.__create_brand_new_db()
        else:
            # 存在しないならば再作成
            db = self.__create_brand_new_db()
        return db


    def get_tool(self):
        # Retrieverの作成
        retriever = self.db.as_retriever()

        # tool の作成
        retriever_tool = create_retriever_tool(
            retriever,
            "retrieve_company_rules",
            "Search and return company rules",
        )
        return retriever_tool