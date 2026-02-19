import pytest
from authenticator import Authenticator

# 以下のコマンドで Authenticator クラスのユニットテストを実行することができます (CUIで行う場合)
# $ pytest

def test_registerメソッドでユーザが正しく登録されるか():
    auth = Authenticator()
    username, password = "user", "password"
    auth.register(username, password)
    assert auth.users.get(username, None) == password


def test_registerメソッドですでに存在するユーザー名で登録を試みた場合にエラーメッセージが出力されるか():
    auth = Authenticator()
    username, password = "user", "password"
    auth.register(username, password)
    with pytest.raises(ValueError) as e:
        auth.register(username, password)
    assert isinstance(e.value, ValueError)
    assert str(e.value) == "エラー: ユーザーは既に存在します。"


def test_loginメソッドで正しいユーザー名とパスワードでログインできるか():
    auth = Authenticator()
    username, password = "user", "password"
    auth.register(username, password)
    result = auth.login(username, password)
    assert result == "ログイン成功"


def test_loginメソッドで誤ったパスワードでエラーが出るか():
    auth = Authenticator()
    username, password = "user", "password"
    auth.register(username, password)
    with pytest.raises(ValueError) as e:
        auth.login(username, password+"worng")
    assert isinstance(e.value, ValueError)
    assert str(e.value) == "エラー: ユーザー名またはパスワードが正しくありません。"