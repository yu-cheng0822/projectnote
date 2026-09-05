from tools.base import Tool


class CalculatorTool(Tool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="執行基本數學運算"
        )

    def execute(self, expression):
        try:
            result = eval(expression, {"__builtins__": None}, {})
            return result
        except Exception:
            return None