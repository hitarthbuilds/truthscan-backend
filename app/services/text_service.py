from transformers import pipeline
from typing import Optional


class TextVerificationService:
    def __init__(self):
        self._classifier: Optional[callable] = None

    def _load_model(self):
        if self._classifier is None:
            self._classifier = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )

    def verify(self, text: str):
        self._load_model()  # loads once, reused forever

        result = self._classifier(text)[0]

        label = result["label"]
        score = float(result["score"])

        if score >= 0.85:
            verdict = (
                "neutral_claim"
                if label == "POSITIVE"
                else "emotionally_loaded_claim"
            )
        else:
            verdict = "low_confidence_claim"

        return {
            "authenticity_score": round(score, 3),
            "verdict": verdict,
            "confidence": round(score, 3),
            "details": {
                "model": "distilbert-base-uncased-sst2",
                "signal_type": "linguistic_confidence",
                "raw_label": label
            }
        }
