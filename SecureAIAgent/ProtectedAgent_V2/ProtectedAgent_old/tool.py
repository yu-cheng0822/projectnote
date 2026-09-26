from data.database import Database


class ToolExecutor:

    def __init__(self):

        # ========================================
        # Database
        # ========================================

        self.database = Database()

        # ========================================
        # Available Tools
        # ========================================

        self.tools = {
            "calculator": self.calculator,
            "recovery": self.recovery,
            "file": self.file,
            "database": self.database_tool
        }

    # ========================================
    # Execute Tool
    # ========================================

    def execute(
        self,
        tool_name,
        input_data=None
    ):

        if tool_name not in self.tools:

            return False, "unknown_tool"

        try:

            result = self.tools[tool_name](
                input_data
            )

            # ------------------------------------
            # Calculator Error
            # ------------------------------------

            if (
                tool_name == "calculator"
                and result in [
                    "invalid_expression",
                    "calculation_error"
                ]
            ):

                return False, result

            # ------------------------------------
            # Database Error
            # ------------------------------------

            if (
                tool_name == "database"
                and result in [
                    "missing_database_query",
                    "unknown_database_query"
                ]
            ):

                return False, result

            return True, result

        except Exception as e:

            return False, str(e)

    # ========================================
    # Calculator
    # ========================================

    def calculator(
        self,
        expression
    ):

        print(
            "\n[DEBUG] Calculator Input:"
        )

        print(
            repr(expression)
        )

        try:

            if expression is None:

                return "invalid_expression"

            expression = expression.strip()

            if not expression:

                return "invalid_expression"

            # ------------------------------------
            # Allow only basic mathematics
            # ------------------------------------

            allowed_chars = (
                "0123456789"
                "+-*/(). "
            )

            for char in expression:

                if char not in allowed_chars:

                    print(
                        "[DEBUG] Invalid Character:",
                        repr(char)
                    )

                    return "invalid_expression"

            # ------------------------------------
            # Calculation
            # ------------------------------------

            result = eval(
                expression,
                {
                    "__builtins__": {}
                }
            )

            return result

        except Exception as e:

            print(
                "[DEBUG] Calculator Error:",
                repr(e)
            )

            return "calculation_error"

    # ========================================
    # Recovery
    # ========================================

    def recovery(
        self,
        data=None
    ):

        return "recovery_action_completed"

    # ========================================
    # File
    # ========================================

    def file(
        self,
        data=None
    ):

        return "file_operation_completed"

    # ========================================
    # Database Tool
    # ========================================

    def database_tool(
        self,
        query=None
    ):

        if query is None:

            return "missing_database_query"

        query = query.strip()

        if not query:

            return "missing_database_query"

        # ========================================
        # Query format:
        #
        # users
        # users | name=Alice
        # accounts | username=alice
        # sensitive_data | user_id=U001
        # ========================================

        parts = [
            part.strip()
            for part in query.split("|")
        ]

        dataset = parts[0].lower()

        filters = {}

        for part in parts[1:]:

            if "=" not in part:
                continue

            key, value = part.split(
                "=",
                1
            )

            key = key.strip().lower()
            value = value.strip()

            filters[key] = value

        # ========================================
        # Users
        # ========================================

        if dataset == "users":

            return self.database.get_users(
                user_id=filters.get(
                    "user_id"
                ),
                name=filters.get(
                    "name"
                )
            )

        # ========================================
        # Accounts
        # ========================================

        if dataset == "accounts":

            return self.database.get_accounts(
                account_id=filters.get(
                    "account_id"
                ),
                username=filters.get(
                    "username"
                )
            )

        # ========================================
        # Sensitive Data
        # ========================================

        if dataset == "sensitive_data":

            return self.database.get_sensitive_data(
                user_id=filters.get(
                    "user_id"
                )
            )

        # ========================================
        # Unknown Dataset
        # ========================================

        return "unknown_database_query"


# ============================================
# Tool Executor Test
# ============================================

if __name__ == "__main__":

    executor = ToolExecutor()

    print(
        "===== Tool Executor Test ====="
    )

    # ========================================
    # Calculator
    # ========================================

    success, result = executor.execute(
        "calculator",
        "123 * 456"
    )

    print(
        "\nCalculator:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Calculator Error
    # ========================================

    success, result = executor.execute(
        "calculator",
        "python main.py"
    )

    print(
        "\nCalculator Error:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Recovery
    # ========================================

    success, result = executor.execute(
        "recovery"
    )

    print(
        "\nRecovery:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Database - All Users
    # ========================================

    success, result = executor.execute(
        "database",
        "users"
    )

    print(
        "\nDatabase - All Users:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Database - Alice
    # ========================================

    success, result = executor.execute(
        "database",
        "users | name=Alice"
    )

    print(
        "\nDatabase - User Alice:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Database - Alice Account
    # ========================================

    success, result = executor.execute(
        "database",
        "accounts | username=alice"
    )

    print(
        "\nDatabase - Account Alice:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Database - Sensitive Data
    # ========================================

    success, result = executor.execute(
        "database",
        "sensitive_data | user_id=U001"
    )

    print(
        "\nDatabase - Sensitive Data U001:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )

    # ========================================
    # Unknown Tool
    # ========================================

    success, result = executor.execute(
        "unknown"
    )

    print(
        "\nUnknown Tool:"
    )

    print(
        "Success:",
        success
    )

    print(
        "Result:",
        result
    )