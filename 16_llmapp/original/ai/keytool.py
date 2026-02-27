# builtin modules
import os
import re
from pathlib import Path

# 3rd party modules
from dotenv import load_dotenv


class KeyTool:
    @classmethod
    def enable_api_key(cls, api_key=None):
        if api_key is None: 
            os.environ['OPENAI_API_KEY'] = cls.load_api_key()
        else:
            os.environ['OPENAI_API_KEY'] = api_key


    @staticmethod
    def load_api_key():
        api_key = None

        # 1. ../.env を読み取る
        env_file_path = Path(__file__).parent.parent.parent.parent.resolve() / ".env"
        print(env_file_path)
        if env_file_path.is_file():
            try:
                load_dotenv(env_file_path)
            except:
                raise Exception("Found .env file but failed to load dotenv file! Please install python-dotenv module.")

        # 2. API_KEY の中身を読み取る
        api_key = os.environ.get("API_KEY", None)

        # 3. API_KEY の中身が FilePath ならばその FilePath の中身を API_KEY として読み出す
        api_file_path = Path(api_key).expanduser()
        if (api_file_path.is_absolute() and api_file_path.is_file()):
            with open(api_file_path, "r") as f:
                api_key = f.read().strip()

        # 4. OpenAI API キーの簡易チェック
        #    "sk-***" という形式のようです
        if re.match(r"^sk\-.*$", api_key) is None:
            raise Exception("Failed to load api key!")
            
        return api_key
