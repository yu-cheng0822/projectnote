class RiskEngine:

    def __init__(self):

        self.tool_risk = {
            "calculator": "LOW",
            "recovery": "LOW",
            "file": "MEDIUM",
            "database": "HIGH"
        }

    # ========================================
    # Get Tool Risk
    # ========================================

    def get_risk(self, tool_name):

        return self.tool_risk.get(
            tool_name,
            "HIGH"
        )

    # ========================================
    # Get Risk Penalty
    # ========================================

    def get_penalty(self, tool_name):

        risk = self.get_risk(tool_name)

        if risk == "LOW":
            return 10

        if risk == "MEDIUM":
            return 20

        return 30


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    risk = RiskEngine()

    tools = [
        "calculator",
        "recovery",
        "file",
        "database",
        "unknown"
    ]

    print("===== Risk Engine Test =====")

    for tool in tools:

        print(
            f"Tool: {tool}"
        )

        print(
            f"Risk: {risk.get_risk(tool)}"
        )

        print(
            f"Penalty: {risk.get_penalty(tool)}"
        )

        print()