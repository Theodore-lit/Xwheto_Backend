#!/bin/bash
# Script d'initialisation des migrations Alembic pour Xwétô

set -e

echo "=== Initialisation des migrations Alembic ==="
echo ""

# Vérifier que alembic est installé
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic n'est pas installé. Installez via: pip install alembic"
    exit 1
fi

echo "✅ Alembic trouvé"
echo ""

# Générer la première migration
echo "🔄 Génération de la migration Phase 1 (User, OtpCode, EntityRole, Delegation, DeviceToken)..."
alembic revision --autogenerate -m "Phase_1_Users_Auth"

echo "✅ Migration Phase 1 générée"
echo ""

# Générer la migration Phase 2
echo "🔄 Génération de la migration Phase 2 (House, Unit, HouseRule, HouseRuleAcceptance)..."
alembic revision --autogenerate -m "Phase_2_Houses_Units"

echo "✅ Migration Phase 2 générée"
echo ""

# Générer la migration Phase 3
echo "🔄 Génération de la migration Phase 3 (Lease, LeaseInvitation, LeaseSignature, DepartureNotice, DepositDeduction)..."
alembic revision --autogenerate -m "Phase_3_Leases_Signatures"

echo "✅ Migration Phase 3 générée"
echo ""

# Générer la migration Phase 4-5
echo "🔄 Génération de la migration Phase 4-5 (MeterReading, Payment, Contribution, Communication, Post, Subscription, Admin)..."
alembic revision --autogenerate -m "Phase_4_5_MetierModules"

echo "✅ Migration Phase 4-5 générée"
echo ""

echo "=== Migrations générées avec succès ==="
echo "Fichiers de migration dans: alembic/versions/"
echo ""
echo "Pour appliquer les migrations:"
echo "  alembic upgrade head"
echo ""
echo "Pour voir le statut:"
echo "  alembic current"
