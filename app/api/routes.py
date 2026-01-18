from fastapi import APIRouter, UploadFile, File
from app.schemas.response import VerificationResponse
from app.services.text_service import TextVerificationService
from app.services.plausibility_service import PlausibilityService
from app.services.explainability_service import ExplainabilityService
from app.services.risk_service import RiskScoringService
from app.services.image_service import ImageVerificationService



router = APIRouter(prefix="/verify", tags=["Verification"])

# Initialize service once (model loads once)
text_service = TextVerificationService()
plausibility_service = PlausibilityService()
explainability_service = ExplainabilityService()
risk_service = RiskScoringService()

image_service = ImageVerificationService()



@router.post("/image", response_model=VerificationResponse)
async def verify_image(file: UploadFile = File(...)):
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



@router.post("/text", response_model=VerificationResponse)
async def verify_text(text: str):
    linguistic_result = text_service.verify(text)
    plausibility_result = plausibility_service.check(text)
    explanations = explainability_service.explain(
        plausibility_result["flags"]
    )

    risk = risk_service.score(
        linguistic_confidence=linguistic_result["confidence"],
        flags=plausibility_result["flags"]
    )

    return {
        "input_type": "text",
        **linguistic_result,
        **risk,
        "details": {
            **linguistic_result["details"],
            "plausibility_flags": plausibility_result["flags"],
            "plausibility_flag_count": plausibility_result["flag_count"],
            "explanations": explanations
        }
    }
