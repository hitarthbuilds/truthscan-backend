from fastapi import APIRouter, UploadFile, File
from app.schemas.response import VerificationResponse

router = APIRouter(prefix="/verify", tags=["Verification"])

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
    return {
        "input_type": "text",
        "authenticity_score": 0.73,
        "verdict": "likely_real",
        "confidence": 0.71,
        "details": {
            "note": "Stub response – NLP model coming soon"
        }
    }
