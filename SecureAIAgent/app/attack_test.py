from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from logger import EventLogger
from risk import RiskEngine
from tool import ToolExecutor


def main():

    # ========================================
    # 1. 建立 Agent Identity
    # ========================================

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator"
        ]
    )

    # ========================================
    # 2. 建立 Security Components
    # ========================================

    trust = TrustEngine()

    policy = PolicyEngine(
        identity,
        trust
    )

    logger = EventLogger()

    risk = RiskEngine()

    executor = ToolExecutor()

    session_id = "attack_test"

    # ========================================
    # 3. Initial State
    # ========================================

    print("========================================")
    print("        AI Agent Security Test")
    print("========================================")

    print("\n===== Initial State =====")

    print(
        "Agent:",
        identity.agent_id
    )

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Trust Level:",
        trust.get_level()
    )

    # ========================================
    # 4. Attack Scenario
    # Repeated Unauthorized Database Request
    # ========================================

    print(
        "\n===== Attack Scenario ====="
    )

    print(
        "Attacker behavior:"
    )

    print(
        "Repeated unauthorized database requests"
    )

    for i in range(3):

        print(
            f"\n--- Attack Request {i + 1} ---"
        )

        tool_name = "database"

        # ------------------------------------
        # Risk
        # ------------------------------------

        risk_level = risk.get_risk(
            tool_name
        )

        risk_penalty = risk.get_penalty(
            tool_name
        )

        print(
            "Tool:",
            tool_name
        )

        print(
            "Risk:",
            risk_level
        )

        print(
            "Risk Penalty:",
            risk_penalty
        )

        # ------------------------------------
        # Policy Decision
        # ------------------------------------

        allowed, reason = policy.check(
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
        # Event Log
        # ------------------------------------

        result = (
            "ALLOW"
            if allowed
            else "DENY"
        )

        logger.log(
            agent_id=identity.agent_id,
            session_id=session_id,
            tool_name=tool_name,
            action="REQUEST",
            result=result
        )

    # ========================================
    # 5. Calculate Dynamic Trust
    # ========================================

    print(
        "\n===== Dynamic Trust Evaluation ====="
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
    # 6. Recovery Attack Test
    # ========================================

    print(
        "\n===== Recovery Abuse Test ====="
    )

    policy.recovery_count = 0

    for i in range(5):

        allowed, reason = policy.check(
            "recovery"
        )

        print(
            f"\nRecovery Request {i + 1}:"
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
            "Recovery Count:",
            policy.recovery_count
        )

        # ------------------------------------
        # 如果 Recovery 被允許
        # ------------------------------------

        if allowed:

            success, result = (
                executor.execute(
                    "recovery"
                )
            )

            print(
                "Execution:",
                success
            )

            print(
                "Result:",
                result
            )

    # ========================================
    # 7. Normal Behavior
    # ========================================

    print(
        "\n===== Normal Behavior Test ====="
    )

    # 重設 Recovery 次數
    policy.recovery_count = 0

    # 正常 Calculator Request

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

    # ========================================
    # 8. 如果允許，執行 Calculator
    # ========================================

    if allowed:

        success, result = (
            executor.execute(
                tool_name,
                "123 * 456"
            )
        )

        print(
            "Execution:",
            success
        )

        print(
            "Result:",
            result
        )

        logger.log(
            agent_id=identity.agent_id,
            session_id=session_id,
            tool_name=tool_name,
            action="EXECUTE",
            result="ALLOW"
        )

    # ========================================
    # 9. Final State
    # ========================================

    # ========================================
    # Trust Recovery Test
    # ========================================

    print("\n===== Trust Recovery Test =====")

    print("Before Recovery:")
    print("Trust:", trust.get_score())
    print("Level:", trust.get_level())

    # 模擬正常行為
    for i in range(10):

        trust.recover(5)

        print(
            f"\nNormal Behavior {i + 1}:"
        )

        print(
            "Trust:",
            trust.get_score()
        )

        print(
            "Level:",
            trust.get_level()
        )

    print(
        "\n===== Final Security State ====="
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
        "Recovery Count:",
        policy.recovery_count
    )

    # ========================================
    # 10. Event Log
    # ========================================

    print(
        "\n===== Security Event Log ====="
    )

    logger.show_events()


if __name__ == "__main__":
    main()