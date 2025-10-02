"""
Authentication Schemas - Pydantic models for request/response
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserCreate(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    name: Optional[str] = None
    organization: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema"""
    id: UUID
    email: str
    name: Optional[str]
    organization: Optional[str]
    subscription_plan: str
    subscription_status: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
