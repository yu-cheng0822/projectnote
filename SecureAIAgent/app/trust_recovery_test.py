from agent import Agent


def main():

    print("========================================")
    print("       Dynamic Trust Recovery Test")
    print("========================================")

    # 建立新的 Agent
    agent = Agent()

    print("\n初始 Trust Score:", agent.trust.get_score())
    print("初始 Trust Level:", agent.trust.get_level())

    # ========================================
    # Phase 1：製造異常行為
    # ========================================

    print("\n\n========================================")
    print(" Phase 1: Simulate Malicious Behavior")
    print("========================================")

    for i in range(3):

        print(f"\n----- Unauthorized Request {i + 1} -----")

        agent.execute_tool("database")

        print(
            "Trust Score:",
            agent.trust.get_score()
        )

        print(
            "Trust Level:",
            agent.trust.get_level()
        )

    # ========================================
    # Phase 2：確認 Agent 已進入 LOW
    # ========================================

    print("\n\n========================================")
    print(" Phase 2: Check Trust Degradation")
    print("========================================")

    print("Current Trust Score:", agent.trust.get_score())
    print("Current Trust Level:", agent.trust.get_level())

    # ========================================
    # Phase 3：開始 Recovery
    # ========================================

    print("\n\n========================================")
    print(" Phase 3: Trust Recovery")
    print("========================================")

    for i in range(3):

        print(f"\n----- Recovery Request {i + 1} -----")

        agent.execute_tool(
            "recovery"
        )

        print(
            "Trust Score:",
            agent.trust.get_score()
        )

        print(
            "Trust Level:",
            agent.trust.get_level()
        )

    # ========================================
    # Phase 4：最終狀態
    # ========================================

    print("\n\n========================================")
    print("       Final Security State")
    print("========================================")

    print("Final Trust Score:", agent.trust.get_score())
    print("Final Trust Level:", agent.trust.get_level())

    # ========================================
    # Security Event Log
    # ========================================

    print("\n===== Security Event Log =====")

    agent.logger.show_events()


if __name__ == "__main__":
    main()