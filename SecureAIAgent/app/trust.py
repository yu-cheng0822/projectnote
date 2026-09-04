from datetime import datetime
import math


class TrustEngine:

    def __init__(self, initial_score=100):
        self.score = initial_score

        self.deny_count = 0
        self.allow_count = 0

    # ========================================
    # Trust Score Control
    # ========================================

    def increase(self, amount):
        self.score = min(
            100,
            self.score + amount
        )

    def decrease(self, amount):
        self.score = max(
            0,
            self.score - amount
        )

    def recover(self, amount):
        self.score = min(
            100,
            self.score + amount
        )

    def set_score(self, score):
        self.score = max(
            0,
            min(100, score)
        )

    # ========================================
    # Event Update
    # ========================================

    def update_from_event(
        self,
        result,
        penalty=20
    ):

        if result == "ALLOW":

            self.allow_count += 1

            self.increase(1)

        elif result == "DENY":

            self.deny_count += 1

            self.decrease(penalty)

    # ========================================
    # Behavioral History
    # ========================================

    def analyze_history(self, events):

        deny_count = 0
        allow_count = 0

        for event in events:

            if event.result == "DENY":
                deny_count += 1

            elif event.result == "ALLOW":
                allow_count += 1

        self.deny_count = deny_count
        self.allow_count = allow_count

    # ========================================
    # Basic Information
    # ========================================

    def get_score(self):
        return self.score

    def get_level(self):

        if self.score >= 80:
            return "HIGH"

        elif self.score >= 50:
            return "MEDIUM"

        else:
            return "LOW"

    def get_allow_count(self):
        return self.allow_count

    def get_deny_count(self):
        return self.deny_count

    # ========================================
    # DENY Rate
    # ========================================

    def get_deny_rate(self):

        total = (
            self.allow_count +
            self.deny_count
        )

        if total == 0:
            return 0

        return (
            self.deny_count /
            total
        )

    # ========================================
    # Time Decay
    # ========================================

    def calculate_time_weight(
        self,
        event_time,
        current_time=None
    ):

        if current_time is None:
            current_time = datetime.now()

        age_seconds = (
            current_time -
            event_time
        ).total_seconds()

        age_hours = (
            age_seconds / 3600
        )

        decay = math.exp(
            -0.1 * age_hours
        )

        return decay

    # ========================================
    # Weighted DENY Rate
    # ========================================

    def get_weighted_deny_rate(
        self,
        events,
        current_time=None
    ):

        weighted_deny = 0
        weighted_total = 0

        for event in events:

            weight = self.calculate_time_weight(
                event.timestamp,
                current_time
            )

            weighted_total += weight

            if event.result == "DENY":
                weighted_deny += weight

        if weighted_total == 0:
            return 0

        return (
            weighted_deny /
            weighted_total
        )

    # ========================================
    # Repeated Violation
    # ========================================

    def get_repeated_violation_penalty(self):

        if self.deny_count <= 1:
            return 0

        return (
            self.deny_count - 1
        ) * 5

    # ========================================
    # Behavioral Penalty
    # ========================================

    def calculate_behavioral_penalty(
        self,
        events,
        current_time=None
    ):

        # Time-weighted DENY behavior
        weighted_deny_rate = (
            self.get_weighted_deny_rate(
                events,
                current_time
            )
        )

        # DENY rate penalty
        rate_penalty = (
            weighted_deny_rate * 20
        )

        # Repeated violation penalty
        repeated_penalty = (
            self.get_repeated_violation_penalty()
        )

        return (
            rate_penalty +
            repeated_penalty
        )

    # ========================================
    # Dynamic Trust Calculation
    # ========================================

    def calculate_dynamic_trust(
        self,
        events,
        risk_penalty=0,
        current_time=None
    ):

        # 更新 Behavioral History
        self.analyze_history(events)

        # 計算 Behavioral Penalty
        behavioral_penalty = (
            self.calculate_behavioral_penalty(
                events,
                current_time
            )
        )

        # Dynamic Trust Formula
        score = (
            100
            - risk_penalty
            - behavioral_penalty
        )

        # 限制在 0 ~ 100
        score = max(
            0,
            min(100, score)
        )

        return score


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    from datetime import timedelta
    from event import SecurityEvent

    trust = TrustEngine()

    now = datetime.now()

    # 建立測試事件
    events = [

        SecurityEvent(
            agent_id="agent_001",
            session_id="session_001",
            tool_name="database",
            action="REQUEST",
            result="DENY",
            timestamp=now
        ),

        SecurityEvent(
            agent_id="agent_001",
            session_id="session_001",
            tool_name="database",
            action="REQUEST",
            result="DENY",
            timestamp=now
        ),

        SecurityEvent(
            agent_id="agent_001",
            session_id="session_001",
            tool_name="database",
            action="REQUEST",
            result="DENY",
            timestamp=now
        ),

        SecurityEvent(
            agent_id="agent_001",
            session_id="session_001",
            tool_name="calculator",
            action="REQUEST",
            result="ALLOW",
            timestamp=now - timedelta(days=7)
        )
    ]

    print("===== Dynamic Trust Engine Test =====")

    # ----------------------------------------
    # Behavioral History
    # ----------------------------------------

    trust.analyze_history(events)

    print(
        "ALLOW Count:",
        trust.get_allow_count()
    )

    print(
        "DENY Count:",
        trust.get_deny_count()
    )

    print(
        "DENY Rate:",
        trust.get_deny_rate()
    )

    # ----------------------------------------
    # Time Decay
    # ----------------------------------------

    weighted_deny_rate = (
        trust.get_weighted_deny_rate(
            events,
            now
        )
    )

    print(
        "Weighted DENY Rate:",
        weighted_deny_rate
    )

    # ----------------------------------------
    # Penalties
    # ----------------------------------------

    rate_penalty = (
        weighted_deny_rate * 20
    )

    repeated_penalty = (
        trust.get_repeated_violation_penalty()
    )

    print(
        "Rate Penalty:",
        rate_penalty
    )

    print(
        "Repeated Violation Penalty:",
        repeated_penalty
    )

    # ----------------------------------------
    # Dynamic Trust
    # ----------------------------------------

    risk_penalty = 30

    dynamic_score = (
        trust.calculate_dynamic_trust(
            events,
            risk_penalty=risk_penalty,
            current_time=now
        )
    )

    print(
        "Risk Penalty:",
        risk_penalty
    )

    print(
        "Dynamic Trust Score:",
        dynamic_score
    )

    # ----------------------------------------
    # Dynamic Trust Level
    # ----------------------------------------

    trust.set_score(dynamic_score)

    print(
        "Dynamic Trust Level:",
        trust.get_level()
    )