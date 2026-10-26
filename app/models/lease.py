"""Module C — Bail, invitation, signature, renouvellement, préavis, caution."""
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, DateTime, Index, Integer, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import DeductionStatus, Initiator, InvitationStatus, LeaseStatus, NoticeStatus, RenewalStatus
from app.models.mixins import CreatedAtMixin, Money, TimestampMixin, UUIDMixin, fk, pg_enum


class Lease(UUIDMixin, TimestampMixin, Base):
    """Bail numérique. Les conditions financières sont COPIÉES depuis l'unité à la création (snapshot).

    Modifier le loyer d'une unité ne doit JAMAIS altérer un bail signé.
    Un seul bail ACTIF par unité à la fois (index unique partiel).
    """

    __tablename__ = "leases"
    __table_args__ = (
        # Un seul bail actif par unité (partiel index)
        Index(
            "uq_leases_one_active_per_unit",
            "unit_id",
            unique=True,
            postgresql_where=text("status = 'actif'"),
        ),
        CheckConstraint("end_date IS NULL OR end_date > start_date", name="dates_coherentes"),
    )

    unit_id: Mapped[uuid.UUID] = fk("units.id")
    tenant_user_id: Mapped[uuid.UUID] = fk("users.id")
    previous_lease_id: Mapped[uuid.UUID | None] = fk("leases.id", nullable=True)  # Chaîne de renouvellement
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[LeaseStatus] = mapped_column(pg_enum(LeaseStatus), default=LeaseStatus.EN_ATTENTE_SIGNATURE, index=True)
    # SNAPSHOT des montants au moment de la signature
    rent_amount: Mapped[Decimal] = mapped_column(Money)
    deposit_amount: Mapped[Decimal] = mapped_column(Money, default=0)
    advance_amount: Mapped[Decimal] = mapped_column(Money, default=0)
    extra_fees: Mapped[Decimal] = mapped_column(Money, default=0)
    notice_period_days: Mapped[int] = mapped_column(Integer, default=30)
    pdf_url: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    signatures: Mapped[list["LeaseSignature"]] = relationship(back_populates="lease", lazy="raise")


class LeaseInvitation(UUIDMixin, TimestampMixin, Base):
    """Invitation d'un locataire sur UNE unité (US1.5 / US1.7).

    Permet au bailleur d'inviter par email, téléphone ou user_id.
    Token unique pour accès sécurisé au lien d'invitation.
    """

    __tablename__ = "lease_invitations"
    __table_args__ = (
        CheckConstraint(
            "invitee_user_id IS NOT NULL OR invitee_phone IS NOT NULL OR invitee_email IS NOT NULL",
            name="invitee_defined",
        ),
    )

    unit_id: Mapped[uuid.UUID] = fk("units.id")
    lease_id: Mapped[uuid.UUID | None] = fk("leases.id", nullable=True)  # NULL au début, défini après création du bail
    invited_by_user_id: Mapped[uuid.UUID] = fk("users.id")  # Bailleur
    invitee_user_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)
    invitee_phone: Mapped[str | None] = mapped_column(String(20))
    invitee_email: Mapped[str | None] = mapped_column(String(255))
    token_hash: Mapped[str] = mapped_column(String(255), unique=True)  # Lien d'invitation sécurisé
    status: Mapped[InvitationStatus] = mapped_column(
        pg_enum(InvitationStatus), default=InvitationStatus.ENVOYEE, index=True
    )
    viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_reminder_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LeaseSignature(UUIDMixin, Base):
    """Signature électronique d'un bail par un user (bailleur ou locataire)."""

    __tablename__ = "lease_signatures"

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    user_id: Mapped[uuid.UUID] = fk("users.id")
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    signature_data: Mapped[str] = mapped_column(Text)  # Image base64 ou hash du document signé
    ip_address: Mapped[str | None] = mapped_column(String(64))

    # Relationships
    lease: Mapped[Lease] = relationship(back_populates="signatures", lazy="raise")


class LeaseRenewalRequest(UUIDMixin, Base):
    """Demande de renouvellement d'un bail."""

    __tablename__ = "lease_renewal_requests"

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    requested_by_user_id: Mapped[uuid.UUID] = fk("users.id")
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[RenewalStatus] = mapped_column(pg_enum(RenewalStatus), default=RenewalStatus.EN_ATTENTE, index=True)
    new_end_date: Mapped[date | None] = mapped_column(Date)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DepartureNotice(UUIDMixin, CreatedAtMixin, Base):
    """Préavis légal de départ (initiée par locataire ou bailleur)."""

    __tablename__ = "departure_notices"

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    initiated_by: Mapped[Initiator] = mapped_column(pg_enum(Initiator))
    reason: Mapped[str | None] = mapped_column(Text)
    notice_date: Mapped[date] = mapped_column(Date)  # Date d'émission du préavis
    effective_date: Mapped[date] = mapped_column(
        Date
    )  # >= notice_date + notice_period_days (vérifié en service)
    status: Mapped[NoticeStatus] = mapped_column(pg_enum(NoticeStatus), default=NoticeStatus.EN_COURS)


class DepositDeduction(UUIDMixin, TimestampMixin, Base):
    """Déduction sur caution avec justificatif obligatoire (US11.5)."""

    __tablename__ = "deposit_deductions"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    created_by_user_id: Mapped[uuid.UUID] = fk("users.id")
    label: Mapped[str] = mapped_column(String(200))  # Motif de la déduction
    amount: Mapped[Decimal] = mapped_column(Money)
    evidence_url: Mapped[str] = mapped_column(String(500))  # Justificatif obligatoire
    status: Mapped[DeductionStatus] = mapped_column(pg_enum(DeductionStatus), default=DeductionStatus.PROPOSEE)
