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

    risk = RiskEngine()

    # ========================================
    # Experiment
    # ========================================

    print("========================================")
    print(" Dynamic Trust Curve Experiment")
    print("========================================")

    print(
        "\nAttack Count | Trust | Level | Calculator"
    )

    print(
        "-------------------------------------------"
    )

    # ========================================
    # 測試 0 ~ 5 次異常行為
    # ========================================

    for attack_count in range(6):

        # 每一組實驗重新建立 Trust
        trust = TrustEngine()

        policy = PolicyEngine(
            identity,
            trust
        )

        logger = EventLogger()

        # ------------------------------------
        # 模擬異常行為
        # ------------------------------------

        for i in range(attack_count):

            tool_name = "database"

            allowed, reason = policy.check(
                tool_name
            )

            logger.log(
                agent_id=identity.agent_id,
                session_id="trust_curve_test",
                tool_name=tool_name,
                action="REQUEST",
                result="DENY"
            )

        # ------------------------------------
        # Dynamic Trust Calculation
        # ------------------------------------

        events = logger.get_events()

        if attack_count > 0:

            risk_penalty = (
                risk.get_penalty("database")
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

        # ------------------------------------
        # 測試 Calculator
        # ------------------------------------

        allowed, reason = policy.check(
            "calculator"
        )

        # ------------------------------------
        # 輸出結果
        # ------------------------------------

        print(
            f"{attack_count:^12} | "
            f"{trust.get_score():^5} | "
            f"{trust.get_level():^6} | "
            f"{'ALLOW' if allowed else 'DENY'}"
        )

    # ========================================
    # Experiment Summary
    # ========================================

    print(
        "\n===== Experiment Summary ====="
    )

    print(
        "This experiment measures the relationship"
    )

    print(
        "between abnormal behavior and Dynamic Trust."
    )


if __name__ == "__main__":
    main()