from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from logger import EventLogger
from tool import ToolExecutor
from security_gateway import SecurityGateway


def main():

    print("========================================")
    print("Security Gateway Test")
    print("========================================")

    # ========================================
    # 建立 Agent 身分
    # ========================================

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=["calculator", "recovery"]
    )

    # ========================================
    # 建立 Dynamic Trust
    # ========================================

    trust = TrustEngine(initial_score=100)

    # ========================================
    # 建立 Policy Engine
    # ========================================

    policy = PolicyEngine(
        identity=identity,
        trust=trust
    )

    # ========================================
    # 建立 Tool Executor
    # ========================================

    tool_executor = ToolExecutor()

    # ========================================
    # 建立 Event Logger
    # ========================================

    logger = EventLogger()

    # ========================================
    # 建立 Security Gateway
    # ========================================

    gateway = SecurityGateway(
        identity=identity,
        trust=trust,
        policy=policy,
        tool_executor=tool_executor,
        logger=logger,
        agent_id="agent_001",
        session_id="gateway_test_session"
    )

    # ========================================
    # Test 1
    # 重複使用未授權 Database
    # 目的：讓 Trust 從 HIGH 降到 LOW
    # ========================================

    print("\n\n===== Test 1: Repeated Unauthorized Database =====")

    for i in range(3):

        print(f"\n--- Database Request {i + 1} ---")

        success, result = gateway.execute_tool(
            "database",
            "SELECT * FROM users"
        )

        print("Test Result:", success, result)

    # ========================================
    # Test 2
    # Recovery
    # 目的：確認 LOW Trust 可以逐步恢復
    # ========================================

    print("\n\n===== Test 2: Recovery =====")

    for i in range(3):

        print(f"\n--- Recovery Request {i + 1} ---")

        success, result = gateway.execute_tool(
            "recovery"
        )

        print("Test Result:", success, result)

    # ========================================
    # Test 3
    # Calculator
    # 目的：確認 Trust 恢復後可以使用合法工具
    # ========================================

    print("\n\n===== Test 3: Calculator =====")

    success, result = gateway.execute_tool(
        "calculator",
        "123 * 456"
    )

    print("Test Result:", success, result)

    # ========================================
    # Final Trust Status
    # ========================================

    print("\n\n===== Final Trust Status =====")

    print("Final Trust Score:", trust.get_score())
    print("Final Trust Level:", trust.get_level())

    # ========================================
    # Security Event Log
    # ========================================

    print("\n\n===== Security Event Log =====")

    logger.show_events()


if __name__ == "__main__":
    main()