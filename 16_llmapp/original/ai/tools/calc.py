import ast
import operator

from langchain.tools import tool

# 文字列から安全に計算を行うためのクラス
# 例えば "3 + 4 * 5" が与えられたときに "23" を返すようにします
# eval を使ってしまうと危険なので使わないようにしています
class Calculator:
    ALLOWED_OPS = {
        ast.Add: operator.add,      # +
        ast.Sub: operator.sub,      # -
        ast.Mult: operator.mul,     # *
        ast.Div: operator.truediv,  # /
        ast.FloorDiv: operator.floordiv,  # //
        ast.Mod: operator.mod,      # %
        ast.Pow: operator.pow,      # **
        ast.USub: operator.neg,     # -（単項マイナス）
        ast.UAdd: operator.pos,     # +（単項プラス）
    }
    
    @classmethod
    def calc_core(K, expression):
        is_error = True
        result = None
        try:
            tree = ast.parse(expression, mode='eval')
            result = K.eval_node(tree.body)
            is_error = False
        except Exception as e:
            result = e.value
        finally:
            result = {
                "expression": expression,
                "result": result,
                "is_error": is_error
            }
        return result

    @classmethod
    def eval_node(K, node):
        # 定数 (Python 3.8以降??)
        if isinstance(node, ast.Constant):
            return node.value
        
        # 二項演算
        elif isinstance(node, ast.BinOp):
            left, op_type, right = K.eval_node(node.left), type(node.op), K.eval_node(node.right)
            if op_type in K.ALLOWED_OPS:
                return K.ALLOWED_OPS[op_type](left, right)
            else:
                raise ValueError(f"Not alloeed operator: {op_type}")
            
        # 単項演算
        elif isinstance(node, ast.UnaryOp):
            operand, op_type = K.eval_node(node.operand), type(node.op)
            if op_type in K.ALLOWED_OPS:
                return K.ALLOWED_OPS[op_type](operand)
            else:
                raise ValueError(f"Not allowed operator: {op_type}")
            
        # その他は演算不可
        else:
            raise ValueError(f"Not allowed node: {type(node)}")


# LLM は統計による推論が得意なのでデータにない無数の組み合わせのある計算などは苦手と考えて
# それらの単純計算がこなせるように実装してみます
class CalculatorTool:
    # Langchain ではアノテーション (****:int) 部分で LLM に型を渡すので必須
    # ※ そうでなくても型の明示的な宣言は良い習慣
    @tool
    @staticmethod
    def calc(expression : str) -> str:
        """文字列の計算式から計算結果を導出します、変数は扱えないので予め数値を代入してください
        Args:
            expression: Python で解釈できる計算式を入力してください 例: "3 + (4 * 5)"
                        変数は入れることができません、もし変数の中身がわかっている場合は変数を数値に代入してください
        """
        # 上のドキュメントも必要です (ただし LLM にわたるので関数のドキュメント化とは少し違います)

        try:
            result = Calculator.calc_core(expression)
            is_error = result["is_error"]
            answer   = result["result"]

            if is_error:
                response = f"計算に失敗しました  計算式は {expression} です"
            else:
                response = f"計算結果は {answer} でした  計算式は {expression} です"
        except:
            response = "すみませんエラーが発生して計算を行うことが出来ませんでした"

        return response
    
    
    @classmethod
    def get_tool(cls):
        return cls.calc
