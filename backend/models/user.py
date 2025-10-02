"""
User Model
"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid
import enum


class SubscriptionPlan(str, enum.Enum):
    """Subscription plan types"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class User(Base, TimestampMixin):
    """User model for authentication and subscription"""
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    name = Column(String(100))
    organization = Column(String(200))
    major = Column(String(100))
    
    # Subscription
    subscription_plan = Column(
        Enum(SubscriptionPlan),
        default=SubscriptionPlan.FREE,
        nullable=False
    )
    subscription_status = Column(String(20), default="active")
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
    
    # Account Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime)
    
    # Relationships
    projects = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    glossaries = relationship(
        "Glossary",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User {self.email}>"
