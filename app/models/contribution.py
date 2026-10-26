"""Modules E & F — Cotisations collectives et salubrité."""
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import CheckConstraint, Date, DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ContributionPaymentStatus, ContributionStatus, TurnStatus
from app.models.mixins import CreatedAtMixin, Money, TimestampMixin, UUIDMixin, fk, pg_enum


class Contribution(UUIDMixin, TimestampMixin, Base):
    """Cotisation collective (ex: nettoyage, réparations partagées)."""

    __tablename__ = "contributions"
    __table_args__ = (CheckConstraint("amount_per_unit > 0", name="amount_positive"),)

    house_id: Mapped[uuid.UUID] = fk("houses.id")
    created_by: Mapped[uuid.UUID] = fk("users.id")
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    amount_per_unit: Mapped[Decimal] = mapped_column(Money)  # Montant par unité
    due_date: Mapped[date] = mapped_column(Date)  # Obligatoire (US7.1)
    justificatif_url: Mapped[str | None] = mapped_column(String(500))  # Justificatif optionnel
    status: Mapped[ContributionStatus] = mapped_column(pg_enum(ContributionStatus), default=ContributionStatus.OUVERTE)

    # Relationships
    payments: Mapped[list["ContributionPayment"]] = relationship(back_populates="contribution", lazy="raise")


class ContributionPayment(UUIDMixin, Base):
    """Paiement d'une cotisation par une unité locative."""

    __tablename__ = "contribution_payments"
    __table_args__ = (UniqueConstraint("contribution_id", "unit_id", name="contribution_unit"),)

    contribution_id: Mapped[uuid.UUID] = fk("contributions.id")
    unit_id: Mapped[uuid.UUID] = fk("units.id")
    user_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)  # Qui a payé (peut être NULL)
    amount: Mapped[Decimal] = mapped_column(Money)
    status: Mapped[ContributionPaymentStatus] = mapped_column(
        pg_enum(ContributionPaymentStatus), default=ContributionPaymentStatus.NON_PAYE, index=True
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    payment_method: Mapped[str | None] = mapped_column(String(30))  # Cash, Fedapay, etc.

    # Relationships
    contribution: Mapped[Contribution] = relationship(back_populates="payments", lazy="raise")


class CleaningSchedule(UUIDMixin, CreatedAtMixin, Base):
    """Calendrier de salubrité d'une maison."""

    __tablename__ = "cleaning_schedules"

    house_id: Mapped[uuid.UUID] = fk("houses.id")
    frequency: Mapped[str] = mapped_column(String(30))  # Ex: hebdomadaire, bimensuel
    spaces: Mapped[list[Any]] = mapped_column(JSONB, default=list)  # Espaces à nettoyer


class CleaningTurn(UUIDMixin, Base):
    """Tour de nettoyage individuel."""

    __tablename__ = "cleaning_turns"

    cleaning_schedule_id: Mapped[uuid.UUID] = fk("cleaning_schedules.id", ondelete="CASCADE")
    unit_id: Mapped[uuid.UUID] = fk("units.id")
    scheduled_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[TurnStatus] = mapped_column(pg_enum(TurnStatus), default=TurnStatus.A_FAIRE)
    photo_url: Mapped[str | None] = mapped_column(String(500))
    completed_by_user_id: Mapped[uuid.UUID | None] = fk(
        "users.id", nullable=True
    )  # Attribution nominative (US16.2)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
