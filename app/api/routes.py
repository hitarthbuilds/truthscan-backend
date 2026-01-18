from fastapi import APIRouter, UploadFile, File
from app.schemas.response import VerificationResponse
from app.services.text_service import TextVerificationService
from app.services.plausibility_service import PlausibilityService

router = APIRouter(prefix="/verify", tags=["Verification"])

# Initialize service once (model loads once)
text_service = TextVerificationService()
plausibility_service = PlausibilityService()



@router.post("/image", response_model=VerificationResponse)
async def verify_image(file: UploadFile = File(...)):
    return {
        "input_type": "image",
        "authenticity_score": 0.42,
        "verdict": "suspicious",
        "confidence": 0.65,
        "details": {
            "note": "Stub response – image model coming soon"
        }
    }


@router.post("/text", response_model=VerificationResponse)
async def verify_text(text: str):
    linguistic_result = text_service.verify(text)
    plausibility_result = plausibility_service.check(text)

    return {
        "input_type": "text",
        **linguistic_result,
        "details": {
            **linguistic_result["details"],
            "plausibility_flags": plausibility_result["flags"],
            "plausibility_flag_count": plausibility_result["flag_count"]
        }
    }

