"""Module I — Paiements, portefeuille bailleur, relances."""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import Channel, PaymentMethod, PaymentStatus, TxStatus, WalletTxType, WithdrawalStatus
from app.models.mixins import CreatedAtMixin, Money, TimestampMixin, UUIDMixin, fk, pg_enum


class Payment(UUIDMixin, TimestampMixin, Base):
    """Paiement du loyer (Fedapay ou cash enregistré manuellement)."""

    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount > 0", name="amount_positive"),
        CheckConstraint(
            "payment_method <> 'fedapay' OR fedapay_transaction_id IS NOT NULL OR status = 'en_attente'",
            name="fedapay_ref",
        ),
    )

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    payer_user_id: Mapped[uuid.UUID] = fk("users.id")
    recorded_by_user_id: Mapped[uuid.UUID | None] = fk(
        "users.id", nullable=True
    )  # Bailleur/manager (paiement cash)
    amount: Mapped[Decimal] = mapped_column(Money)
    payment_method: Mapped[PaymentMethod] = mapped_column(pg_enum(PaymentMethod))
    status: Mapped[PaymentStatus] = mapped_column(pg_enum(PaymentStatus), default=PaymentStatus.EN_ATTENTE, index=True)
    fedapay_transaction_id: Mapped[str | None] = mapped_column(
        String(100), unique=True
    )  # Idempotence webhook
    receipt_pdf_url: Mapped[str | None] = mapped_column(String(500))
    proof_photo_url: Mapped[str | None] = mapped_column(String(500))  # Photo de preuve (cash)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Wallet(UUIDMixin, Base):
    """Portefeuille bailleur (solde des paiements reçus)."""

    __tablename__ = "wallets"
    __table_args__ = (CheckConstraint("balance >= 0", name="balance_non_negative"),)

    owner_user_id: Mapped[uuid.UUID] = fk("users.id", unique=True)
    balance: Mapped[Decimal] = mapped_column(Money, default=0, server_default="0")
    currency: Mapped[str] = mapped_column(String(3), default="XOF", server_default="XOF")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    transactions: Mapped[list["WalletTransaction"]] = relationship(back_populates="wallet", lazy="raise")


class WalletTransaction(UUIDMixin, CreatedAtMixin, Base):
    """Grand livre du portefeuille : solde = somme des transactions réussies."""

    __tablename__ = "wallet_transactions"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    wallet_id: Mapped[uuid.UUID] = fk("wallets.id")
    type: Mapped[WalletTxType] = mapped_column(pg_enum(WalletTxType))  # CREDIT, DEBIT, RETRAIT
    amount: Mapped[Decimal] = mapped_column(Money)
    related_payment_id: Mapped[uuid.UUID | None] = fk("payments.id", nullable=True, unique=True)
    status: Mapped[TxStatus] = mapped_column(pg_enum(TxStatus), default=TxStatus.EN_ATTENTE)

    # Relationships
    wallet: Mapped[Wallet] = relationship(back_populates="transactions", lazy="raise")


class WithdrawalRequest(UUIDMixin, Base):
    """Demande de retrait du portefeuille vers le compte bancaire du bailleur."""

    __tablename__ = "withdrawal_requests"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    wallet_id: Mapped[uuid.UUID] = fk("wallets.id")
    requested_by_user_id: Mapped[uuid.UUID] = fk("users.id")  # Toujours le propriétaire (US16.5)
    amount: Mapped[Decimal] = mapped_column(Money)
    destination: Mapped[str] = mapped_column(String(50))  # Numéro Mobile Money
    status: Mapped[WithdrawalStatus] = mapped_column(
        pg_enum(WithdrawalStatus), default=WithdrawalStatus.EN_ATTENTE, index=True
    )
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PaymentReminder(UUIDMixin, Base):
    """Historique des relances de paiement envoyées."""

    __tablename__ = "payment_reminders"
    __table_args__ = (UniqueConstraint("lease_id", "period_label", "level", name="lease_period_level"),)

    lease_id: Mapped[uuid.UUID] = fk("leases.id")
    period_label: Mapped[str] = mapped_column(String(7))  # Ex: "2026-10"
    level: Mapped[int] = mapped_column(Integer)  # 1/2/3 (1ère, 2e, 3e relance)
    channel: Mapped[Channel] = mapped_column(pg_enum(Channel))  # PUSH, SMS, EMAIL
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
