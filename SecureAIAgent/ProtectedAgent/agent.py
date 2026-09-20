from llm import LocalLLM
from identity import AgentIdentity
from trust import TrustEngine
from policy import PolicyEngine
from tool import ToolExecutor
from logger import EventLogger
from security_gateway import SecurityGateway

class Agent:

    def __init__(
        self,
        agent_id="agent_001",
        identity=None,
        trust=None,
        policy=None,
        llm=None,
        tool_executor=None,
        logger=None,
        session_id="session_001"
    ):

        # ========================================
        # Agent 基本資訊
        # ========================================

        self.agent_id = agent_id
        self.session_id = session_id

        # ========================================
        # 1. Agent Identity
        # ========================================

        if identity is None:
            self.identity = AgentIdentity(
                agent_id=agent_id,
                role="assistant",
                permissions=["calculator"]
            )
        else:
            self.identity = identity

        # ========================================
        # 2. Dynamic Trust
        # ========================================

        if trust is None:
            self.trust = TrustEngine()
        else:
            self.trust = trust

        # ========================================
        # 3. Policy Engine
        # ========================================

        if policy is None:
            self.policy = PolicyEngine(
                self.identity,
                self.trust
            )
        else:
            self.policy = policy

        # ========================================
        # 4. LLM
        # ========================================

        if llm is None:
            self.llm = LocalLLM()
        else:
            self.llm = llm

        # ========================================
        # 5. Tool Executor
        # ========================================

        if tool_executor is None:
            self.tool_executor = ToolExecutor()
        else:
            self.tool_executor = tool_executor

        # ========================================
        # 6. Event Logger
        # ========================================

        if logger is None:
            self.logger = EventLogger()
        else:
            self.logger = logger

        # ========================================
        # 7. Security Gateway
        # ========================================

        self.security_gateway = SecurityGateway(
            identity=self.identity,
            trust=self.trust,
            policy=self.policy,
            tool_executor=self.tool_executor,
            logger=self.logger,
            agent_id=self.agent_id,
            session_id=self.session_id
        )

    # ==================================================
    # Agent Decision
    # ==================================================

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

        decision = self.llm.generate(prompt)

        return decision.strip()



    def extract_expression(self, decision):

        decision = decision.strip()

        prefix = "CALCULATE:"

        position = decision.upper().find(prefix)

        if position == -1:

            return ""

        expression = decision[
            position + len(prefix):
        ]

        expression = expression.strip()

        return expression

    # ==================================================
    # Main Agent Run
    # ==================================================

    def run(self, user_input):

        # ========================================
        # 1. LLM Decision
        # ========================================

        decision = self.decide(user_input)

        print("\n===== Agent Decision =====")

        print(decision)

        # ========================================
        # 2. Calculator Request
        # ========================================

        if decision.upper().startswith("CALCULATE:"):

            expression = self.extract_expression(
                decision
            )

            print(
                "\n[DEBUG] Extracted Expression:"
            )

            print(repr(expression))

            # ------------------------------------
            # Execute Calculator
            # ------------------------------------

            success, result = self.security_gateway.execute_tool(
                "calculator",
                expression
            )

            execution = {
                "success": success,
                "reason": (
                    "executed"
                    if success
                    else result
                ),
                "result": result
            }
            
            # ------------------------------------
            # Security Event Log
            # ------------------------------------

            print(
                "\n===== Security Event Log ====="
            )

            self.logger.show_events()

            return {
                "decision": decision,
                "tool": "calculator",
                "execution": execution
            }

        # ========================================
        # 3. No Tool Required
        # ========================================

        return {
            "decision": decision,
            "tool": None,
            "execution": {
                "success": False,
                "reason": "no_tool_required",
                "result": None
            }
        }


# ==================================================
# Direct Execution
# ==================================================

if __name__ == "__main__":

    agent = Agent()

    user_input = input("User：")

    result = agent.run(user_input)

    print("\n===== Final Result =====")

    print(result)