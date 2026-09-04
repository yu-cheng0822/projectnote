from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from logger import EventLogger
from risk import RiskEngine


def main():

    # ========================================
    # 1. 建立 Agent Identity
    # ========================================

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator",
            "recovery"
        ]
    )

    # ========================================
    # 2. 建立安全模組
    # ========================================

    trust = TrustEngine()
    policy = PolicyEngine(identity, trust)
    logger = EventLogger()
    risk = RiskEngine()

    session_id = "test_session"

    # ========================================
    # 3. 初始 Trust
    # ========================================

    print("===== Dynamic Trust Test =====")

    print("\nInitial:")
    print("Trust:", trust.get_score())
    print("Level:", trust.get_level())

    # ========================================
    # 4. 模擬 3 次未授權 database Request
    # ========================================

    for i in range(3):

        print(
            f"\n--- Unauthorized Request {i + 1} ---"
        )

        tool_name = "database"

        allowed, reason = policy.check(
            tool_name
        )

        print("Tool:", tool_name)
        print("Allowed:", allowed)
        print("Reason:", reason)

        if not allowed:

            logger.log(
                agent_id=identity.agent_id,
                session_id=session_id,
                tool_name=tool_name,
                action="REQUEST",
                result="DENY"
            )

            penalty = risk.get_penalty(
                tool_name
            )

            print(
                "Risk Penalty:",
                penalty
            )

    # ========================================
    # 5. Behavioral History
    # ========================================

    print(
        "\n===== Behavioral History ====="
    )

    events = logger.get_events()

    trust.analyze_history(events)

    print(
        "ALLOW Count:",
        trust.get_allow_count()
    )

    print(
        "DENY Count:",
        trust.get_deny_count()
    )

    print(
        "DENY Rate:",
        trust.get_deny_rate()
    )

    # ========================================
    # 6. Weighted DENY Rate
    # ========================================

    weighted_deny_rate = (
        trust.get_weighted_deny_rate(
            events
        )
    )

    print(
        "Weighted DENY Rate:",
        weighted_deny_rate
    )

    # ========================================
    # 7. Behavioral Penalty
    # ========================================

    rate_penalty = (
        weighted_deny_rate * 20
    )

    repeated_penalty = (
        trust.get_repeated_violation_penalty()
    )

    print(
        "Rate Penalty:",
        rate_penalty
    )

    print(
        "Repeated Violation Penalty:",
        repeated_penalty
    )

    # ========================================
    # 8. Dynamic Trust Calculation
    # ========================================

    risk_penalty = risk.get_penalty(
        "database"
    )

    dynamic_score = (
        trust.calculate_dynamic_trust(
            events,
            risk_penalty=risk_penalty
        )
    )

    trust.set_score(
        dynamic_score
    )

    print(
        "Risk Penalty:",
        risk_penalty
    )

    print(
        "Dynamic Trust Score:",
        dynamic_score
    )

    print(
        "Dynamic Trust Level:",
        trust.get_level()
    )

    # ========================================
    # 9. Trust Recovery Test
    # ========================================

    print(
        "\n===== Trust Recovery Test ====="
    )

    print("Before Recovery:")
    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Level:",
        trust.get_level()
    )

    # ========================================
    # 10. 使用 Recovery Tool
    # ========================================

    for i in range(5):

        tool_name = "recovery"

        allowed, reason = policy.check(
            tool_name
        )

        print(
            f"\n--- Recovery Request {i + 1} ---"
        )

        print(
            "Tool:",
            tool_name
        )

        print(
            "Allowed:",
            allowed
        )

        print(
            "Reason:",
            reason
        )

        # ------------------------------------
        # Recovery 被 Policy 允許
        # ------------------------------------

        if allowed:

            # 記錄 ALLOW Event
            logger.log(
                agent_id=identity.agent_id,
                session_id=session_id,
                tool_name=tool_name,
                action="REQUEST",
                result="ALLOW"
            )

            # Trust Recovery
            trust.recover(5)

            print(
                "Trust Recovery: +5"
            )

        else:

            print(
                "Trust Recovery: 0"
            )

        print(
            "Current Trust:",
            trust.get_score()
        )

        print(
            "Current Level:",
            trust.get_level()
        )

    # ========================================
    # 11. Recovery 後 Trust
    # ========================================

    dynamic_score = (
        trust.get_score()
    )

    dynamic_level = (
        trust.get_level()
    )

    print(
        "\n===== Current Trust After Recovery ====="
    )

    print(
        "Dynamic Trust:",
        dynamic_score
    )

    print(
        "Dynamic Level:",
        dynamic_level
    )

    # ========================================
    # 12. Final Test
    # ========================================

    print(
        "\n===== Final Test ====="
    )

    tool_name = "calculator"

    allowed, reason = policy.check(
        tool_name
    )

    print(
        "Tool:",
        tool_name
    )

    print(
        "Allowed:",
        allowed
    )

    print(
        "Reason:",
        reason
    )

    print(
        "Current Trust:",
        trust.get_score()
    )

    print(
        "Current Level:",
        trust.get_level()
    )

    # ========================================
    # 13. Event Log
    # ========================================

    print(
        "\n===== Event Log ====="
    )

    logger.show_events()


if __name__ == "__main__":
    main()