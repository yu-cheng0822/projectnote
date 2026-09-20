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
    # Recovery Reward
    # ========================================

    def calculate_recovery_reward(
        self,
        events,
        current_time=None
    ):

        if current_time is None:
            current_time = datetime.now()

        recovery_reward = 0

        for event in events:

            # 只有 ALLOW 行為可以產生 Recovery
            if event.result != "ALLOW":
                continue

            weight = self.calculate_time_weight(
                event.timestamp,
                current_time
            )

            # 每一次正常行為最多提供 5 分
            recovery_reward += (
                5 * weight
            )

        # 單次分析最多恢復 25 分
        recovery_reward = min(
            25,
            recovery_reward
        )

        return recovery_reward

    # ========================================
    # Dynamic Trust Calculation
    # ========================================

    def calculate_dynamic_trust(
        self,
        events,
        risk_penalty=0,
        current_time=None
    ):

        # ------------------------------------
        # 更新 Behavioral History
        # ------------------------------------

        self.analyze_history(events)

        # ------------------------------------
        # Behavioral Penalty
        # ------------------------------------

        behavioral_penalty = (
            self.calculate_behavioral_penalty(
                events,
                current_time
            )
        )

        # ------------------------------------
        # Recovery Reward
        # ------------------------------------

        recovery_reward = (
            self.calculate_recovery_reward(
                events,
                current_time
            )
        )

        # ------------------------------------
        # Dynamic Trust Formula
        # ------------------------------------

        score = (
            self.score
            - risk_penalty
            - behavioral_penalty
            + recovery_reward
        )

        # ------------------------------------
        # 限制 Trust Score 在 0 ~ 100
        # ------------------------------------

        score = max(
            0,
            min(100, score)
        )

        return score

    # ========================================
    # Trust Analysis Report
    # ========================================

    def get_trust_analysis(
        self,
        events,
        risk_penalty=0,
        current_time=None
    ):

        # 更新 Behavioral History
        self.analyze_history(events)

        # Weighted DENY Rate
        weighted_deny_rate = (
            self.get_weighted_deny_rate(
                events,
                current_time
            )
        )

        # Rate Penalty
        rate_penalty = (
            weighted_deny_rate * 20
        )

        # Repeated Violation Penalty
        repeated_penalty = (
            self.get_repeated_violation_penalty()
        )

        # Recovery Reward
        recovery_reward = (
            self.calculate_recovery_reward(
                events,
                current_time
            )
        )

        # Dynamic Trust
        dynamic_score = (
            self.calculate_dynamic_trust(
                events,
                risk_penalty,
                current_time
            )
        )

        # Dynamic Trust Level
        if dynamic_score >= 80:
            dynamic_level = "HIGH"

        elif dynamic_score >= 50:
            dynamic_level = "MEDIUM"

        else:
            dynamic_level = "LOW"

        return {
            "allow_count": self.allow_count,
            "deny_count": self.deny_count,
            "deny_rate": self.get_deny_rate(),
            "weighted_deny_rate": weighted_deny_rate,
            "rate_penalty": rate_penalty,
            "repeated_penalty": repeated_penalty,
            "risk_penalty": risk_penalty,
            "recovery_reward": recovery_reward,
            "dynamic_score": dynamic_score,
            "dynamic_level": dynamic_level
        }


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    from datetime import timedelta
    from event import SecurityEvent

    trust = TrustEngine()

    now = datetime.now()

    # ----------------------------------------
    # 建立測試事件
    # ----------------------------------------

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
            timestamp=now 
        )
    ]

    print("===== Dynamic Trust Engine Test =====")

    # ----------------------------------------
    # Trust Analysis
    # ----------------------------------------

    analysis = trust.get_trust_analysis(
        events,
        risk_penalty=30,
        current_time=now
    )

    # ----------------------------------------
    # Behavioral History
    # ----------------------------------------

    print(
        "ALLOW Count:",
        analysis["allow_count"]
    )

    print(
        "DENY Count:",
        analysis["deny_count"]
    )

    print(
        "DENY Rate:",
        analysis["deny_rate"]
    )

    # ----------------------------------------
    # Weighted DENY Rate
    # ----------------------------------------

    print(
        "Weighted DENY Rate:",
        analysis["weighted_deny_rate"]
    )

    # ----------------------------------------
    # Penalties
    # ----------------------------------------

    print(
        "Rate Penalty:",
        analysis["rate_penalty"]
    )

    print(
        "Repeated Violation Penalty:",
        analysis["repeated_penalty"]
    )

    print(
        "Risk Penalty:",
        analysis["risk_penalty"]
    )

    # ----------------------------------------
    # Recovery
    # ----------------------------------------

    print(
        "Recovery Reward:",
        analysis["recovery_reward"]
    )

    # ----------------------------------------
    # Dynamic Trust
    # ----------------------------------------

    print(
        "Dynamic Trust Score:",
        analysis["dynamic_score"]
    )

    print(
        "Dynamic Trust Level:",
        analysis["dynamic_level"]
    )