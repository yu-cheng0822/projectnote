import uuid
from datetime import datetime


class Session:
    def __init__(self, agent_id):
        self.session_id = str(uuid.uuid4())
        self.agent_id = agent_id
        self.created_at = datetime.now()
        self.active = True

    def end(self):
        self.active = False


if __name__ == "__main__":
    session = Session("agent_001")

    print("Agent ID:", session.agent_id)
    print("Session ID:", session.session_id)
    print("Created At:", session.created_at)
    print("Active:", session.active)

    session.end()

    print("Active after end:", session.active)