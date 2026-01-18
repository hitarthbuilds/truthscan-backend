from typing import List


class ExplainabilityService:
    def __init__(self):
        self.flag_explanations = {
            "temporal_improbability": (
                "The claim refers to an event occurring in an unusually short or unrealistic timeframe."
            ),
            "physical_impossibility": (
                "The claim describes a phenomenon that contradicts well-established physical laws."
            ),
            "absolute_claim": (
                "The claim uses absolute language that leaves no room for uncertainty."
            )
        }

    def explain(self, flags: List[str]) -> List[str]:
        explanations = []

        for flag in flags:
            explanation = self.flag_explanations.get(
                flag,
                "This aspect of the claim requires further verification."
            )
            explanations.append(explanation)

        return explanations
