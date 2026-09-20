from agent import Agent


def show_agent_state(agent, name):
    print(f"\n===== {name} State =====")
    print("Agent ID:", agent.agent_id)
    print("Session ID:", agent.session_id)
    print("Trust Score:", agent.trust.get_score())
    print("Trust Level:", agent.trust.get_level())


def main():

    print("========================================")
    print("         Session Isolation Test")
    print("========================================")

    # ========================================
    # 建立 Session A
    # ========================================

    agent_a = Agent(
        agent_id="agent_001",
        session_id="session_A"
    )

    # ========================================
    # 建立 Session B
    # ========================================

    agent_b = Agent(
        agent_id="agent_001",
        session_id="session_B"
    )

    show_agent_state(agent_a, "Session A Initial")
    show_agent_state(agent_b, "Session B Initial")

    # ========================================
    # Session A：執行未授權操作
    # ========================================

    print("\n\n===== Session A: Unauthorized Database Request =====")

    agent_a.execute_tool("database")

    show_agent_state(agent_a, "Session A After DENY")
    show_agent_state(agent_b, "Session B Unchanged")

    # ========================================
    # Session B：執行合法 Calculator
    # ========================================

    print("\n\n===== Session B: Authorized Calculator Request =====")

    result_b = agent_b.execute_tool(
        "calculator",
        "10 + 20"
    )

    print("\nSession B Calculator Result:")
    print(result_b)

    show_agent_state(agent_a, "Session A Final")
    show_agent_state(agent_b, "Session B Final")

    # ========================================
    # 顯示各 Session 的事件
    # ========================================

    print("\n\n========================================")
    print("        Session A Event Log")
    print("========================================")

    agent_a.logger.show_events()

    print("\n\n========================================")
    print("        Session B Event Log")
    print("========================================")

    agent_b.logger.show_events()


if __name__ == "__main__":
    main()