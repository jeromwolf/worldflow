"""
Project Model - Translation Projects
"""
from sqlalchemy import Column, String, Integer, BigInteger, Text, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid
import enum


class ProjectStatus(str, enum.Enum):
    """Project status enum"""
    UPLOADING = "uploading"
    PARSING = "parsing"
    TRANSLATING = "translating"
    COMPLETED = "completed"
    FAILED = "failed"


class Project(Base, TimestampMixin):
    """Translation project model"""
    
    __tablename__ = "projects"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # File Information
    original_filename = Column(String(500), nullable=False)
    original_file_url = Column(String(1000))  # S3 URL
    pdf_translated_url = Column(String(1000))  # S3 URL
    
    # Language
    source_language = Column(String(10), default="ko", nullable=False)
    target_language = Column(String(10), default="en", nullable=False)
    
    # Document Info
    page_count = Column(Integer)
    file_size_bytes = Column(BigInteger)
    
    # Status
    status = Column(
        Enum(ProjectStatus),
        default=ProjectStatus.UPLOADING,
        nullable=False,
        index=True
    )
    progress_percent = Column(Integer, default=0)
    error_message = Column(Text)
    
    # Content (Markdown)
    markdown_original = Column(Text)
    markdown_translated = Column(Text)
    
    # Soft Delete
    deleted_at = Column(DateTime, index=True)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    usage_logs = relationship(
        "UsageLog",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    images = relationship(
        "ProjectImage",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectImage.page_number, ProjectImage.image_index"
    )
    
    def __repr__(self):
        return f"<Project {self.original_filename} ({self.status})>"
