from datetime import datetime
from event import SecurityEvent

class EventLogger:
    def __init__(self):
        self.events = []

    def log(
        self,
        agent_id,
        session_id,
        tool_name,
        action,
        result
    ):
        event = SecurityEvent(
            agent_id=agent_id,
            session_id=session_id,
            tool_name=tool_name,
            action=action,
            result=result
        )

        self.events.append(event)

    def get_events(self):
        return self.events

    def show_events(self):
        print("\n===== Event Log =====")

        for event in self.events:
            print(event)


if __name__ == "__main__":
    logger = EventLogger()

    logger.log(
        agent_id="agent_001",
        session_id="session_001",
        tool_name="calculator",
        action="REQUEST",
        result="ALLOW"
    )

    logger.log(
        agent_id="agent_001",
        session_id="session_001",
        tool_name="file",
        action="REQUEST",
        result="DENY"
    )

    logger.show_events()