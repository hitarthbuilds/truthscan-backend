from typing import Optional
from fastapi import APIRouter, UploadFile, File, Request
from slowapi import Limiter

from app.schemas.response import VerificationResponse
from app.schemas.batch import BatchVerificationResponse
from app.core.ratelimit import limiter

router = APIRouter(prefix="/verify", tags=["Verification"])


@router.post("/text", response_model=VerificationResponse)
@limiter.limit("10/minute")
async def verify_text(request: Request, text: str):
    # 🔥 Pull services from app.state
    text_service = request.app.state.text_service
    plausibility_service = request.app.state.plausibility_service
    explainability_service = request.app.state.explainability_service
    risk_service = request.app.state.risk_service

    linguistic_result = text_service.verify(text)
    plausibility_result = plausibility_service.check(text)
    explanations = explainability_service.explain(plausibility_result["flags"])

    risk = risk_service.score(
        linguistic_confidence=linguistic_result["confidence"],
        flags=plausibility_result["flags"]
    )

    return {
        "input_type": "text",
        "authenticity_score": linguistic_result["authenticity_score"],
        "confidence": linguistic_result["confidence"],
        "verdict": linguistic_result["verdict"],
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "details": {
            **linguistic_result["details"],
            "plausibility_flags": plausibility_result["flags"],
            "plausibility_flag_count": plausibility_result["flag_count"],
            "explanations": explanations
        }
    }


@router.post("/image", response_model=VerificationResponse)
@limiter.limit("5/minute")
async def verify_image(request: Request, file: UploadFile = File(...)):
    image_service = request.app.state.image_service
    risk_service = request.app.state.risk_service

    file_bytes = await file.read()
    image_result = image_service.verify(file_bytes)

    risk = risk_service.score(
        linguistic_confidence=image_result["confidence"],
        flags=image_result["details"]["image_flags"]
    )

    return {
        "input_type": "image",
        **image_result,
        **risk
    }


@router.post("/batch", response_model=BatchVerificationResponse)
@limiter.limit("3/minute")
async def verify_batch(
    request: Request,
    text: Optional[str] = None,
    image: Optional[UploadFile] = File(None)
):
    text_service = request.app.state.text_service
    plausibility_service = request.app.state.plausibility_service
    explainability_service = request.app.state.explainability_service
    risk_service = request.app.state.risk_service
    image_service = request.app.state.image_service

    text_result = None
    image_result = None
    risks = []

    if text:
        linguistic = text_service.verify(text)
        plausibility = plausibility_service.check(text)
        explanations = explainability_service.explain(plausibility["flags"])

        text_risk = risk_service.score(
            linguistic_confidence=linguistic["confidence"],
            flags=plausibility["flags"]
        )

        text_result = {
            **linguistic,
            **text_risk,
            "details": {
                **linguistic["details"],
                "plausibility_flags": plausibility["flags"],
                "explanations": explanations
            }
        }

        risks.append(text_risk["risk_score"])

    if image:
        image_result = image_service.verify(await image.read())
        risks.append(image_result["risk_score"])

    combined_risk = round(sum(risks) / len(risks), 3) if risks else 0.0
    combined_level = "high" if combined_risk >= 0.75 else "medium" if combined_risk >= 0.4 else "low"

    return {
        "text_result": text_result,
        "image_result": image_result,
        "combined_risk_score": combined_risk,
        "combined_risk_level": combined_level
    }
