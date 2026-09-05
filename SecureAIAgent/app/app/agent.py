from llm import LocalLLM
from identity import AgentIdentity
from session import Session
from logger import EventLogger
from trust import TrustEngine
from policy import PolicyEngine
from tools.registry import ToolRegistry
from tools.calculator import CalculatorTool

class Agent:
    def __init__(self):
        self.llm = LocalLLM()

        self.identity = AgentIdentity(
            agent_id="agent_001",
            role="assistant",
            permissions=["calculator"]
        )

        self.session = Session(
            self.identity.agent_id
        )

        self.logger = EventLogger()

        self.trust = TrustEngine()

        self.policy = PolicyEngine(
            self.identity,
            self.trust
        ) 

        self.tools = ToolRegistry()

        self.tools.register(
            CalculatorTool()
        )

    def run(self, user_input):
        print("\nSession:")
        print("Session ID:", self.session.session_id)
        print("Active:", self.session.active)
        prompt = f"""

你是一個 AI Agent。

使用者輸入：
{user_input}

你可以使用以下工具：

calculator：
執行基本數學運算。

如果需要計算，請只輸出：

CALCULATE: 數學表達式

例如：

CALCULATE: 123 * 456

如果不需要計算，請直接回答。
"""

        decision = self.llm.generate(prompt)

        print("\nAgent Decision:")
        print(decision)

        if decision.startswith("CALCULATE:"):
            expression = decision.replace(
                "CALCULATE:",
                ""
            ).strip()

            tool_name = "calculator"
            
            self.logger.log(
                agent_id=self.identity.agent_id,
                session_id=self.session.session_id,
                tool_name=tool_name,
                action="REQUEST",
                result="PENDING"
            )

            print("\nSecurity Check:")
            print("Agent:", self.identity.agent_id)
            print("Requested Tool:", tool_name)

            allowed, reason = self.policy.check(
                tool_name
            )

            if not allowed:

                self.logger.log(
                    agent_id=self.identity.agent_id,
                    session_id=self.session.session_id,
                    tool_name=tool_name,
                    action="REQUEST",
                    result="DENY"
                )

                self.trust.update_from_event("DENY")

                print("Permission: DENY")
                print("Reason:", reason)

                self.logger.show_events()

                return "這個操作被安全策略拒絕。"

            print("Permission: ALLOW")

            self.logger.log(
                agent_id=self.identity.agent_id,
                session_id=self.session.session_id,
                tool_name=tool_name,
                action="REQUEST",
                result="ALLOW"
            )

            self.trust.update_from_event("ALLOW")

            print("Trust Score:", self.trust.get_score())
            print("Trust Level:", self.trust.get_level())

            self.logger.show_events()

            tool = self.tools.get(tool_name)

            result = tool.execute(
                expression=expression
            )

            if result is None:
                return "無法執行這個計算。"

            final_prompt = f"""
使用者原本的問題：

{user_input}

Calculator Tool 的結果：

{result}

請使用繁體中文回答使用者。
不要重新計算。
"""

            return self.llm.generate(final_prompt)

        return decision