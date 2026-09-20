from agent import Agent


def print_trust(agent, title):
    print(f"\n===== {title} =====")
    print("Trust Score:", agent.trust.get_score())
    print("Trust Level:", agent.trust.get_level())


def main():

    print("========================================")
    print("       Full Dynamic Trust Cycle Test")
    print("========================================")

    agent = Agent()

    print_trust(agent, "Initial Trust State")

    # ========================================
    # Phase 1：製造違規行為
    # ========================================

    print("\n\n========================================")
    print(" Phase 1: Unauthorized Access")
    print("========================================")

    for i in range(3):

        print(f"\n----- Unauthorized Database Request {i + 1} -----")

        agent.execute_tool("database")

        print_trust(
            agent,
            f"Trust After Unauthorized Request {i + 1}"
        )

    # ========================================
    # Phase 2：確認 Calculator 被阻擋
    # ========================================

    print("\n\n========================================")
    print(" Phase 2: Calculator Blocked")
    print("========================================")

    calculator_before_recovery = agent.execute_tool(
        "calculator",
        "123 * 456"
    )

    print("\nCalculator Before Recovery:")
    print(calculator_before_recovery)

    # ========================================
    # Phase 3：執行 Recovery
    # ========================================

    print("\n\n========================================")
    print(" Phase 3: Trust Recovery")
    print("========================================")

    for i in range(3):

        print(f"\n----- Recovery Request {i + 1} -----")

        agent.execute_tool("recovery")

        print_trust(
            agent,
            f"Trust After Recovery {i + 1}"
        )

    # ========================================
    # Phase 4：確認 Calculator 恢復
    # ========================================

    print("\n\n========================================")
    print(" Phase 4: Calculator Restored")
    print("========================================")

    calculator_after_recovery = agent.execute_tool(
        "calculator",
        "123 * 456"
    )

    print("\nCalculator After Recovery:")
    print(calculator_after_recovery)

    # ========================================
    # Phase 5：最終狀態
    # ========================================

    print("\n\n========================================")
    print("       Final Security State")
    print("========================================")

    print_trust(agent, "Final Trust State")

    # ========================================
    # Security Event Log
    # ========================================

    print("\n===== Security Event Log =====")

    agent.logger.show_events()


if __name__ == "__main__":
    main()