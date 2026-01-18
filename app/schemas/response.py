from pydantic import BaseModel
from typing import Dict

class VerificationResponse(BaseModel):
    input_type: str
    authenticity_score: float
    verdict: str
    confidence: float
    details: Dict
