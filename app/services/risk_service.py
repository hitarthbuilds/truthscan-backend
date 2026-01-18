from typing import List


class RiskScoringService:
    def __init__(self):
        self.flag_weights = {
            # TEXT FLAGS
            "physical_impossibility": 0.4,
            "temporal_improbability": 0.25,
            "absolute_claim": 0.15,

            # IMAGE FLAGS
            "missing_metadata": 0.15,
            "compression_artifacts": 0.2,
            "screenshot_like": 0.15,
        }

        self.max_flag_risk = 0.6

    def score(self, linguistic_confidence: float, flags: List[str]):
        base_risk = 1.0 - linguistic_confidence

        flag_risk = 0.0
        for flag in flags:
            flag_risk += self.flag_weights.get(flag, 0.1)

        flag_risk = min(flag_risk, self.max_flag_risk)

        risk = base_risk + flag_risk
        risk = max(0.0, min(risk, 1.0))

        if risk >= 0.75:
            level = "high"
        elif risk >= 0.4:
            level = "medium"
        else:
            level = "low"

        return {
            "risk_score": round(risk, 3),
            "risk_level": level,
        }
