"""Modèles SQLAlchemy pour Xwétô.

Tous les modèles sont importés ici pour que Alembic puisse les découvrir automatiquement.
"""

from app.models.admin import (  # noqa: F401
    AdminRole,
    AuditLog,
    LegalDocument,
    SiteSetting,
    SupportTicket,
    SyncLog,
)
from app.models.communication import (  # noqa: F401
    AiConversation,
    AiRecommendation,
    Announcement,
    AnnouncementRead,
    Dispute,
    DisputeMessage,
    NotificationPreference,
)
from app.models.contribution import (  # noqa: F401
    CleaningSchedule,
    CleaningTurn,
    Contribution,
    ContributionPayment,
)
from app.models.enums import *  # noqa: F401, F403
from app.models.house import House, HouseRule, HouseRuleAcceptance, Unit  # noqa: F401
from app.models.lease import (  # noqa: F401
    DepartureNotice,
    DepositDeduction,
    Lease,
    LeaseInvitation,
    LeaseRenewalRequest,
    LeaseSignature,
)
from app.models.meter_reading import Invoice, MeterReading  # noqa: F401
from app.models.mixins import *  # noqa: F401, F403
from app.models.payment import (  # noqa: F401
    Payment,
    PaymentReminder,
    Wallet,
    WalletTransaction,
    WithdrawalRequest,
)
from app.models.post import Comment, Certification, ModerationLog, Post, Reaction  # noqa: F401
from app.models.subscription import PlanFeature, Subscription, SubscriptionPlan  # noqa: F401
from app.models.user import (  # noqa: F401
    Delegation,
    DeviceToken,
    EntityRole,
    OtpCode,
    SecondaryMember,
    User,
)

__all__ = [
    # Enums & Mixins
    "UUIDMixin",
    "CreatedAtMixin",
    "TimestampMixin",
    "Money",
    # User & Auth
    "User",
    "OtpCode",
    "EntityRole",
    "Delegation",
    "SecondaryMember",
    "DeviceToken",
    # House
    "House",
    "Unit",
    "HouseRule",
    "HouseRuleAcceptance",
    # Lease
    "Lease",
    "LeaseInvitation",
    "LeaseSignature",
    "LeaseRenewalRequest",
    "DepartureNotice",
    "DepositDeduction",
    # Meter & Invoice
    "MeterReading",
    "Invoice",
    # Payment
    "Payment",
    "Wallet",
    "WalletTransaction",
    "WithdrawalRequest",
    "PaymentReminder",
    # Contribution
    "Contribution",
    "ContributionPayment",
    "CleaningSchedule",
    "CleaningTurn",
    # Communication
    "Announcement",
    "AnnouncementRead",
    "NotificationPreference",
    "Dispute",
    "DisputeMessage",
    "AiRecommendation",
    "AiConversation",
    # Post & Social
    "Post",
    "Comment",
    "Reaction",
    "ModerationLog",
    "Certification",
    # Subscription
    "SubscriptionPlan",
    "PlanFeature",
    "Subscription",
    # Admin
    "SupportTicket",
    "AuditLog",
    "AdminRole",
    "SyncLog",
    "LegalDocument",
    "SiteSetting",
]
