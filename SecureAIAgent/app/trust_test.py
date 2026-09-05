from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from logger import EventLogger
from risk import RiskEngine
from tool import ToolExecutor


def print_trust(trust):

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Level:",
        trust.get_level()
    )


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
    # 2. 建立 Security Modules
    # ========================================

    trust = TrustEngine()

    risk = RiskEngine()

    policy = PolicyEngine(
        identity,
        trust,
        risk
    )

    logger = EventLogger()

    executor = ToolExecutor()

    session_id = "test_session"

    # ========================================
    # 3. Initial Trust
    # ========================================

    print("===== Dynamic Trust Test =====")

    print("\nInitial:")

    print_trust(trust)

    # ========================================
    # 4. Unauthorized Database Requests
    # ========================================

    for i in range(3):

        print(
            f"\n--- Unauthorized Request {i + 1} ---"
        )

        tool_name = "database"

        # ------------------------------------
        # Policy Check
        # ------------------------------------

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

        # ------------------------------------
        # Risk
        # ------------------------------------

        penalty = risk.get_penalty(
            tool_name
        )

        print(
            "Risk:",
            risk.get_risk(tool_name)
        )

        print(
            "Risk Penalty:",
            penalty
        )

        # ------------------------------------
        # Security Event
        # ------------------------------------

        if not allowed:

            logger.log(
                agent_id=identity.agent_id,
                session_id=session_id,
                tool_name=tool_name,
                action="REQUEST",
                result="DENY"
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
    # 7. Behavioral Penalties
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
    # 8. Database Risk Penalty
    # ========================================

    risk_penalty = (
        risk.get_penalty(
            "database"
        )
    )

    print(
        "Risk Penalty:",
        risk_penalty
    )

    # ========================================
    # 9. Dynamic Trust Calculation
    # ========================================

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
        "Dynamic Trust Score:",
        dynamic_score
    )

    print(
        "Dynamic Trust Level:",
        trust.get_level()
    )

    # ========================================
    # 10. Trust Recovery Test
    # ========================================

    print(
        "\n===== Trust Recovery Test ====="
    )

    print(
        "Before Recovery:"
    )

    print_trust(trust)

    # ----------------------------------------
    # Recovery Requests
    # ----------------------------------------

    for i in range(5):

        tool_name = "recovery"

        print(
            f"\n--- Recovery Request {i + 1} ---"
        )

        # ------------------------------------
        # Policy Check
        # ------------------------------------

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

        # ------------------------------------
        # Recovery Risk
        # ------------------------------------

        print(
            "Risk:",
            risk.get_risk(tool_name)
        )

        # ------------------------------------
        # 如果允許 Recovery
        # ------------------------------------

        if allowed:

            # -------------------------------
            # 記錄 Recovery Event
            # -------------------------------

            logger.log(
                agent_id=identity.agent_id,
                session_id=session_id,
                tool_name=tool_name,
                action="REQUEST",
                result="ALLOW"
            )

            print(
                "Recovery Event: ALLOW"
            )

        else:

            print(
                "Recovery Event: DENY"
            )

    # ========================================
    # 11. Recalculate Dynamic Trust
    # ========================================

    print(
        "\n===== Recalculate Dynamic Trust ====="
    )

    events = logger.get_events()

    # Recovery 行為加入 Behavioral History
    trust.analyze_history(
        events
    )

    # ----------------------------------------
    # Recovery Reward
    # ----------------------------------------

    recovery_reward = (
        trust.calculate_recovery_reward(
            events
        )
    )

    print(
        "Recovery Reward:",
        recovery_reward
    )

    # ----------------------------------------
    # 重新計算 Dynamic Trust
    # ----------------------------------------

    dynamic_score = (
        trust.calculate_dynamic_trust(
            events,
            risk_penalty=0
        )
    )

    trust.set_score(
        dynamic_score
    )

    print(
        "Dynamic Trust After Recovery:",
        trust.get_score()
    )

    print(
        "Dynamic Trust Level:",
        trust.get_level()
    )

    # ========================================
    # Final Tool Execution Test
    # ========================================

    print("\n===== Final Tool Execution Test =====")

    tool_name = "calculator"
    input_data = "123 * 456"

    # ----------------------------------------
    # Policy Check
    # ----------------------------------------

    allowed, reason = policy.check(
        tool_name
    )

    print("Tool:", tool_name)
    print("Allowed:", allowed)
    print("Reason:", reason)

    # ----------------------------------------
    # 如果 Policy ALLOW
    # 才能真正執行 Tool
    # ----------------------------------------

    if allowed:

        print("\nPolicy Decision: ALLOW")

        success, result = executor.execute(
            tool_name,
            input_data
        )

        print("Tool Execution:", success)
        print("Tool Result:", result)

    # ------------------------------------
    # 記錄 Tool Execution Event
    # ------------------------------------

        logger.log(
            agent_id=identity.agent_id,
            session_id=session_id,
            tool_name=tool_name,
            action="EXECUTE",
            result="ALLOW"
        )

    else:

        print("\nPolicy Decision: DENY")

        print(
            "Tool Execution: BLOCKED"
        )

    # ----------------------------------------
    # Current Trust
    # ----------------------------------------

    print(
        "\nCurrent Trust:",
        trust.get_score()
    )

    print(
        "Current Level:",
        trust.get_level()
    )

    # ========================================
    # 13. Final Security Event Log
    # ========================================

    print("\n===== Event Log =====")
    logger.show_events()


# ============================================
# Program Entry
# ============================================

if __name__ == "__main__":

    main()