from llm import LocalLLM
from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine

#/
class Agent:

    def __init__(
        self,
        agent_id,
        identity,
        trust,
        policy,
        llm=None
    ):

        self.agent_id = agent_id
        self.identity = identity
        self.trust = trust
        self.policy = policy

        if llm is None:
            self.llm = LocalLLM()
        else:
            self.llm = llm

    # ========================================
    # Agent Decision
    # ========================================

    def decide(self, user_input):

        prompt = f"""
You are a secure AI agent.

User request:
{user_input}

Available tools:
- calculator

If the user asks for a mathematical calculation,
respond using exactly this format:

CALCULATE: <expression>

Otherwise, answer normally.
"""

        decision = self.llm.generate(
            prompt
        )

        return decision.strip()

    # ========================================
    # Tool Request
    # ========================================

    def request_tool(
        self,
        tool_name
    ):

        print(
            "\n===== Tool Request ====="
        )

        print(
            "Agent:",
            self.agent_id
        )

        print(
            "Tool:",
            tool_name
        )

        print(
            "Trust:",
            self.trust.get_score()
        )

        print(
            "Trust Level:",
            self.trust.get_level()
        )

        # ------------------------------------
        # Policy Check
        # ------------------------------------

        allowed, reason = (
            self.policy.check(
                tool_name
            )
        )

        print(
            "Policy Decision:",
            "ALLOW"
            if allowed
            else "DENY"
        )

        print(
            "Reason:",
            reason
        )

        return allowed, reason

    # ========================================
    # Agent Run
    # ========================================

    def run(
        self,
        user_input
    ):

        decision = self.decide(
            user_input
        )

        print(
            "\n===== Agent Decision ====="
        )

        print(
            decision
        )

        # ------------------------------------
        # 判斷是否需要 Calculator
        # ------------------------------------

        if decision.startswith(
            "CALCULATE:"
        ):

            allowed, reason = (
                self.request_tool(
                    "calculator"
                )
            )

            return (
                decision,
                allowed,
                reason
            )

        return (
            decision,
            False,
            "no_tool_required"
        )


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    identity = AgentIdentity(
        agent_id="agent_001",
        role="assistant",
        permissions=[
            "calculator"
        ]
    )

    trust = TrustEngine()

    policy = PolicyEngine(
        identity,
        trust
    )

    agent = Agent(
        agent_id="agent_001",
        identity=identity,
        trust=trust,
        policy=policy
    )

    user_input = input(
        "User："
    )

    agent.run(
        user_input
    )