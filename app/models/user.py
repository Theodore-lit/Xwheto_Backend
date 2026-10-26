"""Module A — Utilisateurs, rôles contextuels, délégation."""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, DateTime, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import EntityType, OtpPurpose, Platform, RoleStatus, RoleType, UserStatus
from app.models.mixins import CreatedAtMixin, TimestampMixin, UUIDMixin, fk, pg_enum


class User(UUIDMixin, TimestampMixin, Base):
    """Compte unique par personne. AUCUN rôle bailleur/locataire ici : voir EntityRole.

    Les rôles (bailleur, locataire, manager) sont CONTEXTUELS — ils dépendent du rattachement
    à une entité spécifique (Maison ou Unité). Un même user peut être bailleur sur une maison
    et locataire sur une autre.
    """

    __tablename__ = "users"
    __table_args__ = (CheckConstraint("phone IS NOT NULL OR email IS NOT NULL", name="phone_or_email"),)

    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(150))
    photo_url: Mapped[str | None] = mapped_column(String(500))
    preferred_language: Mapped[str] = mapped_column(String(8), default="fr", server_default="fr")
    profile_completed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    phone_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[UserStatus] = mapped_column(pg_enum(UserStatus), default=UserStatus.ACTIF, index=True)

    # Relationships
    entity_roles: Mapped[list["EntityRole"]] = relationship(back_populates="user", lazy="raise")


class OtpCode(UUIDMixin, CreatedAtMixin, Base):
    """Codes OTP (inscription/connexion). On stocke un hash, jamais le code en clair.

    Le code réel est généré côté service, hashé ici, et jamais retourné en clair à l'utilisateur
    (seule confirmation du succès de la génération).
    """

    __tablename__ = "otp_codes"

    identifier: Mapped[str] = mapped_column(String(255), index=True)  # téléphone ou email
    purpose: Mapped[OtpPurpose] = mapped_column(pg_enum(OtpPurpose))
    code_hash: Mapped[str] = mapped_column(String(255))  # Hash du code (ex: SHA256)
    attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EntityRole(UUIDMixin, CreatedAtMixin, Base):
    """Rattachement contextuel user <-> entité (Maison ou Unit) avec un rôle.

    entity_id est polymorphe (pas de FK SQL native) : l'intégrité est garantie par entity_service.
    Cela permet d'ajouter des entités supplémentaires sans migration DB.

    Un user peut avoir plusieurs rôles sur la même entité (rare, mais théoriquement possible).
    """

    __tablename__ = "entity_roles"
    __table_args__ = (
        UniqueConstraint("user_id", "entity_type", "entity_id", "role_type", name="user_entity_role"),
        Index("ix_entity_roles_entity", "entity_type", "entity_id"),
    )

    user_id: Mapped[uuid.UUID] = fk("users.id")
    entity_type: Mapped[EntityType] = mapped_column(pg_enum(EntityType))  # "house" ou "unit"
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))  # UUID de la maison ou unité
    role_type: Mapped[RoleType] = mapped_column(pg_enum(RoleType))  # bailleur, locataire, etc.
    status: Mapped[RoleStatus] = mapped_column(pg_enum(RoleStatus), default=RoleStatus.ACTIF)

    # Relationships
    user: Mapped[User] = relationship(back_populates="entity_roles", lazy="raise")


class Delegation(UUIDMixin, CreatedAtMixin, Base):
    """Un propriétaire délègue un périmètre (maison/unité) à un manager.

    Les actions non-délégables (US16.5) sont bloquées au niveau service, pas ici.
    Le manager ne peut que gérer — jamais modifier ownership ou accès.
    """

    __tablename__ = "delegations"
    __table_args__ = (Index("ix_delegations_scope", "scope_type", "scope_id"),)

    owner_user_id: Mapped[uuid.UUID] = fk("users.id")
    delegate_user_id: Mapped[uuid.UUID] = fk("users.id")
    scope_type: Mapped[EntityType] = mapped_column(pg_enum(EntityType))  # house ou unit
    scope_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    permissions: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)  # Permissions granulaires
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # NULL = active


class SecondaryMember(UUIDMixin, Base):
    """Membre secondaire (enfant, colocataire) : accès limité, n'engage pas le bail.

    Un member secondaire ne signe jamais le bail (c'est le locataire principal).
    Accès limité aux infos du bail et certaines actions (ex: déclarer un incident).
    """

    __tablename__ = "secondary_members"
    __table_args__ = (UniqueConstraint("lease_id", "member_user_id", name="lease_member"),)

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    primary_tenant_user_id: Mapped[uuid.UUID] = fk("users.id")  # Locataire principal (qui signe)
    member_user_id: Mapped[uuid.UUID] = fk("users.id")  # Membre secondaire
    permissions: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DeviceToken(UUIDMixin, CreatedAtMixin, Base):
    """Token de dispositif pour les notifications push (FCM, APNs, etc.)."""

    __tablename__ = "device_tokens"

    user_id: Mapped[uuid.UUID] = fk("users.id", ondelete="CASCADE")
    token: Mapped[str] = mapped_column(String(500), unique=True)
    platform: Mapped[Platform] = mapped_column(pg_enum(Platform))
