# Configuration des Migrations Alembic pour Xwétô

## Prérequis

1. **PostgreSQL** doit être en cours d'exécution
2. **Python >= 3.9** et les dépendances du `requirements.txt` doivent être installées :
   ```bash
   pip install -r requirements.txt
   ```
3. Un fichier `.env` correctement configuré avec une `DATABASE_URL` valide pointant vers PostgreSQL

## Configuration de la DATABASE_URL

Dans le fichier `.env` :

```env
DATABASE_URL=postgresql+asyncpg://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

Exemple pour localhost :
```env
DATABASE_URL=postgresql+asyncpg://xweto:xweto@localhost:5432/xweto_db
```

## Avant de générer les migrations

Assurez-vous que :
1. La base de données PostgreSQL existe
2. L'utilisateur dans DATABASE_URL a les droits de création de tables
3. Tous les fichiers modèles sont présents dans `app/models/`

## Générer la migration initiale

```bash
# Aller dans le répertoire xwhetô_Backend
cd xwhetô_Backend

# Générer la migration automatiquement (autogenerate)
alembic revision --autogenerate -m "Initial: All 57 tables and structures"
```

## Vérifier le fichier de migration

Une fois généré, consultez le fichier dans `alembic/versions/` pour vérifier :
- Toutes les tables sont créées
- Les contraintes CHECK et UNIQUE sont présentes
- Les indexes sont générés
- Les clés étrangères sont correctement formées

## Appliquer la migration

```bash
# Appliquer toutes les migrations en attente jusqu'à head
alembic upgrade head

# Vérifier le statut
alembic current

# Voir l'historique
alembic history
```

## Struture des modèles (18 tables par module)

### Phase 1 : Users & Auth (6 tables)
- `users`
- `otp_codes`
- `entity_roles`
- `delegations`
- `secondary_members`
- `device_tokens`

### Phase 2 : Houses & Units (4 tables)
- `houses`
- `units`
- `house_rules`
- `house_rule_acceptances`

### Phase 3 : Leases & Contracts (6 tables)
- `leases`
- `lease_invitations`
- `lease_signatures`
- `lease_renewal_requests`
- `departure_notices`
- `deposit_deductions`

### Phase 4-5 : Business Logic (41 tables)
- `meter_readings` + `invoices`
- `payments` + `wallets` + `wallet_transactions` + `withdrawal_requests` + `payment_reminders`
- `contributions` + `contribution_payments` + `cleaning_schedules` + `cleaning_turns`
- `announcements` + `announcement_reads` + `notification_preferences` + `disputes` + `dispute_messages` + `ai_recommendations` + `ai_conversations`
- `posts` + `comments` + `reactions` + `moderation_logs` + `certifications`
- `subscription_plans` + `plan_features` + `subscriptions`
- `support_tickets` + `audit_logs` + `admin_roles` + `sync_logs` + `legal_documents` + `site_settings`

## Développement itératif

Si vous voulez créer les migrations en plusieurs phases :

1. Créer une branche git : `git checkout -b migrations/phase1`
2. Modifier `app/models/__init__.py` pour importer seulement les modèles de Phase 1
3. Générer la migration : `alembic revision --autogenerate -m "Phase 1: Users & Auth"`
4. Appliquer : `alembic upgrade head`
5. Tester : `pytest tests/test_models_phase1.py`
6. Répéter pour Phase 2, 3, 4-5

## Troubleshooting

### Erreur : "Can't locate revision identified by ''"
→ Les migrations n'ont pas été générées. Exécutez `alembic revision --autogenerate`

### Erreur : "FATAL: database does not exist"
→ Créez d'abord la base : `createdb xweto_db` (via psql)

### Erreur : "FATAL: role 'username' does not exist"
→ Créez l'utilisateur : `createuser -P xweto` (via psql)

### Erreur : Import errors dans env.py
→ Vérifiez que Python peut importer `app.core.config` et `app.models`
→ Assurez-vous que `PYTHONPATH` inclut le répertoire `xwhetô_Backend/`

## Documentation

Pour plus d'infos sur Alembic :
- https://alembic.sqlalchemy.org/
- https://alembic.sqlalchemy.org/en/latest/tutorial.html
