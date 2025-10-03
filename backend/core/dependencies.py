"""
FastAPI Dependencies - Reusable authentication and authorization
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
import uuid

from .database import get_db
from .security import decode_token
from .config import settings
from models.user import User, SubscriptionPlan

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    # Development mode: create a mock user if no token provided
    if settings.DEBUG and not token:
        # Check if dev user exists, if not create it
        dev_email = "dev@example.com"
        result = await db.execute(
            select(User).where(User.email == dev_email)
        )
        dev_user = result.scalar_one_or_none()

        if not dev_user:
            # Create dev user
            dev_user = User(
                email=dev_email,
                password_hash="dev-password-hash",
                subscription_plan=SubscriptionPlan.PRO,
                subscription_status="active",
                is_active=True,
                is_verified=True
            )
            db.add(dev_user)
            await db.commit()
            await db.refresh(dev_user)

        return dev_user

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if not token:
        raise credentials_exception

    payload = decode_token(token)

    if not payload:
        raise credentials_exception

    user_id: str = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(User.id == user_uuid)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (must be active and verified)"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current verified user"""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email not verified"
        )

    return current_user


def require_subscription(required_plan: str):
    """Dependency factory for subscription-based access control"""
    async def check_subscription(
        current_user: User = Depends(get_current_verified_user)
    ) -> User:
        plan_hierarchy = {
            "free": 0,
            "basic": 1,
            "pro": 2,
            "enterprise": 3
        }

        user_plan_level = plan_hierarchy.get(current_user.subscription_plan.value, 0)
        required_plan_level = plan_hierarchy.get(required_plan, 0)

        if user_plan_level < required_plan_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This feature requires {required_plan} subscription or higher"
            )

        if current_user.subscription_status != "active":
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Subscription is not active. Please update your payment method."
            )

        return current_user

    return check_subscription
