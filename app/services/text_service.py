from transformers import pipeline


class TextVerificationService:
    def __init__(self):
        # Lightweight linguistic analysis model (NOT a truth model)
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def verify(self, text: str):
        result = self.classifier(text)[0]

        label = result["label"]
        score = float(result["score"])

        # Interpret results honestly
        if score >= 0.85:
            if label == "POSITIVE":
                verdict = "neutral_claim"
            else:
                verdict = "emotionally_loaded_claim"
        else:
            verdict = "low_confidence_claim"

        return {
            # This is NOT factual truth — it's linguistic confidence
            "authenticity_score": round(score, 3),
            "verdict": verdict,
            "confidence": round(score, 3),
            "details": {
                "model": "distilbert-base-uncased-sst2",
                "signal_type": "linguistic_confidence",
                "raw_label": label
            }
        }
