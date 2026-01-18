from pydantic import BaseModel
from typing import Dict, Any, Optional


class VerificationResponse(BaseModel):
    input_type: str
    authenticity_score: float
    verdict: str
    confidence: float

    # NEW — composite risk
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None

    details: Dict[str, Any]
