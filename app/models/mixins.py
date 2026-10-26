"""Briques communes : PK UUID, timestamps, helpers FK / enum / monnaie."""
import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

Money = Numeric(14, 2)  # XOF n'a pas de décimales, mais on garde 2 pour l'évolutivité


class UUIDMixin:
    """Mixin ajoutant une clé primaire UUID auto-générée."""

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class CreatedAtMixin:
    """Mixin ajoutant un timestamp de création (server-side)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TimestampMixin(CreatedAtMixin):
    """Mixin ajoutant timestamps de création et modification."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


def fk(
    target: str, *, nullable: bool = False, ondelete: str = "RESTRICT", unique: bool = False
) -> Any:
    """Crée une clé étrangère UUID indexée.

    Args:
        target: Cible FK au format 'table.column' (ex: 'users.id')
        nullable: Si False (défaut), NOT NULL. RESTRICT par défaut = pas de suppression en cascade
        ondelete: Action au DELETE de la cible (RESTRICT, CASCADE, SET NULL)
        unique: Si True, applique UNIQUE au lieu d'INDEX

    Returns:
        mapped_column avec ForeignKey, index/unique, et UUID(as_uuid=True)

    Example:
        owner_user_id: Mapped[uuid.UUID] = fk("users.id")
        previous_lease_id: Mapped[uuid.UUID | None] = fk("leases.id", nullable=True)
    """
    return mapped_column(
        UUID(as_uuid=True),
        ForeignKey(target, ondelete=ondelete),
        nullable=nullable,
        index=not unique,
        unique=unique,
    )


def pg_enum(enum_cls: type[enum.Enum]) -> SAEnum:
    """Crée un Enum PostgreSQL (VARCHAR, pas ENUM natif PG).

    Avantage : les migrations Alembic ne cassent pas les changements d'enum.
    Les valeurs sont stockées en tant que strings comparables.

    Args:
        enum_cls: Classe Enum Python (ex: UserStatus)

    Returns:
        SAEnum configuré pour PostgreSQL avec validation strict

    Example:
        status: Mapped[UserStatus] = mapped_column(pg_enum(UserStatus))
    """
    return SAEnum(
        enum_cls,
        native_enum=False,  # VARCHAR, pas ENUM PG natif
        length=40,
        values_callable=lambda e: [m.value for m in e],
        validate_strings=True,
        create_constraint=False,
    )
