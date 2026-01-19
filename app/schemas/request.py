from typing import Optional
from pydantic import BaseModel, Field


class TextVerificationRequest(BaseModel):
    """
    Request schema for text verification.
    """

    text: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Text content to verify"
    )


class BatchVerificationRequest(BaseModel):
    """
    Request schema for batch verification.
    """

    text: Optional[str] = Field(
        None,
        min_length=10,
        max_length=2000,
        description="Optional text content to verify"
    )

    image: Optional[bool] = Field(
        False,
        description="Whether an image is included in the batch request"
    )


from pydantic import BaseModel

class TextVerificationRequest(BaseModel):
    text: str
