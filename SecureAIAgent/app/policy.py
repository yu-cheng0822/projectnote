from identity import AgentIdentity
from trust import TrustEngine
from risk import RiskEngine


class PolicyEngine:

    def __init__(
        self,
        identity,
        trust,
        risk
    ):

        self.identity = identity
        self.trust = trust
        self.risk = risk

    def check(self, tool_name):

        # ========================================
        # 1. Identity Permission Check
        # ========================================

        if tool_name == "recovery":

            # Recovery 不需要一般工具權限
            # 但必須符合 Recovery Policy

            if self.trust.get_score() >= 80:

                return False, "recovery_not_needed"

            return True, "recovery_allowed"

        # ========================================
        # 2. 一般 Tool Permission Check
        # ========================================

        if not self.identity.has_permission(tool_name):

            return False, "permission_denied"

        # ========================================
        # 3. Dynamic Trust Check
        # ========================================

        trust_score = self.trust.get_score()

        # LOW Trust
        if trust_score < 50:

            return False, "trust_too_low"

        # ========================================
        # 4. MEDIUM Trust
        # ========================================

        if trust_score < 80:

            # MEDIUM 只能使用低風險工具

            if tool_name == "calculator":

                return True, "allowed"

            return False, "medium_trust_restricted"

        # ========================================
        # 5. HIGH Trust
        # ========================================

        return True, "allowed"


# ============================================
# Policy Engine Test
# ============================================

if __name__ == "__main__":

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator",
            "database",
            "recovery"
        ]
    )

    trust = TrustEngine()

    policy = PolicyEngine(
        identity,
        trust
    )

    # ========================================
    # HIGH Trust Test
    # ========================================

    print("===== HIGH Trust =====")

    print("Trust:", trust.get_score())
    print("Level:", trust.get_level())

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
    # MEDIUM Trust Test
    # ========================================

    trust.set_score(65)

    print("\n===== MEDIUM Trust =====")

    print("Trust:", trust.get_score())
    print("Level:", trust.get_level())

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
    # LOW Trust Test
    # ========================================

    trust.set_score(40)

    print("\n===== LOW Trust =====")

    print("Trust:", trust.get_score())
    print("Level:", trust.get_level())

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

    allowed, reason = policy.check(
        "recovery"
    )

    print("\nRecovery:")
    print("Allowed:", allowed)
    print("Reason:", reason)

    # ========================================
    # Unauthorized Tool Test
    # ========================================

    allowed, reason = policy.check(
        "file"
    )

    print("\n===== Unauthorized Tool =====")

    print("Tool: file")
    print("Allowed:", allowed)
    print("Reason:", reason)

    print("\n===== Recovery Test =====")

    trust.set_score(40)

    allowed, reason = policy.check(
        "recovery"
    )

    print("Trust:", trust.get_score())
    print("Recovery:")
    print("Allowed:", allowed)
    print("Reason:", reason)


    trust.set_score(100)

    allowed, reason = policy.check(
        "recovery"
    )

    print("\nHIGH Trust Recovery:")
    print("Trust:", trust.get_score())
    print("Allowed:", allowed)
    print("Reason:", reason)