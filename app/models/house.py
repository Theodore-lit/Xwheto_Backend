"""Module B — Maisons, unités, règlement intérieur."""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import UnitStatus, UnitType
from app.models.mixins import CreatedAtMixin, Money, TimestampMixin, UUIDMixin, fk, pg_enum


class House(UUIDMixin, TimestampMixin, Base):
    """Représente une propriété complète (maison, immeuble, boutique).

    Une house est possédée par un unique user (owner_user_id). Le bailleur y gère
    plusieurs unités (chambres, boutiques, etc.) avec leurs propres contrats.
    """

    __tablename__ = "houses"

    owner_user_id: Mapped[uuid.UUID] = fk("users.id")
    name: Mapped[str] = mapped_column(String(150))
    address: Mapped[str] = mapped_column(String(300))
    city: Mapped[str | None] = mapped_column(String(100), index=True)
    photo_url: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    units: Mapped[list["Unit"]] = relationship(back_populates="house", lazy="raise")


class Unit(UUIDMixin, TimestampMixin, Base):
    """Chambre / Boutique / Espace libre avec ses propres conditions financières.

    Les montants ici (rent_amount, deposit_amount, etc.) sont les VALEURS PAR DÉFAUT
    proposées par le bailleur. Les valeurs contractuelles RÉELLES sont copiées dans
    le modèle Lease à la création du bail (snapshot) et ne changent jamais après signature.

    Cela garantit qu'augmenter le loyer d'une unité ne change pas les bails existants.
    """

    __tablename__ = "units"

    house_id: Mapped[uuid.UUID] = fk("houses.id")
    type: Mapped[UnitType] = mapped_column(pg_enum(UnitType))
    label: Mapped[str] = mapped_column(String(100))
    status: Mapped[UnitStatus] = mapped_column(pg_enum(UnitStatus), default=UnitStatus.LIBRE, index=True)
    rent_amount: Mapped[Decimal] = mapped_column(Money)
    deposit_amount: Mapped[Decimal] = mapped_column(Money, default=0)
    advance_amount: Mapped[Decimal] = mapped_column(Money, default=0)
    extra_fees: Mapped[Decimal] = mapped_column(Money, default=0)
    notice_period_days: Mapped[int] = mapped_column(Integer, default=30)

    # Relationships
    house: Mapped[House] = relationship(back_populates="units", lazy="raise")


class HouseRule(UUIDMixin, Base):
    """Règlement intérieur d'une maison (versions multiples possible).

    Chaque version du règlement est horodatée. Un user doit accepter la dernière
    version avant de louer dans la maison.
    """

    __tablename__ = "house_rules"
    __table_args__ = (UniqueConstraint("house_id", "version", name="house_version"),)

    house_id: Mapped[uuid.UUID] = fk("houses.id")
    content: Mapped[str] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer, default=1)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class HouseRuleAcceptance(UUIDMixin, Base):
    """Acceptation d'un règlement intérieur par un user."""

    __tablename__ = "house_rule_acceptances"
    __table_args__ = (UniqueConstraint("house_rule_id", "user_id", name="rule_user"),)

    house_rule_id: Mapped[uuid.UUID] = fk("house_rules.id", ondelete="CASCADE")
    user_id: Mapped[uuid.UUID] = fk("users.id")
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
