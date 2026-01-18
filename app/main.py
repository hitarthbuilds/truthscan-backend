from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.core.logging import setup_logging
from app.core.ratelimit import limiter
from app.middleware.request_context import RequestContextMiddleware

# Services
from app.services.text_service import TextVerificationService
from app.services.plausibility_service import PlausibilityService
from app.services.explainability_service import ExplainabilityService
from app.services.risk_service import RiskScoringService
from app.services.image_service import ImageVerificationService


# ---------------------------------------------------------
# Logging (do this FIRST)
# ---------------------------------------------------------
setup_logging()


# ---------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs ONCE at startup.
    Initialize long-lived services here.
    """

    # Initialize services once and store on app.state
    app.state.text_service = TextVerificationService()
    app.state.plausibility_service = PlausibilityService()
    app.state.explainability_service = ExplainabilityService()
    app.state.risk_service = RiskScoringService()
    app.state.image_service = ImageVerificationService()

    yield

    # Optional: cleanup resources on shutdown


# ---------------------------------------------------------
# App
# ---------------------------------------------------------
app = FastAPI(
    title="TruthScan API",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS (REQUIRED for frontend)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------
app.add_middleware(RequestContextMiddleware)


# ---------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
app.include_router(router)
