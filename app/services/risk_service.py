from typing import List


class RiskScoringService:
    def __init__(self):
        # Weights are opinionated but explainable
        self.flag_weights = {
            "physical_impossibility": 0.4,
            "temporal_improbability": 0.25,
            "absolute_claim": 0.15
        }

    def score(self, linguistic_confidence: float, flags: List[str]):
        # Base risk increases when confidence is low
        risk = 1.0 - linguistic_confidence

        # Add weighted risk for plausibility flags
        for flag in flags:
            risk += self.flag_weights.get(flag, 0.1)

        # Clamp between 0 and 1
        risk = max(0.0, min(risk, 1.0))

        # Human-readable level
        if risk >= 0.75:
            level = "high"
        elif risk >= 0.4:
            level = "medium"
        else:
            level = "low"

        return {
            "risk_score": round(risk, 3),
            "risk_level": level
        }
