from typing import Optional
from pydantic import BaseModel


class BatchVerificationResponse(BaseModel):
    text_result: Optional[dict]
    image_result: Optional[dict]
    combined_risk_score: float
    combined_risk_level: str
