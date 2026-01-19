class TextVerificationService:
    def verify(self, text: str):
        flags = []

        if "tomorrow" in text.lower():
            flags.append("temporal_improbability")

        confidence = 0.7
        risk_score = 0.25 if flags else 0.1

        return {
            "confidence": confidence,
            "flags": flags,
            "risk_score": risk_score
        }
