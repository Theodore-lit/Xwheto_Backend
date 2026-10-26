"""Modules G & H — Annonces, préférences, litiges, IA."""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import Channel, DisputeObjectType, DisputeStatus, Urgency
from app.models.mixins import CreatedAtMixin, TimestampMixin, UUIDMixin, fk, pg_enum


class Announcement(UUIDMixin, CreatedAtMixin, Base):
    """Annonce urgente ou informative dans une maison."""

    __tablename__ = "announcements"

    house_id: Mapped[uuid.UUID] = fk("houses.id")
    author_id: Mapped[uuid.UUID] = fk("users.id")
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    urgency: Mapped[Urgency] = mapped_column(pg_enum(Urgency), default=Urgency.NORMAL, index=True)
    channels: Mapped[list[Any]] = mapped_column(JSONB, default=list)  # Canaux d'envoi (PUSH, SMS, EMAIL)


class AnnouncementRead(UUIDMixin, Base):
    """Suivi des lectures : annonce urgente persistante tant que non lue (US9.3)."""

    __tablename__ = "announcement_reads"
    __table_args__ = (UniqueConstraint("announcement_id", "user_id", name="announcement_user"),)

    announcement_id: Mapped[uuid.UUID] = fk("announcements.id", ondelete="CASCADE")
    user_id: Mapped[uuid.UUID] = fk("users.id")
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class NotificationPreference(UUIDMixin, Base):
    """Préférences de notification par utilisateur et type d'événement."""

    __tablename__ = "notification_preferences"
    __table_args__ = (UniqueConstraint("user_id", "event_type", "channel", name="user_event_channel"),)

    user_id: Mapped[uuid.UUID] = fk("users.id", ondelete="CASCADE")
    event_type: Mapped[str] = mapped_column(String(50))  # Ex: paiement, alerte, cotisation, salubrité
    channel: Mapped[Channel] = mapped_column(pg_enum(Channel))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class Dispute(UUIDMixin, TimestampMixin, Base):
    """Réclamation/Litige. L'admin n'a qu'accès lecture seule (US14.1). Référence polymorphe."""

    __tablename__ = "disputes"
    __table_args__ = (CheckConstraint("opened_by_user_id <> against_user_id", name="distinct_parties"),)

    related_object_type: Mapped[DisputeObjectType] = mapped_column(pg_enum(DisputeObjectType))
    related_object_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    opened_by_user_id: Mapped[uuid.UUID] = fk("users.id")
    against_user_id: Mapped[uuid.UUID] = fk("users.id")
    reason: Mapped[str] = mapped_column(Text)
    evidence_url: Mapped[str] = mapped_column(String(500))  # Preuve obligatoire (US9.4)
    status: Mapped[DisputeStatus] = mapped_column(pg_enum(DisputeStatus), default=DisputeStatus.OUVERTE, index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    messages: Mapped[list["DisputeMessage"]] = relationship(back_populates="dispute", lazy="raise")


class DisputeMessage(UUIDMixin, CreatedAtMixin, Base):
    """Message dans une conversation de litige."""

    __tablename__ = "dispute_messages"

    dispute_id: Mapped[uuid.UUID] = fk("disputes.id", ondelete="CASCADE")
    author_id: Mapped[uuid.UUID] = fk("users.id")
    message: Mapped[str] = mapped_column(Text)
    attachment_url: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    dispute: Mapped[Dispute] = relationship(back_populates="messages", lazy="raise")


class AiRecommendation(UUIDMixin, Base):
    """Recommandation IA NON contraignante (US9.6)."""

    __tablename__ = "ai_recommendations"

    dispute_id: Mapped[uuid.UUID] = fk("disputes.id")
    requested_by_user_id: Mapped[uuid.UUID] = fk("users.id")
    content: Mapped[str] = mapped_column(Text)  # Contenu de la recommandation
    based_on: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)  # Données ayant servi à la génération
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AiConversation(UUIDMixin, CreatedAtMixin, Base):
    """Historique de conversation avec l'assistant IA (Xwétô-Assist)."""

    __tablename__ = "ai_conversations"

    user_id: Mapped[uuid.UUID] = fk("users.id")
    message: Mapped[str] = mapped_column(Text)  # Question utilisateur
    response: Mapped[str] = mapped_column(Text)  # Réponse IA
    context_type: Mapped[str] = mapped_column(String(30))  # Ex: situation, usage_app
