from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from logger import EventLogger
from risk import RiskEngine


def main():

    # ========================================
    # 1. Agent Identity
    # ========================================

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator"
        ]
    )

    # ========================================
    # 2. Security Components
    # ========================================

    trust = TrustEngine()

    policy = PolicyEngine(
        identity,
        trust
    )

    logger = EventLogger()

    risk = RiskEngine()

    session_id = "abuse_test"

    # ========================================
    # Phase 1
    # 正常狀態
    # ========================================

    print("========================================")
    print(" Agent Privilege Abuse Test")
    print("========================================")

    print("\n===== Phase 1: Normal Agent =====")

    print(
        "Permission:",
        identity.has_permission("calculator")
    )

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Trust Level:",
        trust.get_level()
    )

    allowed, reason = policy.check(
        "calculator"
    )

    print(
        "Calculator:",
        "ALLOW" if allowed else "DENY"
    )

    print(
        "Reason:",
        reason
    )

    # ========================================
    # Phase 2
    # 模擬異常行為
    # ========================================

    print(
        "\n===== Phase 2: Abnormal Behavior ====="
    )

    for i in range(3):

        tool_name = "database"

        allowed, reason = policy.check(
            tool_name
        )

        logger.log(
            agent_id=identity.agent_id,
            session_id=session_id,
            tool_name=tool_name,
            action="REQUEST",
            result="DENY"
        )

        print(
            f"\nAbnormal Request {i + 1}"
        )

        print(
            "Tool:",
            tool_name
        )

        print(
            "Risk:",
            risk.get_risk(tool_name)
        )

        print(
            "Decision:",
            "ALLOW" if allowed else "DENY"
        )

        print(
            "Reason:",
            reason
        )

    # ========================================
    # Phase 3
    # Dynamic Trust
    # ========================================

    print(
        "\n===== Phase 3: Dynamic Trust ====="
    )

    events = logger.get_events()

    dynamic_score = (
        trust.calculate_dynamic_trust(
            events,
            risk_penalty=30
        )
    )

    trust.set_score(
        dynamic_score
    )

    print(
        "Dynamic Trust:",
        trust.get_score()
    )

    print(
        "Dynamic Trust Level:",
        trust.get_level()
    )

    # ========================================
    # Phase 4
    # 再次使用原本有權限的 Calculator
    # ========================================

    print(
        "\n===== Phase 4: Privilege Abuse Attempt ====="
    )

    print(
        "Calculator Permission:",
        identity.has_permission(
            "calculator"
        )
    )

    print(
        "Current Trust:",
        trust.get_score()
    )

    print(
        "Current Level:",
        trust.get_level()
    )

    allowed, reason = policy.check(
        "calculator"
    )

    print(
        "Policy Decision:",
        "ALLOW" if allowed else "DENY"
    )

    print(
        "Reason:",
        reason
    )

    # ========================================
    # Phase 5
    # 結論
    # ========================================

    print(
        "\n===== Security Result ====="
    )

    if (
        identity.has_permission("calculator")
        and not allowed
    ):

        print(
            "Permission: GRANTED"
        )

        print(
            "Dynamic Trust: LOW"
        )

        print(
            "Final Decision: DENY"
        )

        print(
            ">>> Privilege Abuse Prevented"
        )

    else:

        print(
            ">>> Security Condition Not Met"
        )

    # ========================================
    # Event Log
    # ========================================

    print(
        "\n===== Security Event Log ====="
    )

    logger.show_events()


if __name__ == "__main__":
    main()