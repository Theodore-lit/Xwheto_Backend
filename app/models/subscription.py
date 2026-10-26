"""Module K — Abonnements et feature flags par plan."""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import SubscriptionStatus
from app.models.mixins import Money, UUIDMixin, fk, pg_enum


class SubscriptionPlan(UUIDMixin, Base):
    """Plan d'abonnement (Free, Pro, Enterprise, etc.)."""

    __tablename__ = "subscription_plans"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    price: Mapped[Decimal] = mapped_column(Money, default=0)
    billing_period: Mapped[str] = mapped_column(String(20), default="mensuel")
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PlanFeature(UUIDMixin, Base):
    """Feature flag par plan d'abonnement."""

    __tablename__ = "plan_features"
    __table_args__ = (UniqueConstraint("plan_id", "feature_key", name="plan_feature"),)

    plan_id: Mapped[uuid.UUID] = fk("subscription_plans.id", ondelete="CASCADE")
    feature_key: Mapped[str] = mapped_column(String(80))  # Ex: advanced_analytics, multi_properties
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)


class Subscription(UUIDMixin, Base):
    """Abonnement d'un utilisateur à un plan."""

    __tablename__ = "subscriptions"

    user_id: Mapped[uuid.UUID] = fk("users.id")
    plan_id: Mapped[uuid.UUID] = fk("subscription_plans.id")
    status: Mapped[SubscriptionStatus] = mapped_column(
        pg_enum(SubscriptionStatus), default=SubscriptionStatus.ACTIF, index=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    renewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    pending_plan_id: Mapped[uuid.UUID | None] = fk(
        "subscription_plans.id", nullable=True
    )  # Downgrade différé (US19.2)
