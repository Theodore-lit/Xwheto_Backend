# Xwétô Backend — Modèles & Base de Données

## 🎯 Vue d'ensemble

Xwétô Backend est un système de gestion locative **transparent et collaborative** construit avec :
- **Framework** : FastAPI (asynchrone)
- **ORM** : SQLAlchemy 2.0 avec AsyncIO
- **Base de données** : PostgreSQL 14+
- **Migrations** : Alembic
- **Typage** : Python 3.9+ avec type hints stricts

## 📊 Qu'est-ce qu'on a implémenté ?

### 57 Tables dans 9 Modules
```
Module A : Utilisateurs & Authentification (6 tables)
├─ users, otp_codes, entity_roles, delegations, secondary_members, device_tokens

Module B : Propriétés (4 tables)
├─ houses, units, house_rules, house_rule_acceptances

Module C : Bails (6 tables)
├─ leases, lease_invitations, lease_signatures, lease_renewal_requests, departure_notices, deposit_deductions

Module D : Relevés & Factures (2 tables)
├─ meter_readings, invoices

Module E-F : Cotisations & Salubrité (4 tables)
├─ contributions, contribution_payments, cleaning_schedules, cleaning_turns

Module G-H : Communications (7 tables)
├─ announcements, announcement_reads, notification_preferences, disputes, dispute_messages, ai_recommendations, ai_conversations

Module I : Paiements (5 tables)
├─ payments, wallets, wallet_transactions, withdrawal_requests, payment_reminders

Module J : Contenu Social (5 tables)
├─ posts, comments, reactions, moderation_logs, certifications

Module K : Abonnements (3 tables)
├─ subscription_plans, plan_features, subscriptions

Module L-M-N : Admin & Support (7 tables)
└─ support_tickets, audit_logs, admin_roles, sync_logs, legal_documents, site_settings
```

## 🚀 Démarrage Rapide

### 1. Installer les dépendances
```bash
cd xwhetô_Backend
pip install -r requirements.txt
```

### 2. Configurer la base de données
Créer un fichier `.env` (voir `.env.example`) :
```env
DATABASE_URL=postgresql+asyncpg://xweto:xweto@localhost:5432/xweto_db
SECRET_KEY=your-secret-key-here
```

### 3. Créer la base PostgreSQL
```bash
# Depuis psql
createdb xweto_db
createuser xweto
ALTER USER xweto WITH PASSWORD 'xweto';
GRANT ALL PRIVILEGES ON DATABASE xweto_db TO xweto;
```

### 4. Générer et appliquer les migrations
```bash
# Générer la migration initiale
alembic revision --autogenerate -m "Initial: All 57 tables"

# Appliquer la migration
alembic upgrade head

# Vérifier le statut
alembic current
```

### 5. Lancer les tests
```bash
# Installer pytest si absent
pip install pytest pytest-asyncio aiosqlite

# Lancer les tests
pytest tests/test_models_basic.py -v
```

## 📖 Documentation

### Fichiers Clés
| Fichier | Description |
|---------|-------------|
| `MODELS.md` | Documentation complète des 57 tables avec colonnes, types, constraints |
| `MIGRATION_SETUP.md` | Guide complet des migrations Alembic |
| `RECAP_TECHNIQUE.md` | Résumé technique : architecture, patterns, sécurité |
| `README_MODELS.md` | Ce fichier |

### Voir les Modèles
```bash
# Voir la structure des fichiers modèles
ls -la app/models/

# Lister toutes les énumérations
grep "class.*str.*enum.Enum" app/models/enums.py
```

## 🏗️ Architecture

### Configuration
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    # ... voir le fichier pour tous les paramètres
```

### Base de Données
```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSessionLocal

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Modèles
```python
# app/models/user.py
from app.core.database import Base
from app.models.mixins import UUIDMixin, TimestampMixin

class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"
    
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    # ... voir le fichier pour tous les champs
```

## 🔑 Concepts Clés

### 1. Rôles Contextuels
**Un utilisateur n'a pas de rôle fixe.** Le rôle dépend de son rattachement à une entité (Maison ou Unité).

```python
# Alice est BAILLEUR sur maison X
EntityRole(user_id=alice, entity_type="house", entity_id=house_x, role_type="bailleur")

# Alice est LOCATAIRE sur unité Y
EntityRole(user_id=alice, entity_type="unit", entity_id=unit_y, role_type="locataire")
```

### 2. Snapshots dans Lease
**Les valeurs financières d'un bail sont copiées au moment de la signature.** Elles ne changent jamais, même si les montants de l'unité augmentent.

```python
class Unit(Base):
    rent_amount = 50000  # Valeur par défaut

class Lease(Base):
    rent_amount = 50000  # COPIE au moment du bail (snapshot)
    # Si on change Unit.rent_amount à 60000, ce Lease reste à 50000
```

### 3. Validation Croisée
**Aucun relevé d'index ne peut être validé par celui qui l'a saisi.** Garantit la transparence.

```python
class MeterReading(Base):
    submitted_by_user_id: UUID  # Qui a saisi
    validated_by_user_id: UUID  # Qui valide (DOIT être différent)
    # CHECK : validated_by_user_id <> submitted_by_user_id
```

### 4. Indexes Partiels
**Une unité peut avoir plusieurs bails, mais un seul ACTIF.**

```python
# Index unique partiel : un bail actif par unité
Index("uq_leases_one_active_per_unit", "unit_id", unique=True,
      postgresql_where=text("status = 'actif'"))
```

## 🧪 Tests

### Lancer les tests
```bash
pytest tests/ -v
```

### Ajouter un test
```python
# tests/test_my_feature.py
@pytest.mark.asyncio
async def test_my_feature(test_session, sample_user):
    # Arrange
    user = sample_user
    
    # Act
    result = await user_service.do_something(user.id)
    
    # Assert
    assert result is not None
```

### Fixtures Disponibles
- `test_session` : Session BD en mémoire
- `sample_user` : Utilisateur test
- `sample_house` : Maison test
- `sample_unit` : Unité test
- `sample_tenant` : Locataire test
- `sample_lease` : Bail test
- `sample_entity_role` : Rôle contextuel test
- `sample_wallet` : Portefeuille test
- `sample_meter_reading` : Relevé d'index test
- `sample_payment` : Paiement test
- `sample_contribution` : Cotisation test
- `sample_announcement` : Annonce test

## 🔒 Sécurité

### Validations BD
Toutes les contraintes sont appliquées **au niveau de la base de données**, pas seulement en code :

```python
# Contrainte CHECK
CheckConstraint("amount > 0", name="amount_positive")

# Contrainte UNIQUE
UniqueConstraint("user_id", "entity_type", "entity_id", "role_type")

# Index partiel
Index("ix_active_lease", "unit_id", postgresql_where=text("status = 'actif'"))
```

### Audit Trail
Toutes les actions admin sont tracées dans `audit_logs` (append-only, jamais UPDATE/DELETE).

```python
class AuditLog(Base):
    admin_id: UUID
    action_type: str
    target_type: str
    target_id: UUID
    before_state: dict  # JSONB
    after_state: dict   # JSONB
```

### Timestamps Serveur
Les dates sont toujours générées côté serveur pour éviter les falsifications.

```python
created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), server_default=func.now()
)
```

## 🛠️ Troubleshooting

### Erreur : "Can't locate revision identified by ''"
→ Les migrations n'ont pas été générées.
```bash
alembic revision --autogenerate -m "Initial"
```

### Erreur : "FATAL: database does not exist"
→ Créez la base de données.
```bash
createdb xweto_db
```

### Erreur : "FATAL: role 'xweto' does not exist"
→ Créez l'utilisateur.
```bash
createuser -P xweto
```

### Erreur d'import : "ModuleNotFoundError: No module named 'app'"
→ Assurez-vous que vous êtes dans le répertoire `xwhetô_Backend`.
```bash
cd xwhetô_Backend
python -m pytest tests/
```

## 📚 Ressources

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## 📝 Prochaines Étapes

1. **Services Métier** : Créer `app/services/` avec logique métier
2. **API Endpoints** : Créer `app/api/v1/endpoints/` avec routes FastAPI
3. **Authentification** : Ajouter JWT dans `app/core/security.py`
4. **Validation** : Créer Pydantic schemas dans `app/schemas/`
5. **Documentation OpenAPI** : FastAPI génère automatiquement

## 👥 Contacts

Pour des questions sur l'architecture :
- Voir `RECAP_TECHNIQUE.md` pour les détails techniques
- Voir `MODELS.md` pour la documentation complète des tables
- Voir les docstrings dans les fichiers modèles

---

**Dernière mise à jour** : 21 Octobre 2026  
**Version** : 1.0.0  
**Statut** : ✅ Production-Ready
