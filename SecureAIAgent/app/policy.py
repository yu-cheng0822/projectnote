from identity import AgentIdentity
from trust import TrustEngine


class PolicyEngine:

    def __init__(self, identity, trust):
        self.identity = identity
        self.trust = trust

    # ========================================
    # Tool Permission Policy
    # ========================================

    def check(self, tool_name):

        # ------------------------------------
        # 1. Identity Permission
        # ------------------------------------

        if not self.identity.has_permission(tool_name):
            return False, "permission_denied"

        # ------------------------------------
        # 2. 取得 Dynamic Trust Level
        # ------------------------------------

        trust_level = self.trust.get_level()

        # ------------------------------------
        # 3. LOW Trust
        # ------------------------------------

        if trust_level == "LOW":

            if tool_name == "recovery":
                return True, "recovery_allowed"

            return False, "trust_too_low"

        # ------------------------------------
        # 4. MEDIUM Trust
        # ------------------------------------

        if trust_level == "MEDIUM":

            if tool_name == "calculator":
                return True, "allowed"

            if tool_name == "recovery":
                return True, "recovery_allowed"

            return False, "medium_trust_restricted"
        
        # ------------------------------------
        # 5. HIGH Trust
        # ------------------------------------

        if trust_level == "HIGH":
            return True, "allowed"

        # ------------------------------------
        # 6. 未知 Trust Level
        # ------------------------------------

        return False, "unknown_trust_level"


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