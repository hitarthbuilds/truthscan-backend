from fastapi import APIRouter, Request, UploadFile, File, Body
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel

router = APIRouter(prefix="/verify", tags=["Verification"])
limiter = Limiter(key_func=get_remote_address)


# ---------- MODELS ----------

class TextRequest(BaseModel):
    text: str


class VerificationResponse(BaseModel):
    input_type: str
    verdict: str
    confidence: float
    risk_score: float
    risk_level: str
    flags: list[str]


# ---------- TEXT ----------

@router.post("/text", response_model=VerificationResponse)
@limiter.limit("10/minute")
async def verify_text(
    request: Request,
    payload: TextRequest = Body(...)
):
    text_service = request.app.state.text_service
    risk_service = request.app.state.risk_service

    text_result = text_service.verify(payload.text)

    # 🔒 SAFE EXTRACTION
    confidence = text_result.get("confidence", 0.0)

    flags = (
        text_result.get("flags")
        or text_result.get("reasons")
        or text_result.get("details", {}).get("flags")
        or []
    )

    risk = risk_service.score(
        linguistic_confidence=confidence,
        flags=flags
    )

    verdict = (
        "MISLEADING"
        if risk["risk_level"] in ["medium", "high"]
        else "UNLIKELY BUT LOW RISK"
    )

    return {
        "input_type": "text",
        "verdict": verdict,
        "confidence": confidence,
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "flags": flags,
    }


# ---------- IMAGE ----------

@router.post("/image", response_model=VerificationResponse)
@limiter.limit("5/minute")
async def verify_image(
    request: Request,
    image: UploadFile = File(...)
):
    image_service = request.app.state.image_service
    risk_service = request.app.state.risk_service

    file_bytes = await image.read()
    image_result = image_service.verify(file_bytes)

    confidence = image_result.get("confidence", 0.0)

    flags = (
        image_result.get("image_flags")
        or image_result.get("flags")
        or image_result.get("details", {}).get("image_flags")
        or []
    )

    risk = risk_service.score(
        linguistic_confidence=confidence,
        flags=flags
    )

    verdict = (
        "POTENTIALLY MANIPULATED"
        if risk["risk_level"] in ["medium", "high"]
        else "LIKELY AUTHENTIC"
    )

    return {
        "input_type": "image",
        "verdict": verdict,
        "confidence": confidence,
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "flags": flags,
    }
