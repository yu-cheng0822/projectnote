from identity import AgentIdentity
from trust import TrustEngine


class PolicyEngine:

    def __init__(self, identity, trust):

        self.identity = identity
        self.trust = trust

        # ========================================
        # Recovery Control
        # ========================================

        # 目前 Session 已使用的 Recovery 次數
        self.recovery_count = 0

        # 單一 Session 最大 Recovery 次數
        self.max_recovery = 3

    # ========================================
    # Policy Decision
    # ========================================

    def check(self, tool_name):

        # ========================================
        # 1. Recovery Policy
        # ========================================

        if tool_name == "recovery":

            # Trust 已經很高
            # 不需要繼續 Recovery
            if self.trust.get_score() >= 80:

                return False, "recovery_not_needed"

            # Recovery 次數超過限制
            if self.recovery_count >= self.max_recovery:

                return False, "recovery_limit_exceeded"

            # 允許 Recovery
            self.recovery_count += 1

            return True, "recovery_allowed"

        # ========================================
        # 2. Identity Permission Check
        # ========================================

        if not self.identity.has_permission(tool_name):

            return False, "permission_denied"

        # ========================================
        # 3. Dynamic Trust Check
        # ========================================

        trust_score = self.trust.get_score()

        # ========================================
        # LOW Trust
        # ========================================

        if trust_score < 50:

            return False, "trust_too_low"

        # ========================================
        # MEDIUM Trust
        # ========================================

        if trust_score < 80:

            # MEDIUM Trust 只能使用 calculator
            if tool_name == "calculator":

                return True, "allowed"

            return False, "medium_trust_restricted"

        # ========================================
        # HIGH Trust
        # ========================================

        return True, "allowed"


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator",
            "database"
        ]
    )

    trust = TrustEngine()

    policy = PolicyEngine(
        identity,
        trust
    )

    # ========================================
    # HIGH Trust
    # ========================================

    print("===== HIGH Trust =====")

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Level:",
        trust.get_level()
    )

    allowed, reason = policy.check(
        "calculator"
    )

    print("\nCalculator:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    allowed, reason = policy.check(
        "database"
    )

    print("\nDatabase:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    # ========================================
    # MEDIUM Trust
    # ========================================

    trust.set_score(65)

    print("\n===== MEDIUM Trust =====")

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Level:",
        trust.get_level()
    )

    allowed, reason = policy.check(
        "calculator"
    )

    print("\nCalculator:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    allowed, reason = policy.check(
        "database"
    )

    print("\nDatabase:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    # ========================================
    # LOW Trust
    # ========================================

    trust.set_score(40)

    print("\n===== LOW Trust =====")

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Level:",
        trust.get_level()
    )

    allowed, reason = policy.check(
        "calculator"
    )

    print("\nCalculator:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    allowed, reason = policy.check(
        "database"
    )

    print("\nDatabase:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    # ========================================
    # Unauthorized Tool
    # ========================================

    print("\n===== Unauthorized Tool =====")

    allowed, reason = policy.check(
        "file"
    )

    print(
        "Tool: file"
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
    # Recovery Test
    # ========================================

    print("\n===== Recovery Test =====")

    trust.set_score(40)

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

    # ========================================
    # HIGH Trust Recovery Test
    # ========================================

    trust.set_score(100)

    policy.recovery_count = 0

    allowed, reason = policy.check(
        "recovery"
    )

    print("\n===== HIGH Trust Recovery =====")

    print(
        "Trust:",
        trust.get_score()
    )

    print(
        "Allowed:",
        allowed
    )

    print(
        "Reason:",
        reason
    )