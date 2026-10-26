"""Modules L, M, N — Support, audit, rôles admin, synchro hors-ligne, contenu légal."""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import AdminRoleType, LegalDocType, TicketStatus
from app.models.mixins import CreatedAtMixin, TimestampMixin, UUIDMixin, fk, pg_enum


class SupportTicket(UUIDMixin, TimestampMixin, Base):
    """Ticket de support utilisateur."""

    __tablename__ = "support_tickets"

    user_id: Mapped[uuid.UUID] = fk("users.id")
    category: Mapped[str] = mapped_column(String(50))  # Ex: bug, acces, paiement_echec, fraude
    subject: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TicketStatus] = mapped_column(pg_enum(TicketStatus), default=TicketStatus.OUVERT, index=True)
    assigned_admin_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditLog(UUIDMixin, CreatedAtMixin, Base):
    """Append-only : ne jamais UPDATE/DELETE (à renforcer par un trigger ou des droits PG).

    Enregistre toutes les actions admin pour compliance et traçabilité.
    """

    __tablename__ = "audit_logs"

    admin_id: Mapped[uuid.UUID] = fk("users.id")
    action_type: Mapped[str] = mapped_column(String(80), index=True)  # Ex: user_created, lease_signed
    target_type: Mapped[str] = mapped_column(String(50))  # Ex: User, Lease, Payment
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    before_state: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    after_state: Mapped[dict[str, Any] | None] = mapped_column(JSONB)


class AdminRole(UUIDMixin, Base):
    """Attribution d'un rôle admin à un utilisateur."""

    __tablename__ = "admin_roles"

    user_id: Mapped[uuid.UUID] = fk("users.id", unique=True)
    role: Mapped[AdminRoleType] = mapped_column(pg_enum(AdminRoleType))
    permissions: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)


class SyncLog(UUIDMixin, Base):
    """Suivi des synchronisations offline (idempotence)."""

    __tablename__ = "sync_logs"

    user_id: Mapped[uuid.UUID] = fk("users.id")
    entity_type: Mapped[str] = mapped_column(String(50))  # Ex: MeterReading, Payment
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    client_request_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), unique=True)
    client_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    server_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    conflict_resolution: Mapped[str | None] = mapped_column(
        String(30)
    )  # Ex: none, user_arbitrated, server_wins
    synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LegalDocument(UUIDMixin, Base):
    """Documents légaux (CGU, politique de confidentialité, etc.)."""

    __tablename__ = "legal_documents"
    __table_args__ = (UniqueConstraint("type", "version", name="type_version"),)

    type: Mapped[LegalDocType] = mapped_column(pg_enum(LegalDocType), index=True)
    content: Mapped[str] = mapped_column(Text)  # Format recommandé: Markdown
    version: Mapped[int] = mapped_column(Integer)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by_admin_id: Mapped[uuid.UUID] = fk("users.id")


class SiteSetting(UUIDMixin, Base):
    """Paramètres dynamiques du site (clé-valeur JSONB)."""

    __tablename__ = "site_settings"

    key: Mapped[str] = mapped_column(String(100), unique=True)
    value: Mapped[Any] = mapped_column(JSONB)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    updated_by_admin_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)
