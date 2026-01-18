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
            ),
            "missing_metadata": (
                "The image lacks standard metadata, which can indicate resaving or manipulation."
            ),
            "screenshot_like": (
                "The image dimensions resemble common screen capture ratios."
            ),
            "compression_artifacts": (
                "The image format or compression suggests possible re-encoding or reposting."
            ),
        }

    def explain(self, flags: List[str]) -> List[str]:
        explanations = []

        for flag in flags:
            explanations.append(
                self.flag_explanations.get(
                    flag,
                    "This aspect of the content requires further verification."
                )
            )

        return explanations
