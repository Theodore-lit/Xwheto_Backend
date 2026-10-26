"""Module J — Contenu social (MVP : annonces). Post polymorphe pour évolution V2/V3."""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import CertificationStatus, ContentType, ModerationStatus, PostType
from app.models.mixins import CreatedAtMixin, Money, TimestampMixin, UUIDMixin, fk, pg_enum


class Post(UUIDMixin, TimestampMixin, Base):
    """Post social polymorphe (annonce, story, réel, article)."""

    __tablename__ = "posts"

    author_user_id: Mapped[uuid.UUID] = fk("users.id")
    type: Mapped[PostType] = mapped_column(pg_enum(PostType), default=PostType.ANNONCE, index=True)
    house_id: Mapped[uuid.UUID | None] = fk("houses.id", nullable=True)
    unit_id: Mapped[uuid.UUID | None] = fk("units.id", nullable=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal | None] = mapped_column(Money)
    media_urls: Mapped[list[Any]] = mapped_column(JSONB, default=list)
    status: Mapped[ModerationStatus] = mapped_column(pg_enum(ModerationStatus), default=ModerationStatus.EN_ATTENTE, index=True)

    # Relationships
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", lazy="raise")


class Comment(UUIDMixin, CreatedAtMixin, Base):
    """Commentaire sur un post."""

    __tablename__ = "comments"

    post_id: Mapped[uuid.UUID] = fk("posts.id", ondelete="CASCADE")
    author_user_id: Mapped[uuid.UUID] = fk("users.id")
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[ModerationStatus] = mapped_column(pg_enum(ModerationStatus), default=ModerationStatus.EN_ATTENTE, index=True)

    # Relationships
    post: Mapped[Post] = relationship(back_populates="comments", lazy="raise")


class Reaction(UUIDMixin, CreatedAtMixin, Base):
    """Réaction (like, etc.) sur un post."""

    __tablename__ = "reactions"
    __table_args__ = (UniqueConstraint("post_id", "user_id", "type", name="post_user_type"),)

    post_id: Mapped[uuid.UUID] = fk("posts.id", ondelete="CASCADE")
    user_id: Mapped[uuid.UUID] = fk("users.id")
    type: Mapped[str] = mapped_column(String(20), default="like")


class ModerationLog(UUIDMixin, Base):
    """Décision de modération d'un contenu."""

    __tablename__ = "moderation_logs"

    content_type: Mapped[ContentType] = mapped_column(pg_enum(ContentType))
    content_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    moderator_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)  # NULL = modération automatique future
    decision: Mapped[ModerationStatus] = mapped_column(pg_enum(ModerationStatus))
    reason: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Certification(UUIDMixin, Base):
    """Certification liée à la paire (bailleur, bien) — pas au compte global (US14.12)."""

    __tablename__ = "certifications"
    __table_args__ = (UniqueConstraint("owner_user_id", "house_id", name="owner_house"),)

    owner_user_id: Mapped[uuid.UUID] = fk("users.id")
    house_id: Mapped[uuid.UUID] = fk("houses.id")
    status: Mapped[CertificationStatus] = mapped_column(
        pg_enum(CertificationStatus), default=CertificationStatus.SUGGEREE, index=True
    )
    suggested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    validated_by_admin_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
