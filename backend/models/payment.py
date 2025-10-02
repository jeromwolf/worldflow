"""
Payment Model - Stripe payment records
"""
from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import uuid


class Payment(Base):
    """Payment transaction records"""
    
    __tablename__ = "payments"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Stripe Info
    stripe_payment_id = Column(String(255), unique=True)
    amount = Column(Numeric(10, 2))
    currency = Column(String(3), default="KRW")
    status = Column(String(20))  # succeeded, failed, refunded
    subscription_plan = Column(String(20))
    
    # Timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    # Relationship
    user = relationship("User")
    
    def __repr__(self):
        return f"<Payment {self.stripe_payment_id} - {self.amount} {self.currency}>"
