from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from logger import EventLogger
from risk import RiskEngine


def main():

    # ========================================
    # 建立 Agent
    # ========================================

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator"
        ]
    )

    # ========================================
    # 建立 Security Components
    # ========================================

    trust = TrustEngine()

    policy = PolicyEngine(
        identity,
        trust
    )

    logger = EventLogger()

    risk = RiskEngine()

    # ========================================
    # Experiment Header
    # ========================================

    print("========================================")
    print(" Permission vs Dynamic Trust")
    print("========================================")

    # ========================================
    # Experiment 1
    # Traditional Permission
    # ========================================

    print("\n===== Experiment 1: Permission Only =====")

    print(
        "Agent Permission:",
        identity.permissions
    )

    # 模擬 Agent 擁有 calculator 權限

    if identity.has_permission("calculator"):

        print(
            "Calculator:",
            "ALLOW"
        )

        print(
            "Reason:",
            "permission_granted"
        )

    else:

        print(
            "Calculator:",
            "DENY"
        )

        print(
            "Reason:",
            "permission_denied"
        )

    # ========================================
    # Experiment 2
    # Dynamic Trust
    # ========================================

    print(
        "\n===== Experiment 2: Dynamic Trust ====="
    )

    print(
        "Initial Trust:",
        trust.get_score()
    )

    print(
        "Initial Level:",
        trust.get_level()
    )

    # ========================================
    # 模擬三次未授權 database Request
    # ========================================

    for i in range(3):

        tool_name = "database"

        allowed, reason = policy.check(
            tool_name
        )

        print(
            f"\nUnauthorized Request {i + 1}"
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
            "Policy:",
            "ALLOW" if allowed else "DENY"
        )

        print(
            "Reason:",
            reason
        )

        logger.log(
            agent_id=identity.agent_id,
            session_id="comparison_test",
            tool_name=tool_name,
            action="REQUEST",
            result=(
                "ALLOW"
                if allowed
                else "DENY"
            )
        )

    # ========================================
    # Dynamic Trust Calculation
    # ========================================

    events = logger.get_events()

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
        "\n===== Dynamic Trust Result ====="
    )

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Level:",
        trust.get_level()
    )

    # ========================================
    # 再次測試 calculator
    # ========================================

    print(
        "\n===== Calculator After Attack ====="
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
        "Permission:",
        identity.has_permission(
            tool_name
        )
    )

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Trust Level:",
        trust.get_level()
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
    # Comparison Summary
    # ========================================

    print(
        "\n===== Comparison Summary ====="
    )

    print(
        "Traditional Permission:"
    )

    print(
        "Calculator -> ALLOW"
    )

    print(
        "\nDynamic Trust:"
    )

    print(
        "Calculator ->",
        "ALLOW" if allowed else "DENY"
    )

    print(
        "\nFinal Trust:",
        trust.get_score()
    )

    print(
        "Final Trust Level:",
        trust.get_level()
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