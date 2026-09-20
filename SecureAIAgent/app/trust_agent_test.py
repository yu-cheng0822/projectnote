from agent import Agent


def main():

    print("========================================")
    print("      Dynamic Trust Security Test")
    print("========================================")

    # 建立新的 Agent
    agent = Agent()

    print("\n初始 Trust Score:", agent.trust.get_score())
    print("初始 Trust Level:", agent.trust.get_level())

    # ========================================
    # 測試 1：嘗試存取未授權的 database
    # ========================================

    print("\n\n===== Test 1: Unauthorized Database Request =====")

    agent.execute_tool("database")

    print("\n目前 Trust Score:", agent.trust.get_score())
    print("目前 Trust Level:", agent.trust.get_level())

    # ========================================
    # 測試 2：再次嘗試 database
    # ========================================

    print("\n\n===== Test 2: Repeated Unauthorized Request =====")

    agent.execute_tool("database")

    print("\n目前 Trust Score:", agent.trust.get_score())
    print("目前 Trust Level:", agent.trust.get_level())

    # ========================================
    # 測試 3：第三次嘗試 database
    # ========================================

    print("\n\n===== Test 3: Repeated Unauthorized Request =====")

    agent.execute_tool("database")

    print("\n目前 Trust Score:", agent.trust.get_score())
    print("目前 Trust Level:", agent.trust.get_level())

    # ========================================
    # 測試 4：Trust 降低後，嘗試合法 calculator
    # ========================================

    print("\n\n===== Test 4: Calculator After Trust Degradation =====")

    result = agent.execute_tool(
        "calculator",
        "123 * 456"
    )

    print("\nCalculator Result:")
    print(result)

    # ========================================
    # 最終狀態
    # ========================================

    print("\n\n========================================")
    print("           Final Security State")
    print("========================================")

    print("Final Trust Score:", agent.trust.get_score())
    print("Final Trust Level:", agent.trust.get_level())

    # ========================================
    # 顯示完整 Security Event
    # ========================================

    print("\n===== Security Event Log =====")
    agent.logger.show_events()


if __name__ == "__main__":
    main()