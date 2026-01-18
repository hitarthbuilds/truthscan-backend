from fastapi import APIRouter
from app.api.verification import router as verification_router

router = APIRouter()
router.include_router(verification_router)

@router.get("/health", tags=["System"])
def health():
    return {
        "status": "ok",
        "service": "truthscan-backend"
    }
