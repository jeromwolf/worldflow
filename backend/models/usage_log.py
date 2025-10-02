"""
Usage Log Model - Track user usage for billing
"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import uuid


class UsageLog(Base):
    """Usage tracking for billing and analytics"""
    
    __tablename__ = "usage_logs"
    
    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL")
    )
    
    # Usage Details
    action = Column(String(50))  # upload, translate, download
    page_count = Column(Integer)
    credits_used = Column(Numeric(10, 2))
    
    # Timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    # Relationships
    user = relationship("User")
    project = relationship("Project", back_populates="usage_logs")
    
    def __repr__(self):
        return f"<UsageLog {self.action} - {self.page_count} pages>"
