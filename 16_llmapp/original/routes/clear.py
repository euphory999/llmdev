from flask import render_template, make_response, session

from flask.views import MethodView

class Clear(MethodView):

    API_NAME = "clear"

    def __init__(self, app):
        super().__init__()
        self.app = app


    # 実際に処理を行うメソッド
    def post(self):
        session.pop('thread_id', None)

        graph = self.app.config.graph
        graph.clear_memory()

        response = make_response(render_template('index.html', messages=[]))
        return response
