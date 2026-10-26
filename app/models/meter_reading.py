"""Module D — Relevés d'index et factures (validation croisée)."""
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import MeterType, ReadingStatus
from app.models.mixins import CreatedAtMixin, Money, UUIDMixin, fk, pg_enum


class MeterReading(UUIDMixin, CreatedAtMixin, Base):
    """Relevé d'index (électricité ou eau) avec validation croisée obligatoire.

    Les deux parties (bailleur, locataire) doivent valider l'index avant génération
    de facture. Aucun ne peut valider sa propre saisie.
    """

    __tablename__ = "meter_readings"
    __table_args__ = (
        # Validation croisée : le validateur ne peut pas être l'auteur de la saisie
        CheckConstraint(
            "validated_by_user_id IS NULL OR validated_by_user_id <> submitted_by_user_id",
            name="cross_validation",
        ),
    )

    unit_id: Mapped[uuid.UUID] = fk("units.id")
    lease_id: Mapped[uuid.UUID] = fk("leases.id")  # Statistiques cloisonnées par relation (US3.2)
    type: Mapped[MeterType] = mapped_column(pg_enum(MeterType))  # electricite ou eau
    value: Mapped[Decimal] = mapped_column(Numeric(12, 2))  # Valeur saisie manuelle ou OCR
    photo_url: Mapped[str] = mapped_column(String(500))  # Photo obligatoire (US6.1)
    ocr_value: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))  # Valeur extraite par OCR
    ocr_confidence: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 3)
    )  # Confiance OCR (0.000 - 1.000)
    submitted_by_user_id: Mapped[uuid.UUID] = fk("users.id")
    status: Mapped[ReadingStatus] = mapped_column(pg_enum(ReadingStatus), default=ReadingStatus.EN_ATTENTE, index=True)
    validated_by_user_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Idempotence de la synchro hors-ligne : UUID généré par le mobile
    client_request_id: Mapped[uuid.UUID | None] = mapped_column(unique=True)


class Invoice(UUIDMixin, Base):
    """Facture générée automatiquement après approbation d'un relevé d'index."""

    __tablename__ = "invoices"

    meter_reading_id: Mapped[uuid.UUID] = fk("meter_readings.id", unique=True)  # 1 index approuvé -> 1 facture
    unit_id: Mapped[uuid.UUID] = fk("units.id")
    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    amount: Mapped[Decimal] = mapped_column(Money)  # Montant calculé
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
    pdf_url: Mapped[str | None] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
