from typing import List


class RiskScoringService:
    def __init__(self):
        # Explainable, capped, modality-agnostic weights
        self.flag_weights = {
            # TEXT / CLAIM FLAGS
            "physical_impossibility": 0.4,
            "temporal_improbability": 0.25,
            "absolute_claim": 0.15,

            # IMAGE FLAGS
            "image_edited_software_detected": 0.3,
            "missing_metadata": 0.15
        }

        # Prevent flag stacking from overpowering everything
        self.max_flag_risk = 0.6

    def score(self, linguistic_confidence: float, flags: List[str]):
        """
        Risk is a combination of:
        - Inverse linguistic confidence
        - Weighted plausibility / image signals
        """

        # Base risk rises as confidence drops
        base_risk = 1.0 - linguistic_confidence

        # Accumulate weighted flag risk
        flag_risk = 0.0
        for flag in flags:
            flag_risk += self.flag_weights.get(flag, 0.1)

        # Cap flag contribution so one bad input doesn't max everything
        flag_risk = min(flag_risk, self.max_flag_risk)

        # Final risk
        risk = base_risk + flag_risk
        risk = max(0.0, min(risk, 1.0))

        # Human-readable interpretation
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
