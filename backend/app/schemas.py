from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator('full_name', mode='before')
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    full_name: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse


class IndicatorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category: str
    description: str
    evidence: str | None = None


class AnalysisCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    message_text: str = Field(min_length=1, max_length=2000)
    store_message: bool = False


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    message_text: str
    risk_level: str
    explanation: str
    recommendation: str
    ai_provider: str
    ai_model: str | None
    created_at: datetime
    completed_at: datetime | None
    indicators: list[IndicatorResponse] = []


class FeedbackRequest(BaseModel):
    is_helpful: bool
    comment: str | None = Field(default=None, max_length=1000)


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    analysis_id: str
    is_helpful: bool
    comment: str | None
