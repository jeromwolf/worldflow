"""
Glossary Model - User's terminology dictionary
"""
from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid


class Glossary(Base, TimestampMixin):
    """User glossary for consistent terminology translation"""
    
    __tablename__ = "glossaries"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Terms
    source_term = Column(String(200), nullable=False)
    target_term = Column(String(200), nullable=False)
    category = Column(String(50))  # tech, medical, education, etc.
    
    # Relationship
    user = relationship("User", back_populates="glossaries")
    
    # Indexes
    __table_args__ = (
        Index('idx_glossary_source_term', 'source_term'),
        Index('idx_glossary_user_category', 'user_id', 'category'),
    )
    
    def __repr__(self):
        return f"<Glossary {self.source_term} -> {self.target_term}>"
