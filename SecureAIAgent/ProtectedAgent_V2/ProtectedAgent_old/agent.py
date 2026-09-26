import json
import re

from llm import LocalLLM
from tool import ToolExecutor


class Agent:

    def __init__(
        self,
        agent_id="agent_001",
        llm=None,
        tool_executor=None,
        session_id="session_001"
    ):

        # ========================================
        # Agent Basic Information
        # ========================================

        self.agent_id = agent_id
        self.session_id = session_id

        # ========================================
        # LLM
        # ========================================

        if llm is None:
            self.llm = LocalLLM()
        else:
            self.llm = llm

        # ========================================
        # Tool Executor
        # ========================================

        if tool_executor is None:
            self.tool_executor = ToolExecutor()
        else:
            self.tool_executor = tool_executor

    # ==================================================
    # Determine Required Datasets
    # ==================================================

    def get_required_datasets(self, user_input):

        text = user_input.lower()

        required = []

        # ----------------------------------------
        # Accounts
        # ----------------------------------------

        account_keywords = [
            "帳號",
            "賬號",
            "account",
            "username",
            "角色",
            "role"
        ]

        if any(
            keyword in text
            for keyword in account_keywords
        ):

            required.append("accounts")

        # ----------------------------------------
        # Users
        # ----------------------------------------

        user_keywords = [
            "個人資料",
            "個人資訊",
            "使用者資料",
            "使用者資訊",
            "user information",
            "email",
            "電話",
            "phone",
            "姓名",
            "使用者"
        ]

        if any(
            keyword in text
            for keyword in user_keywords
        ):

            required.append("users")

        # ----------------------------------------
        # Sensitive Data
        # ----------------------------------------

        sensitive_keywords = [
            "敏感資料",
            "敏感資訊",
            "私人資訊",
            "private information",
            "private_information",
            "地址",
            "個資"
        ]

        if any(
            keyword in text
            for keyword in sensitive_keywords
        ):

            required.append("sensitive_data")

        # ----------------------------------------
        # Generic data request
        # ----------------------------------------

        if (
            "資料" in text
            and not required
        ):

            required.append("users")

        return required

    # ==================================================
    # Get Completed Datasets
    # ==================================================

    def get_completed_datasets(
        self,
        tool_history
    ):

        completed = []

        for record in tool_history:

            if record.get("tool") != "database":
                continue

            if not record.get("success"):
                continue

            query = record.get(
                "input",
                ""
            )

            dataset = query.split(
                "|",
                1
            )[0].strip().lower()

            if dataset not in completed:

                completed.append(
                    dataset
                )

        return completed

    # ==================================================
    # Get Successful Database Records
    # ==================================================

    def get_database_records(
        self,
        tool_history,
        dataset
    ):

        records = []

        for record in tool_history:

            if record.get("tool") != "database":
                continue

            if not record.get("success"):
                continue

            query = record.get(
                "input",
                ""
            )

            current_dataset = query.split(
                "|",
                1
            )[0].strip().lower()

            if current_dataset == dataset:

                result = record.get(
                    "result"
                )

                if isinstance(
                    result,
                    list
                ):

                    records.extend(
                        result
                    )

        return records

    # ==================================================
    # Check Successful Query
    # ==================================================

    def has_successful_query(
        self,
        tool_history,
        query
    ):

        normalized = (
            query.strip().lower()
        )

        for record in tool_history:

            if not record.get("success"):
                continue

            old_query = record.get(
                "input",
                ""
            ).strip().lower()

            if old_query == normalized:

                return True

        return False

    # ==================================================
    # Extract Person / User Information
    # ==================================================

    def extract_person_name(
        self,
        user_input
    ):

        text = user_input.strip()

        # ----------------------------------------
        # 已知資料庫名稱
        # ----------------------------------------

        known_names = [
            "alice",
            "bob",
            "charlie"
        ]

        lower_text = text.lower()

        for name in known_names:

            if name in lower_text:

                return name.capitalize()

        return None

    # ==================================================
    # Extract User ID
    # ==================================================

    def extract_user_id(
        self,
        user_input
    ):

        match = re.search(
            r"\bU\d{3}\b",
            user_input,
            re.IGNORECASE
        )

        if match:

            return match.group(0).upper()

        return None

    # ==================================================
    # Extract Username
    # ==================================================

    def extract_username(
        self,
        user_input
    ):

        person_name = (
            self.extract_person_name(
                user_input
            )
        )

        if person_name:

            return person_name.lower()

        return None

    # ==================================================
    # Build Database Query
    # ==================================================

    def build_database_query(
        self,
        dataset,
        user_input,
        tool_history
    ):

        # ========================================
        # Accounts
        # ========================================

        if dataset == "accounts":

            # ------------------------------------
            # 優先使用已查詢 Users 的結果
            # ------------------------------------

            users = (
                self.get_database_records(
                    tool_history,
                    "users"
                )
            )

            if users:

                name = users[0].get(
                    "name"
                )

                if name:

                    return (
                        "accounts | username="
                        + str(name).lower()
                    )

            # ------------------------------------
            # 從原始輸入取得名稱
            # ------------------------------------

            username = (
                self.extract_username(
                    user_input
                )
            )

            if username:

                return (
                    "accounts | username="
                    + username
                )

            # ------------------------------------
            # 沒有指定對象
            # ------------------------------------

            return "accounts"

        # ========================================
        # Users
        # ========================================

        if dataset == "users":

            # ------------------------------------
            # 優先使用已查詢 Accounts 的結果
            # ------------------------------------

            accounts = (
                self.get_database_records(
                    tool_history,
                    "accounts"
                )
            )

            if accounts:

                username = accounts[0].get(
                    "username"
                )

                if username:

                    return (
                        "users | name="
                        + str(username).capitalize()
                    )

            # ------------------------------------
            # User ID
            # ------------------------------------

            user_id = (
                self.extract_user_id(
                    user_input
                )
            )

            if user_id:

                return (
                    "users | user_id="
                    + user_id
                )

            # ------------------------------------
            # Name
            # ------------------------------------

            name = (
                self.extract_person_name(
                    user_input
                )
            )

            if name:

                return (
                    "users | name="
                    + name
                )

            return "users"

        # ========================================
        # Sensitive Data
        # ========================================

        if dataset == "sensitive_data":

            # ------------------------------------
            # 優先使用 Users 查詢結果
            # ------------------------------------

            users = (
                self.get_database_records(
                    tool_history,
                    "users"
                )
            )

            if users:

                user_id = users[0].get(
                    "user_id"
                )

                if user_id:

                    return (
                        "sensitive_data | user_id="
                        + str(user_id)
                    )

            # ------------------------------------
            # User ID
            # ------------------------------------

            user_id = (
                self.extract_user_id(
                    user_input
                )
            )

            if user_id:

                return (
                    "sensitive_data | user_id="
                    + user_id
                )

            return "sensitive_data"

        return dataset

    # ==================================================
    # Validate Decision
    # ==================================================

    def validate_decision(
        self,
        decision,
        user_input,
        missing_datasets,
        tool_history
    ):

        # ========================================
        # 已經沒有缺少的資料
        # ========================================

        if not missing_datasets:

            return "FINAL"

        # ========================================
        # 如果 LLM 誤判成 CALCULATE
        # 但使用者其實是在查資料
        # ========================================

        if decision.upper().startswith(
            "CALCULATE:"
        ):

            if missing_datasets:

                query = (
                    self.build_database_query(
                        missing_datasets[0],
                        user_input,
                        tool_history
                    )
                )

                return (
                    "DATABASE: "
                    + query
                )

        # ========================================
        # Database Decision
        # ========================================

        if decision.upper().startswith(
            "DATABASE:"
        ):

            query = self.extract_database_query(
                decision
            )

            dataset = query.split(
                "|",
                1
            )[0].strip().lower()

            # ------------------------------------
            # LLM 選到了已經完成的 dataset
            # ------------------------------------

            if dataset not in missing_datasets:

                query = (
                    self.build_database_query(
                        missing_datasets[0],
                        user_input,
                        tool_history
                    )
                )

                return (
                    "DATABASE: "
                    + query
                )

            # ------------------------------------
            # 驗證成功
            # ------------------------------------

            return decision

        # ========================================
        # LLM 太早 FINAL
        # ========================================

        if decision.upper() == "FINAL":

            query = (
                self.build_database_query(
                    missing_datasets[0],
                    user_input,
                    tool_history
                )
            )

            return (
                "DATABASE: "
                + query
            )

        # ========================================
        # 任何其他錯誤輸出
        # ========================================

        query = (
            self.build_database_query(
                missing_datasets[0],
                user_input,
                tool_history
            )
        )

        return (
            "DATABASE: "
            + query
        )

    # ==================================================
    # Agent Decision
    # ==================================================

    def decide(
        self,
        user_input,
        tool_history=None,
        missing_datasets=None
    ):

        if tool_history is None:
            tool_history = []

        if missing_datasets is None:
            missing_datasets = []

        history_text = json.dumps(
            tool_history,
            ensure_ascii=False,
            indent=2
        )

        prompt = f"""
You are an autonomous AI assistant.

Understand the user's request and select
ONE tool for the next step.

==================================================
USER REQUEST
==================================================

{user_input}


==================================================
TOOL HISTORY
==================================================

{history_text}


==================================================
AVAILABLE TOOLS
==================================================

Calculator:

CALCULATE: <expression>


Database:

DATABASE: users

DATABASE: users | name=Alice

DATABASE: users | user_id=U001

DATABASE: accounts

DATABASE: accounts | username=alice

DATABASE: accounts | account_id=A001

DATABASE: sensitive_data

DATABASE: sensitive_data | user_id=U001


==================================================
STRICT RULES
==================================================

1. Output exactly ONE decision.

2. Never output multiple decisions.

3. Use CALCULATE only for actual mathematics.

4. Use DATABASE for data requests.

5. Never use SQL.

6. Never put field comparisons inside CALCULATE.

7. Never invent values.

8. Do not repeat a successful database query.

9. If multiple datasets are required,
   query exactly ONE dataset at a time.

10. Do not output FINAL while required information
    is still missing.


==================================================
MISSING DATASETS
==================================================

{", ".join(missing_datasets)}


==================================================
VALID OUTPUT
==================================================

CALCULATE: 123 * 456

DATABASE: users | name=Alice

DATABASE: accounts | username=alice

FINAL
"""

        raw_decision = self.llm.generate(
            prompt
        )

        return self.normalize_decision(
            raw_decision
        )

    # ==================================================
    # Normalize Decision
    # ==================================================

    def normalize_decision(
        self,
        raw_decision
    ):

        if raw_decision is None:
            return "FINAL"

        raw_decision = raw_decision.strip()

        if not raw_decision:
            return "FINAL"

        lines = raw_decision.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            upper_line = line.upper()

            if upper_line.startswith(
                "CALCULATE:"
            ):

                return line

            if upper_line.startswith(
                "DATABASE:"
            ):

                return line

            if upper_line == "FINAL":

                return "FINAL"

        return "FINAL"

    # ==================================================
    # Extract Calculator Expression
    # ==================================================

    def extract_expression(
        self,
        decision
    ):

        prefix = "CALCULATE:"

        position = decision.upper().find(
            prefix
        )

        if position == -1:

            return ""

        expression = decision[
            position + len(prefix):
        ]

        return expression.strip()

    # ==================================================
    # Validate Calculator Expression
    # ==================================================

    def is_valid_calculator_expression(
        self,
        expression
    ):

        if not expression:
            return False

        expression = expression.strip()

        pattern = r"^[0-9+\-*/().\s]+$"

        return bool(
            re.fullmatch(
                pattern,
                expression
            )
        )

    # ==================================================
    # Extract Database Query
    # ==================================================

    def extract_database_query(
        self,
        decision
    ):

        prefix = "DATABASE:"

        position = decision.upper().find(
            prefix
        )

        if position == -1:

            return ""

        query = decision[
            position + len(prefix):
        ]

        return query.strip()

    # ==================================================
    # Generate Final Answer
    # ==================================================

    def generate_final_answer(
        self,
        user_input,
        tool_history
    ):

        # ========================================
        # Calculator
        # ========================================

        for record in tool_history:

            if (
                record.get("tool")
                == "calculator"
                and record.get("success")
            ):

                result = record.get(
                    "result"
                )

                return (
                    f"計算結果：{result}"
                )

        # ========================================
        # Database
        # ========================================

        answer_parts = []

        accounts = (
            self.get_database_records(
                tool_history,
                "accounts"
            )
        )

        users = (
            self.get_database_records(
                tool_history,
                "users"
            )
        )

        sensitive_data = (
            self.get_database_records(
                tool_history,
                "sensitive_data"
            )
        )

        # ----------------------------------------
        # Accounts
        # ----------------------------------------

        if accounts:

            answer_parts.append(
                "帳號資訊："
            )

            for record in accounts:

                for key, value in record.items():

                    answer_parts.append(
                        f"{key}: {value}"
                    )

        # ----------------------------------------
        # Users
        # ----------------------------------------

        if users:

            answer_parts.append(
                "個人資料："
            )

            for record in users:

                for key, value in record.items():

                    answer_parts.append(
                        f"{key}: {value}"
                    )

        # ----------------------------------------
        # Sensitive Data
        # ----------------------------------------

        if sensitive_data:

            answer_parts.append(
                "敏感資料："
            )

            for record in sensitive_data:

                for key, value in record.items():

                    answer_parts.append(
                        f"{key}: {value}"
                    )

        # ----------------------------------------
        # 有資料
        # ----------------------------------------

        if answer_parts:

            return "\n".join(
                answer_parts
            )

        # ========================================
        # General Conversation
        # ========================================

        prompt = f"""
You are a helpful AI assistant.

User request:

{user_input}

Answer in Traditional Chinese.

Do not invent facts.
"""

        answer = self.llm.generate(
            prompt
        )

        return answer.strip()

    # ==================================================
    # Main Agent Run
    # ==================================================

    def run(
        self,
        user_input
    ):

        tool_history = []

        max_tool_calls = 5

        required_datasets = (
            self.get_required_datasets(
                user_input
            )
        )

        # ========================================
        # No database required
        # ========================================

        if not required_datasets:

            decision = self.decide(
                user_input,
                tool_history,
                []
            )

            print(
                "\n===== Agent Decision "
                "(Step 1) ====="
            )

            print(
                decision
            )

            if decision.upper().startswith(
                "CALCULATE:"
            ):

                expression = (
                    self.extract_expression(
                        decision
                    )
                )

                # --------------------------------
                # Calculator validation
                # --------------------------------

                if not self.is_valid_calculator_expression(
                    expression
                ):

                    final_answer = (
                        "無法執行這個計算要求，"
                        "因為輸入不是有效的數學運算式。"
                    )

                    print(
                        "\n===== AI Answer ====="
                    )

                    print(final_answer)

                    return {
                        "decision": "FINAL",
                        "tool": "calculator",
                        "tool_history": [],
                        "answer": final_answer
                    }

                success, result = (
                    self.tool_executor.execute(
                        "calculator",
                        expression
                    )
                )

                tool_history.append(
                    {
                        "tool": "calculator",
                        "input": expression,
                        "success": success,
                        "result": result
                    }
                )

                print(
                    "\n===== Tool Result ====="
                )

                print(
                    "Tool: calculator"
                )

                print(
                    "Success:",
                    success
                )

                print(
                    "Result:",
                    result
                )

                if success:

                    final_answer = (
                        f"計算結果：{result}"
                    )

                else:

                    final_answer = (
                        f"計算失敗：{result}"
                    )

                print(
                    "\n===== AI Answer ====="
                )

                print(final_answer)

                return {
                    "decision": "FINAL",
                    "tool": "calculator",
                    "tool_history": tool_history,
                    "answer": final_answer
                }

            # ------------------------------------
            # Normal conversation
            # ------------------------------------

            final_answer = (
                decision
            )

            print(
                "\n===== AI Answer ====="
            )

            print(final_answer)

            return {
                "decision": "FINAL",
                "tool": None,
                "tool_history": [],
                "answer": final_answer
            }

        # ========================================
        # Database Agent Loop
        # ========================================

        for step in range(
            max_tool_calls
        ):

            completed_datasets = (
                self.get_completed_datasets(
                    tool_history
                )
            )

            missing_datasets = [
                dataset
                for dataset in required_datasets
                if dataset not in completed_datasets
            ]

            # ------------------------------------
            # All required data collected
            # ------------------------------------

            if not missing_datasets:

                final_answer = (
                    self.generate_final_answer(
                        user_input,
                        tool_history
                    )
                )

                print(
                    "\n===== AI Answer ====="
                )

                print(final_answer)

                return {
                    "decision": "FINAL",
                    "tool": None,
                    "tool_history": tool_history,
                    "answer": final_answer
                }

            # ------------------------------------
            # LLM Decision
            # ------------------------------------

            raw_decision = self.decide(
                user_input,
                tool_history,
                missing_datasets
            )

            # ------------------------------------
            # Controller validates LLM decision
            # ------------------------------------

            decision = (
                self.validate_decision(
                    raw_decision,
                    user_input,
                    missing_datasets,
                    tool_history
                )
            )

            print(
                f"\n===== Agent Decision "
                f"(Step {step + 1}) ====="
            )

            print(decision)

            # ====================================
            # DATABASE
            # ====================================

            if decision.upper().startswith(
                "DATABASE:"
            ):

                query = (
                    self.extract_database_query(
                        decision
                    )
                )

                # --------------------------------
                # Prevent duplicate queries
                # --------------------------------

                if self.has_successful_query(
                    tool_history,
                    query
                ):

                    query = (
                        self.build_database_query(
                            missing_datasets[0],
                            user_input,
                            tool_history
                        )
                    )

                    if self.has_successful_query(
                        tool_history,
                        query
                    ):

                        break

                print(
                    "\n[DEBUG] Database Query:"
                )

                print(
                    repr(query)
                )

                success, result = (
                    self.tool_executor.execute(
                        "database",
                        query
                    )
                )

                tool_history.append(
                    {
                        "tool": "database",
                        "input": query,
                        "success": success,
                        "result": result
                    }
                )

                print(
                    "\n===== Tool Result ====="
                )

                print(
                    "Tool: database"
                )

                print(
                    "Success:",
                    success
                )

                print(
                    "Result:",
                    result
                )

                if not success:

                    final_answer = (
                        f"資料查詢失敗：{result}"
                    )

                    print(
                        "\n===== AI Answer ====="
                    )

                    print(final_answer)

                    return {
                        "decision": "FINAL",
                        "tool": "database",
                        "tool_history": tool_history,
                        "answer": final_answer
                    }

                continue

            # ====================================
            # Unexpected Calculator
            # ====================================

            if decision.upper().startswith(
                "CALCULATE:"
            ):

                query = (
                    self.build_database_query(
                        missing_datasets[0],
                        user_input,
                        tool_history
                    )
                )

                print(
                    "\n[Agent Controller]"
                )

                print(
                    "LLM returned an invalid "
                    "calculation decision."
                )

                print(
                    "Switching to database query:"
                )

                print(
                    query
                )

                success, result = (
                    self.tool_executor.execute(
                        "database",
                        query
                    )
                )

                tool_history.append(
                    {
                        "tool": "database",
                        "input": query,
                        "success": success,
                        "result": result
                    }
                )

                print(
                    "\n===== Tool Result ====="
                )

                print(
                    "Tool: database"
                )

                print(
                    "Success:",
                    success
                )

                print(
                    "Result:",
                    result
                )

                continue

        # ========================================
        # Maximum Tool Calls
        # ========================================

        final_answer = (
            self.generate_final_answer(
                user_input,
                tool_history
            )
        )

        print(
            "\n===== AI Answer ====="
        )

        print(final_answer)

        return {
            "decision": "FINAL",
            "tool": None,
            "tool_history": tool_history,
            "answer": final_answer
        }


# ==================================================
# Direct Execution
# ==================================================

if __name__ == "__main__":

    print(
        "Please run ProtectedAgent through main.py"
    )