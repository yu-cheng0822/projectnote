
class SecurityGateway:
    """
    Security Gateway

    集中處理：
    1. 工具請求
    2. 身分與權限檢查
    3. 動態信任檢查
    4. 工具執行
    5. 安全事件記錄
    6. 動態信任更新
    """

    def __init__(
        self,
        identity,
        trust,
        policy,
        tool_executor,
        logger,
        agent_id,
        session_id
    ):
        self.identity = identity
        self.trust = trust
        self.policy = policy
        self.tool_executor = tool_executor
        self.logger = logger

        self.agent_id = agent_id
        self.session_id = session_id

    def request_tool(self, tool_name):
        """
        處理工具請求，並進行安全政策檢查。
        """

        print("\n===== Security Gateway =====")
        print("Agent:", self.agent_id)
        print("Session:", self.session_id)
        print("Tool Request:", tool_name)
        print("Trust Score:", self.trust.get_score())
        print("Trust Level:", self.trust.get_level())

        # 使用原本的 PolicyEngine 進行檢查
        allowed, reason = self.policy.check(tool_name)

        if allowed:
            print("Policy Decision: ALLOW")
            print("Reason:", reason)

            return True, reason

        print("Policy Decision: DENY")
        print("Reason:", reason)

        # 信任過低時，不重複扣除信任分數
        if reason == "trust_too_low":
            print("\n===== Dynamic Trust Update =====")
            print("Event Result: DENY")
            print("Tool:", tool_name)
            print("Trust Score Unchanged:", self.trust.get_score())
            print("Trust Level Unchanged:", self.trust.get_level())
        else:
            self.trust.decrease(20)

            print("\n===== Dynamic Trust Update =====")
            print("Event Result: DENY")
            print("Tool:", tool_name)
            print("New Trust Score:", self.trust.get_score())
            print("New Trust Level:", self.trust.get_level())

        # 記錄安全事件
        self.logger.log(
            self.agent_id,
            self.session_id,
            tool_name,
            "REQUEST",
            "DENY"
        )

        return False, reason

    def execute_tool(self, tool_name, input_data=None):
        """
        先進行安全檢查，允許後才執行工具。
        """

        allowed, reason = self.request_tool(tool_name)

        if not allowed:
            return False, reason

        print("\n===== Tool Execution =====")
        print("Tool:", tool_name)

        success, result = self.tool_executor.execute(
            tool_name,
            input_data
        )

        if success:
            event_result = "ALLOW"

            # Recovery 成功時，信任分數增加較多
            if tool_name == "recovery":
                self.trust.increase(5)
            else:
                self.trust.increase(1)

            print("Execution Status: SUCCESS")
            print("Result:", result)

        else:
            event_result = "FAIL"

            print("Execution Status: FAILED")
            print("Result:", result)

        # 記錄工具執行事件
        self.logger.log(
            self.agent_id,
            self.session_id,
            tool_name,
            "EXECUTE",
            event_result
        )

        print("\n===== Dynamic Trust Update =====")
        print("Event Result:", event_result)
        print("Tool:", tool_name)
        print("New Trust Score:", self.trust.get_score())
        print("New Trust Level:", self.trust.get_level())

        return success, result