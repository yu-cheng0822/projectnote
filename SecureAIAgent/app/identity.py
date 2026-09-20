class AgentIdentity:
    def __init__(
        self,
        agent_id,
        role,
        permissions=["calculator", "database","recovery"]
    ):
        self.agent_id = agent_id
        self.role = role
        self.permissions = permissions or ["calculator", "database","recovery"]

    def has_permission(self, tool_name):
        return tool_name in self.permissions