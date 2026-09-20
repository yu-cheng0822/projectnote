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

    session_id = "experiment_001"

    # ========================================
    # Experiment Start
    # ========================================

    print("========================================")
    print(" Dynamic Trust Security Experiment")
    print("========================================")

    # ========================================
    # Phase 1
    # Initial State
    # ========================================

    print("\n===== Phase 1: Initial State =====")

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
    # Phase 2
    # Unauthorized Attack
    # ========================================

    print(
        "\n===== Phase 2: Unauthorized Attack ====="
    )

    for i in range(3):

        tool_name = "database"

        print(
            f"\nAttack Request {i + 1}"
        )

        print(
            "Tool:",
            tool_name
        )

        print(
            "Risk:",
            risk.get_risk(tool_name)
        )

        allowed, reason = policy.check(
            tool_name
        )

        print(
            "Policy Decision:",
            "ALLOW" if allowed else "DENY"
        )

        print(
            "Reason:",
            reason
        )

        # ------------------------------------
        # 記錄 Security Event
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
    # Phase 3
    # Dynamic Trust Evaluation
    # ========================================

    print(
        "\n===== Phase 3: Dynamic Trust Evaluation ====="
    )

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
        "Risk Penalty:",
        risk_penalty
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
    # Test Calculator Under Low Trust
    # ========================================

    print(
        "\n===== Phase 4: Tool Access Under Low Trust ====="
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
        "Policy Decision:",
        "ALLOW" if allowed else "DENY"
    )

    print(
        "Reason:",
        reason
    )

    # ========================================
    # Phase 5
    # Trust Recovery
    # ========================================

    print(
        "\n===== Phase 5: Trust Recovery ====="
    )

    for i in range(8):

        trust.recover(5)

        print(
            f"\nNormal Behavior {i + 1}"
        )

        print(
            "Trust:",
            trust.get_score()
        )

        print(
            "Trust Level:",
            trust.get_level()
        )

        # ------------------------------------
        # Trust 到達 MEDIUM
        # ------------------------------------

        if (
            trust.get_score() >= 50
            and trust.get_score() < 55
        ):

            print(
                ">>> Trust reached MEDIUM"
            )

        # ------------------------------------
        # Trust 到達 HIGH
        # ------------------------------------

        if (
            trust.get_score() >= 80
            and trust.get_score() < 85
        ):

            print(
                ">>> Trust reached HIGH"
            )

    # ========================================
    # Phase 6
    # Test Calculator After Recovery
    # ========================================

    print(
        "\n===== Phase 6: Tool Access After Recovery ====="
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
        "Policy Decision:",
        "ALLOW" if allowed else "DENY"
    )

    print(
        "Reason:",
        reason
    )

    # ========================================
    # Phase 7
    # Calculator Execution
    # ========================================

    if allowed:

        print(
            "\n===== Phase 7: Tool Execution ====="
        )

        success, result = executor.execute(
            tool_name,
            "123 * 456"
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
    # Phase 8
    # Final Security State
    # ========================================

    print(
        "\n===== Phase 8: Final Security State ====="
    )

    print(
        "Final Trust:",
        trust.get_score()
    )

    print(
        "Final Trust Level:",
        trust.get_level()
    )

    # ========================================
    # Phase 9
    # Security Event Log
    # ========================================

    print(
        "\n===== Security Event Log ====="
    )

    logger.show_events()


if __name__ == "__main__":
    main()