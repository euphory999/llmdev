from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import traceback

app = Flask(__name__)

# 実行するディレクトリごとに保存されるパスが変わってしまうため
# 常に app.py と同じディレクトリに保存するように
# ちょっとだけ改修させてもらいます
TODO_FILE = Path(__file__).parent / "todos.txt"

# ファイルからTODOリストを読み込む関数
def load_todos():
    try:
        with open(TODO_FILE, "r") as file:
            todos = [line.strip() for line in file]
    except FileNotFoundError:
        todos = []
    return todos


# TODOリストをファイルに保存する関数
def save_todos(todos):
    with open(TODO_FILE, "w") as file:
        file.write("\n".join(todos))


# TODOリストからタスクを削除する関数
def delete_todo(todo_id):

    # 現時点でのタスクを読み取り
    todos = load_todos()

    # もし削除できるならタスクの削除を行う
    try:
        deleted_todo = todos.pop(todo_id)
    except Exception as e:
        print("=== EXCEPTION ============")
        print(traceback.format_exc())
        print("==========================")
        print(f"Failed to delete task. {todo_id=}")
        deleted_todo = None

    # 結果を保存
    save_todos(todos)

    # 今回は必要がないが削除したタスクを返す
    return deleted_todo


@app.route("/", methods=["GET", "POST"])
def index():
    todos = load_todos()
    if request.method == "POST":
        new_todo = request.form.get("todo")
        if new_todo:
            todos.append(new_todo)
            save_todos(todos)
        return redirect(url_for("index"))
    return render_template("index.html", todos=todos)


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    delete_todo(todo_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # 通常は host 引数を指定しなくても 127.0.0.1 に bind されますが
    # 念の為に 127.0.0.1 を明示的に指定することにします
    # Ref. https://flask.palletsprojects.com/en/stable/api/#application-object
    app.run(debug=True, host='127.0.0.1')