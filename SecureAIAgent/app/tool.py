class ToolExecutor:

    def __init__(self):
        self.tools = {
            "calculator": self.calculator,
            "recovery": self.recovery,
            "file": self.file,
            "database": self.database
        }

    # ========================================
    # Execute Tool
    # ========================================

    def execute(self, tool_name, input_data=None):

        if tool_name not in self.tools:
            return False, "unknown_tool"

        try:

            result = self.tools[tool_name](
                input_data
            )

            return True, result

        except Exception as e:

            return False, str(e)

    # ========================================
    # Calculator
    # ========================================

    def calculator(self, expression):

        try:

            # 目前先限制只能做基本數學運算
            allowed_chars = (
                "0123456789"
                "+-*/(). "
            )

            for char in expression:

                if char not in allowed_chars:
                    return "invalid_expression"

            result = eval(
                expression,
                {
                    "__builtins__": {}
                }
            )

            return result

        except Exception:

            return "calculation_error"

    # ========================================
    # Recovery
    # ========================================

    def recovery(self, data=None):

        return "recovery_action_completed"

    # ========================================
    # File
    # ========================================

    def file(self, data=None):

        return "file_operation_completed"

    # ========================================
    # Database
    # ========================================

    def database(self, data=None):

        return "database_operation_completed"


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    executor = ToolExecutor()

    print("===== Tool Executor Test =====")

    success, result = executor.execute(
        "calculator",
        "123 * 456"
    )

    print("\nCalculator:")

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    success, result = executor.execute(
        "recovery"
    )

    print("\nRecovery:")

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    success, result = executor.execute(
        "unknown"
    )

    print("\nUnknown Tool:")

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )