from datetime import datetime


class SecurityEvent:
    def __init__(
        self,
        agent_id,
        session_id,
        tool_name,
        action,
        result,
        timestamp=None
    ):
        self.agent_id = agent_id
        self.session_id = session_id
        self.tool_name = tool_name
        self.action = action
        self.result = result

        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

    def __str__(self):
        return (
            f"[{self.timestamp}] "
            f"Agent={self.agent_id} "
            f"Session={self.session_id} "
            f"Tool={self.tool_name} "
            f"Action={self.action} "
            f"Result={self.result}"
        )