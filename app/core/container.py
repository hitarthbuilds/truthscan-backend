from typing import Optional
from app.services.text_service import TextVerificationService

# Global service singletons live here
text_service: Optional[TextVerificationService] = None
