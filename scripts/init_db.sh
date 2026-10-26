#!/bin/bash
# Script d'initialisation complète de la BD Xwétô

set -e

echo "================================================"
echo "  Xwétô Backend — Initialisation BD PostgreSQL"
echo "================================================"
echo ""

# Vérifier que PostgreSQL est disponible
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL n'est pas installé ou psql n'est pas dans PATH"
    echo "   Installez PostgreSQL : https://www.postgresql.org/download/"
    exit 1
fi

echo "✅ PostgreSQL trouvé"
echo ""

# Vérifier les variables d'environnement
if [ -z "$PGUSER" ]; then
    PGUSER="postgres"
    echo "⚠️  PGUSER non défini, utilisation de 'postgres'"
fi

if [ -z "$PGHOST" ]; then
    PGHOST="localhost"
    echo "⚠️  PGHOST non défini, utilisation de 'localhost'"
fi

if [ -z "$PGPORT" ]; then
    PGPORT="5432"
    echo "⚠️  PGPORT non défini, utilisation de '5432'"
fi

echo "Connexion PostgreSQL : $PGUSER@$PGHOST:$PGPORT"
echo ""

# Demander confirmation
echo "Cela va :"
echo "  1. Créer la BD 'xweto_db'"
echo "  2. Créer l'utilisateur 'xweto'"
echo "  3. Appliquer les migrations Alembic"
echo ""
read -p "Continuer ? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Annulé"
    exit 1
fi

echo ""
echo "=== Étape 1 : Créer la BD et l'utilisateur ==="
echo ""

# Créer la BD et l'utilisateur
psql -U $PGUSER -h $PGHOST -p $PGPORT -tc "SELECT 1 FROM pg_database WHERE datname = 'xweto_db'" | grep -q 1 || \
    psql -U $PGUSER -h $PGHOST -p $PGPORT -c "CREATE DATABASE xweto_db"

echo "✅ BD 'xweto_db' créée (ou existe déjà)"

# Créer l'utilisateur
psql -U $PGUSER -h $PGHOST -p $PGPORT -tc "SELECT 1 FROM pg_roles WHERE rolname = 'xweto'" | grep -q 1 || \
    psql -U $PGUSER -h $PGHOST -p $PGPORT -c "CREATE USER xweto WITH PASSWORD 'xweto'"

echo "✅ Utilisateur 'xweto' créé (ou existe déjà)"

# Donner les droits
psql -U $PGUSER -h $PGHOST -p $PGPORT -c "GRANT ALL PRIVILEGES ON DATABASE xweto_db TO xweto"
echo "✅ Droits accordés à 'xweto'"

echo ""
echo "=== Étape 2 : Appliquer les migrations Alembic ==="
echo ""

# Vérifier qu'Alembic est installé
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic n'est pas installé"
    echo "   Installez via : pip install alembic"
    exit 1
fi

echo "✅ Alembic trouvé"
echo ""

# Aller au répertoire xwhetô_Backend
cd "$(dirname "$0")/.."

# Vérifier que .env existe
if [ ! -f ".env" ]; then
    echo "❌ Le fichier .env n'existe pas"
    echo "   Copiez .env.example en .env et configurez DATABASE_URL"
    exit 1
fi

echo "✅ Fichier .env trouvé"
echo ""

# Générer la migration si elle n'existe pas
if [ ! "$(ls -A alembic/versions/)" ]; then
    echo "🔄 Générant la migration initiale..."
    alembic revision --autogenerate -m "Initial: All 57 tables"
    echo "✅ Migration générée"
else
    echo "✅ Les migrations existent déjà"
fi

echo ""
echo "🔄 Appliquant les migrations..."
alembic upgrade head

echo ""
echo "✅ Migrations appliquées avec succès"

echo ""
echo "================================================"
echo "  ✅ Initialisation complète !"
echo "================================================"
echo ""
echo "Prochaines étapes :"
echo "  1. Vérifier la connexion :"
echo "     PGPASSWORD='xweto' psql -U xweto -h $PGHOST -p $PGPORT -d xweto_db -c '\\dt'"
echo ""
echo "  2. Lancer les tests :"
echo "     pytest tests/test_models_basic.py -v"
echo ""
echo "  3. Lancer FastAPI :"
echo "     uvicorn app.main:app --reload"
echo ""
