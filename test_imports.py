#!/usr/bin/env python3
"""Script de test pour vérifier que tous les modèles s'importent correctement."""
import sys

try:
    print("🔍 Importation de la configuration...")
    from app.core.config import settings
    print(f"✅ Configuration chargée : {settings.PROJECT_NAME}")

    print("\n🔍 Importation de la base de données...")
    from app.core.database import Base, engine
    print(f"✅ Base SQLAlchemy et engine chargés")

    print("\n🔍 Importation des enums...")
    from app.models.enums import UserStatus, EntityType, RoleType
    print(f"✅ Enums chargés : UserStatus={UserStatus.ACTIF}")

    print("\n🔍 Importation des mixins...")
    from app.models.mixins import UUIDMixin, TimestampMixin
    print(f"✅ Mixins chargés")

    print("\n🔍 Importation de tous les modèles...")
    from app.models import (
        User,
        House,
        Unit,
        Lease,
        MeterReading,
        Payment,
        Wallet,
        Contribution,
        Post,
        Announcement,
        SupportTicket,
        AuditLog,
    )
    print(f"✅ Tous les modèles chargés")

    print("\n🔍 Vérification des tables du Base.metadata...")
    tables = list(Base.metadata.tables.keys())
    print(f"✅ {len(tables)} tables découvertes")
    for i, table_name in enumerate(sorted(tables), 1):
        print(f"   {i:2}. {table_name}")

    print("\n✅ Tous les tests d'import réussis ! Prêt pour les migrations Alembic.")
    sys.exit(0)

except Exception as e:
    print(f"\n❌ ERREUR : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
