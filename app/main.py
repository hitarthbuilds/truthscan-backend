from fastapi import FastAPI
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


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs ONCE at startup.
    Creates long-lived services and attaches them to app.state.
    """

    # 🔥 Initialize services exactly once
    app.state.text_service = TextVerificationService()
    app.state.plausibility_service = PlausibilityService()
    app.state.explainability_service = ExplainabilityService()
    app.state.risk_service = RiskScoringService()
    app.state.image_service = ImageVerificationService()

    yield

    # (Optional cleanup later if needed)


app = FastAPI(
    title="TruthScan API",
    lifespan=lifespan
)

# Middleware
app.add_middleware(RequestContextMiddleware)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routes
app.include_router(router)
