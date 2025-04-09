"""
Authentication models for iiko.services API
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TokenRequest(BaseModel):
    """Request model for authentication"""
    api_login: str = Field(..., description="API login")


class TokenResponse(BaseModel):
    """Response model for authentication"""
    token: str = Field(..., description="Access token")
    correlation_id: Optional[str] = Field(None, alias="correlationId", description="Correlation ID")
    expire_seconds: Optional[int] = Field(None, description="Token expiration time in seconds")

    # Additional fields for internal use
    created_at: Optional[datetime] = Field(None, description="Token creation time")

    def is_expired(self) -> bool:
        """Check if token is expired"""
        if not self.created_at:
            return True

        # Default expiration time is 1 hour (3600 seconds) if not provided
        expiration_seconds = self.expire_seconds or 3600
        expiration_time = self.created_at.timestamp() + expiration_seconds
        current_time = datetime.now().timestamp()

        return current_time >= expiration_time
