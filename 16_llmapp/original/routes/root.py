from flask import render_template, make_response, session, request
import uuid
from flask.views import MethodView


class IndexPage(MethodView):

    API_NAME = "index"

    def __init__(self, app):
        super().__init__()
        self.app = app


    def get(self):
        graph = self.app.config.graph
        if 'thread_id' not in session:
            session['thread_id'] = str(uuid.uuid4())

        # メモリをクリア
        graph.clear_memory()
        # 対話履歴を初期化
        response = make_response(render_template('index.html', messages=[]))
        return response


    def post(self):
        graph = self.app.config.graph
        if 'thread_id' not in session:
            session['thread_id'] = str(uuid.uuid4())
        thread_id = session['thread_id']

        user_message = request.form['user_message']
        # ボットのレスポンスを取得（メモリに保持）
        graph.invoke(user_message, thread_id)

        # メモリからメッセージの取得
        messages = graph.get_messages_list(thread_id)

        # レスポンスを返す
        return make_response(render_template('index.html', messages=messages))
