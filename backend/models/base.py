"""
Base Model and Mixins
"""
from sqlalchemy import Column, DateTime
from datetime import datetime

# Import Base from core.database to ensure single source of truth
from core.database import Base


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
