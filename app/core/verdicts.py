from typing import Literal


Verdict = Literal[
    "likely_authentic",
    "review_required",
    "likely_false",
    "low_confidence_claim"
]


def compute_verdict(
    authenticity_score: float,
    risk_score: float
) -> Verdict:
    """
    Centralized verdict logic.
    Change thresholds here, not across services.
    """

    # High risk overrides everything
    if risk_score >= 0.75:
        return "likely_false"

    # Medium risk or shaky authenticity
    if risk_score >= 0.4 or authenticity_score < 0.7:
        return "review_required"

    # Weird but not dangerous
    if authenticity_score < 0.6:
        return "low_confidence_claim"

    return "likely_authentic"
