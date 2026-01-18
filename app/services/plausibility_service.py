import re
from typing import List, Dict


class PlausibilityService:
    def __init__(self):
        # Simple keyword-based heuristics (fast + explainable)
        self.temporal_triggers = [
            r"\btomorrow\b",
            r"\binstantly\b",
            r"\bwithin (minutes|hours)\b",
            r"\bby tonight\b"
        ]

        self.physical_impossibilities = [
            r"\bsun will explode\b",
            r"\bgravity (stopped|turned off)\b",
            r"\bperpetual motion\b",
            r"\bviolates the laws of physics\b"
        ]

        self.absolute_claims = [
            r"\balways\b",
            r"\bnever\b",
            r"\bguaranteed\b",
            r"\b100%\b"
        ]

    def check(self, text: str) -> Dict:
        flags: List[str] = []

        lowered = text.lower()

        for pattern in self.temporal_triggers:
            if re.search(pattern, lowered):
                flags.append("temporal_improbability")

        for pattern in self.physical_impossibilities:
            if re.search(pattern, lowered):
                flags.append("physical_impossibility")

        for pattern in self.absolute_claims:
            if re.search(pattern, lowered):
                flags.append("absolute_claim")

        return {
            "flags": flags,
            "flag_count": len(flags)
        }
