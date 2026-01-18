from fastapi import APIRouter, UploadFile, File
from app.schemas.response import VerificationResponse
from app.services.text_service import TextVerificationService

router = APIRouter(prefix="/verify", tags=["Verification"])

# Initialize service once (model loads once)
text_service = TextVerificationService()


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
    result = text_service.verify(text)

    return {
        "input_type": "text",
        **result
    }
