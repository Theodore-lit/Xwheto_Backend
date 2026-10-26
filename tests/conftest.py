"""Fixtures pytest pour les tests de modèles."""
import asyncio
import uuid
from datetime import date, datetime, timedelta

import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models import (
    User,
    House,
    Unit,
    Lease,
    EntityRole,
    OtpCode,
    DeviceToken,
    HouseRule,
    MeterReading,
    Payment,
    Wallet,
    Contribution,
    Announcement,
    Post,
    AiConversation,
    SupportTicket,
    AuditLog,
    SubscriptionPlan,
    Subscription,
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
    TicketStatus,
    AdminRoleType,
    SubscriptionStatus,
)


@pytest.fixture(scope="session")
def event_loop():
    """Crée une boucle d'événements pour les tests async."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Crée un engine de test en base de données en mémoire SQLite (compatible avec tests unitaires)."""
    # Pour les tests, on peut utiliser SQLite en mémoire, ou une vrai BD de test
    # Ici on utilise SQLite pour la rapidité et l'isolation
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Crée une session de test pour chaque test."""
    TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def sample_user(test_session: AsyncSession) -> User:
    """Fixture : créer un utilisateur de test valide."""
    user = User(
        phone="+22390000001",
        email="user@example.com",
        password_hash="hashed_password_here",
        full_name="John Doe",
        status=UserStatus.ACTIF,
        profile_completed=True,
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def sample_house(test_session: AsyncSession, sample_user: User) -> House:
    """Fixture : créer une maison de test."""
    house = House(
        owner_user_id=sample_user.id,
        name="Maison Test",
        address="123 Rue de la Paix",
        city="Abidjan",
        photo_url="http://example.com/house.jpg",
    )
    test_session.add(house)
    await test_session.commit()
    await test_session.refresh(house)
    return house


@pytest.fixture
async def sample_unit(test_session: AsyncSession, sample_house: House) -> Unit:
    """Fixture : créer une unité locative de test."""
    unit = Unit(
        house_id=sample_house.id,
        type=UnitType.CHAMBRE,
        label="Chambre 101",
        status=UnitStatus.LIBRE,
        rent_amount=Decimal("50000.00"),
        deposit_amount=Decimal("100000.00"),
        advance_amount=Decimal("25000.00"),
        extra_fees=Decimal("5000.00"),
        notice_period_days=30,
    )
    test_session.add(unit)
    await test_session.commit()
    await test_session.refresh(unit)
    return unit


@pytest.fixture
async def sample_tenant(test_session: AsyncSession) -> User:
    """Fixture : créer un locataire de test."""
    tenant = User(
        phone="+22390000002",
        email="tenant@example.com",
        password_hash="hashed_password_tenant",
        full_name="Jane Tenant",
        status=UserStatus.ACTIF,
        profile_completed=True,
    )
    test_session.add(tenant)
    await test_session.commit()
    await test_session.refresh(tenant)
    return tenant


@pytest.fixture
async def sample_lease(test_session: AsyncSession, sample_unit: Unit, sample_tenant: User) -> Lease:
    """Fixture : créer un bail de test."""
    lease = Lease(
        unit_id=sample_unit.id,
        tenant_user_id=sample_tenant.id,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=365),
        status=LeaseStatus.ACTIF,
        rent_amount=Decimal("50000.00"),
        deposit_amount=Decimal("100000.00"),
        advance_amount=Decimal("25000.00"),
        extra_fees=Decimal("5000.00"),
        notice_period_days=30,
    )
    test_session.add(lease)
    await test_session.commit()
    await test_session.refresh(lease)
    return lease


@pytest.fixture
async def sample_entity_role(test_session: AsyncSession, sample_user: User, sample_house: House) -> EntityRole:
    """Fixture : créer un rôle contextuel de test."""
    role = EntityRole(
        user_id=sample_user.id,
        entity_type=EntityType.HOUSE,
        entity_id=sample_house.id,
        role_type=RoleType.BAILLEUR,
        status=RoleStatus.ACTIF,
    )
    test_session.add(role)
    await test_session.commit()
    await test_session.refresh(role)
    return role


@pytest.fixture
async def sample_wallet(test_session: AsyncSession, sample_user: User) -> Wallet:
    """Fixture : créer un portefeuille de test."""
    wallet = Wallet(
        owner_user_id=sample_user.id,
        balance=Decimal("0.00"),
        currency="XOF",
    )
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)
    return wallet


@pytest.fixture
async def sample_meter_reading(test_session: AsyncSession, sample_unit: Unit, sample_lease: Lease, sample_user: User) -> MeterReading:
    """Fixture : créer un relevé d'index de test."""
    reading = MeterReading(
        unit_id=sample_unit.id,
        lease_id=sample_lease.id,
        type=MeterType.ELECTRICITE,
        value=Decimal("1234.50"),
        photo_url="http://example.com/meter.jpg",
        submitted_by_user_id=sample_user.id,
        status=ReadingStatus.EN_ATTENTE,
    )
    test_session.add(reading)
    await test_session.commit()
    await test_session.refresh(reading)
    return reading


@pytest.fixture
async def sample_payment(test_session: AsyncSession, sample_lease: Lease, sample_tenant: User) -> Payment:
    """Fixture : créer un paiement de test."""
    payment = Payment(
        lease_id=sample_lease.id,
        payer_user_id=sample_tenant.id,
        amount=Decimal("50000.00"),
        payment_method=PaymentMethod.FEDAPAY,
        status=PaymentStatus.EN_ATTENTE,
    )
    test_session.add(payment)
    await test_session.commit()
    await test_session.refresh(payment)
    return payment


@pytest.fixture
async def sample_contribution(test_session: AsyncSession, sample_house: House, sample_user: User) -> Contribution:
    """Fixture : créer une cotisation de test."""
    from app.models import Contribution

    contribution = Contribution(
        house_id=sample_house.id,
        created_by=sample_user.id,
        title="Nettoyage collectif",
        description="Nettoyage du quartier commun",
        amount_per_unit=Decimal("5000.00"),
        due_date=date.today() + timedelta(days=7),
        status=ContributionStatus.OUVERTE,
    )
    test_session.add(contribution)
    await test_session.commit()
    await test_session.refresh(contribution)
    return contribution


@pytest.fixture
async def sample_announcement(test_session: AsyncSession, sample_house: House, sample_user: User) -> Announcement:
    """Fixture : créer une annonce de test."""
    announcement = Announcement(
        house_id=sample_house.id,
        author_id=sample_user.id,
        title="Maintenance urgente",
        content="Eau coupée demain de 8h à 16h",
        urgency=Urgency.URGENT,
    )
    test_session.add(announcement)
    await test_session.commit()
    await test_session.refresh(announcement)
    return announcement
