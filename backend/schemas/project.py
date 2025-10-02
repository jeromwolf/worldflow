"""
Project Schemas - Pydantic models for project requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProjectCreate(BaseModel):
    """Project creation schema"""
    source_language: str = Field(default="ko", pattern="^[a-z]{2}$")
    target_language: str = Field(default="en", pattern="^[a-z]{2}$")


class ProjectResponse(BaseModel):
    """Project response schema"""
    id: UUID
    user_id: UUID
    original_filename: str
    original_file_url: Optional[str]
    pdf_translated_url: Optional[str]
    source_language: str
    target_language: str
    page_count: Optional[int]
    status: str
    progress_percent: int
    markdown_original: Optional[str]
    markdown_translated: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    """Project update schema"""
    markdown_translated: Optional[str] = None
    status: Optional[str] = None


class ProjectList(BaseModel):
    """Project list response"""
    projects: list[ProjectResponse]
    total: int
    page: int
    page_size: int
