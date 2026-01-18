from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TextDetails(BaseModel):
    model: str
    signal_type: str
    raw_label: str
    plausibility_flags: List[str] = []
    plausibility_flag_count: int = 0
    explanations: List[str] = []


class ImageDetails(BaseModel):
    exif_present: bool
    exif_keys: List[str] = []
    image_flags: List[str] = []
    image_flag_count: int = 0


class VerificationResponse(BaseModel):
    input_type: str = Field(..., examples=["text", "image"])
    authenticity_score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    verdict: str

    # Risk
    risk_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_level: Optional[str]

    # Details
    details: Dict[str, Any]
