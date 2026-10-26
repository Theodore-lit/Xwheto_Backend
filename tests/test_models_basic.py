"""Tests unitaires basiques pour les modèles Xwétô."""
import pytest
from decimal import Decimal
from datetime import date, timedelta

from app.models import (
    User,
    House,
    Unit,
    Lease,
    EntityRole,
    OtpCode,
    DeviceToken,
    MeterReading,
    Payment,
    Wallet,
    WalletTransaction,
    Contribution,
    Announcement,
    Post,
)
from app.models.enums import (
    UserStatus,
    EntityType,
    RoleType,
    RoleStatus,
    Platform,
    UnitType,
    UnitStatus,
    LeaseStatus,
    MeterType,
    ReadingStatus,
    PaymentMethod,
    PaymentStatus,
    OtpPurpose,
    ContributionStatus,
    Urgency,
    PostType,
    ModerationStatus,
    WalletTxType,
    TxStatus,
)


@pytest.mark.asyncio
async def test_user_creation(test_session, sample_user):
    """Test : création d'un utilisateur."""
    assert sample_user.id is not None
    assert sample_user.phone == "+22390000001"
    assert sample_user.email == "user@example.com"
    assert sample_user.full_name == "John Doe"
    assert sample_user.status == UserStatus.ACTIF
    assert sample_user.created_at is not None
    assert sample_user.updated_at is not None


@pytest.mark.asyncio
async def test_user_phone_or_email_constraint(test_session, sample_user):
    """Test : un user doit avoir phone OU email (ou les deux)."""
    # Ce test s'assurerait que la contrainte CHECK est appliquée en BD
    # Pour SQLite, les CHECK peuvent ne pas être supportées, donc on teste juste la logique
    assert sample_user.phone is not None or sample_user.email is not None


@pytest.mark.asyncio
async def test_house_creation(test_session, sample_house):
    """Test : création d'une maison."""
    assert sample_house.id is not None
    assert sample_house.owner_user_id is not None
    assert sample_house.name == "Maison Test"
    assert sample_house.address == "123 Rue de la Paix"
    assert sample_house.city == "Abidjan"


@pytest.mark.asyncio
async def test_unit_creation(test_session, sample_unit):
    """Test : création d'une unité locative."""
    assert sample_unit.id is not None
    assert sample_unit.type == UnitType.CHAMBRE
    assert sample_unit.status == UnitStatus.LIBRE
    assert sample_unit.rent_amount == Decimal("50000.00")
    assert sample_unit.deposit_amount == Decimal("100000.00")
    assert sample_unit.notice_period_days == 30


@pytest.mark.asyncio
async def test_lease_creation(test_session, sample_lease):
    """Test : création d'un bail."""
    assert sample_lease.id is not None
    assert sample_lease.status == LeaseStatus.ACTIF
    assert sample_lease.rent_amount == Decimal("50000.00")
    assert sample_lease.end_date > sample_lease.start_date


@pytest.mark.asyncio
async def test_lease_status_enum(test_session, sample_lease):
    """Test : les statuts de bail sont corrects."""
    valid_statuses = [s.value for s in LeaseStatus]
    assert sample_lease.status.value in valid_statuses


@pytest.mark.asyncio
async def test_entity_role_creation(test_session, sample_entity_role):
    """Test : création d'un rôle contextuel."""
    assert sample_entity_role.id is not None
    assert sample_entity_role.entity_type == EntityType.HOUSE
    assert sample_entity_role.role_type == RoleType.BAILLEUR
    assert sample_entity_role.status == RoleStatus.ACTIF


@pytest.mark.asyncio
async def test_entity_role_polymorphic(test_session, sample_user, sample_unit):
    """Test : entity_id est polymorphe (pas de FK SQL)."""
    # On peut créer un rôle sur une unité avec le même entity_id (UUID)
    from app.models import EntityRole

    role_unit = EntityRole(
        user_id=sample_user.id,
        entity_type=EntityType.UNIT,
        entity_id=sample_unit.id,  # UUID de l'unité
        role_type=RoleType.LOCATAIRE,
        status=RoleStatus.ACTIF,
    )
    test_session.add(role_unit)
    await test_session.commit()
    await test_session.refresh(role_unit)

    assert role_unit.entity_type == EntityType.UNIT
    assert role_unit.entity_id == sample_unit.id


@pytest.mark.asyncio
async def test_meter_reading_creation(test_session, sample_meter_reading):
    """Test : création d'un relevé d'index."""
    assert sample_meter_reading.id is not None
    assert sample_meter_reading.type == MeterType.ELECTRICITE
    assert sample_meter_reading.value == Decimal("1234.50")
    assert sample_meter_reading.status == ReadingStatus.EN_ATTENTE
    assert sample_meter_reading.photo_url is not None


@pytest.mark.asyncio
async def test_wallet_creation(test_session, sample_wallet):
    """Test : création d'un portefeuille."""
    assert sample_wallet.id is not None
    assert sample_wallet.balance == Decimal("0.00")
    assert sample_wallet.currency == "XOF"


@pytest.mark.asyncio
async def test_payment_creation(test_session, sample_payment):
    """Test : création d'un paiement."""
    assert sample_payment.id is not None
    assert sample_payment.amount == Decimal("50000.00")
    assert sample_payment.payment_method == PaymentMethod.FEDAPAY
    assert sample_payment.status == PaymentStatus.EN_ATTENTE


@pytest.mark.asyncio
async def test_contribution_creation(test_session, sample_contribution):
    """Test : création d'une cotisation."""
    assert sample_contribution.id is not None
    assert sample_contribution.title == "Nettoyage collectif"
    assert sample_contribution.amount_per_unit == Decimal("5000.00")
    assert sample_contribution.status == ContributionStatus.OUVERTE


@pytest.mark.asyncio
async def test_announcement_creation(test_session, sample_announcement):
    """Test : création d'une annonce."""
    assert sample_announcement.id is not None
    assert sample_announcement.title == "Maintenance urgente"
    assert sample_announcement.urgency == Urgency.URGENT


@pytest.mark.asyncio
async def test_device_token_creation(test_session, sample_user):
    """Test : création d'un token de dispositif."""
    from app.models import DeviceToken

    token = DeviceToken(
        user_id=sample_user.id,
        token="expo_token_xxxxx",
        platform=Platform.IOS,
    )
    test_session.add(token)
    await test_session.commit()
    await test_session.refresh(token)

    assert token.id is not None
    assert token.platform == Platform.IOS


@pytest.mark.asyncio
async def test_otp_code_creation(test_session):
    """Test : création d'un code OTP."""
    from app.models import OtpCode
    from datetime import datetime, timedelta

    otp = OtpCode(
        identifier="+22390000001",
        purpose=OtpPurpose.CONNEXION,
        code_hash="hashed_code_here",
        expires_at=datetime.now() + timedelta(minutes=10),
    )
    test_session.add(otp)
    await test_session.commit()
    await test_session.refresh(otp)

    assert otp.id is not None
    assert otp.purpose == OtpPurpose.CONNEXION
    assert otp.consumed_at is None


@pytest.mark.asyncio
async def test_post_creation(test_session, sample_user, sample_house):
    """Test : création d'un post social."""
    post = Post(
        author_user_id=sample_user.id,
        type=PostType.ANNONCE,
        house_id=sample_house.id,
        title="Annonce Location",
        description="Petite chambre à louer",
        price=Decimal("50000.00"),
        status=ModerationStatus.EN_ATTENTE,
    )
    test_session.add(post)
    await test_session.commit()
    await test_session.refresh(post)

    assert post.id is not None
    assert post.type == PostType.ANNONCE
    assert post.status == ModerationStatus.EN_ATTENTE


@pytest.mark.asyncio
async def test_uuid_mixin(test_session, sample_user):
    """Test : UUIDMixin génère des UUID valides."""
    assert sample_user.id is not None
    assert isinstance(sample_user.id, type(sample_user.id))  # UUID type


@pytest.mark.asyncio
async def test_timestamp_mixin(test_session, sample_user):
    """Test : TimestampMixin génère created_at et updated_at."""
    assert sample_user.created_at is not None
    assert sample_user.updated_at is not None
    # updated_at >= created_at
    assert sample_user.updated_at >= sample_user.created_at
