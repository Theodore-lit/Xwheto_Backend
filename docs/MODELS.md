# Documentation des Modèles Xwétô

## Vue d'ensemble

Xwétô implémente **57 tables** organisées en **9 modules métier**, avec une architecture stricte :
- **Type hints** : typage complet en Python et SQLAlchemy
- **Constraints** : validations CHECK, UNIQUE, FK au niveau BD
- **Enums** : stockées en VARCHAR (pas ENUM natif PG) pour éviter les migrations cassantes
- **UUIDs** : clés primaires UUID auto-générées
- **Timestamps** : `created_at` et `updated_at` côté serveur
- **Async-first** : tous les modèles prêts pour SQLAlchemy AsyncIO

---

## Module A : Utilisateurs & Authentification (6 tables)

### `users` - Compte unique par personne
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK, auto-généré |
| `phone` | VARCHAR(20) | UNIQUE, INDEX, nullable |
| `email` | VARCHAR(255) | UNIQUE, INDEX, nullable |
| `password_hash` | VARCHAR(255) | Jamais stocké en clair |
| `full_name` | VARCHAR(150) | Obligatoire |
| `photo_url` | VARCHAR(500) | Avatar utilisateur |
| `preferred_language` | VARCHAR(8) | Défaut: "fr" |
| `profile_completed` | BOOLEAN | Défaut: false |
| `phone_verified_at` | TIMESTAMP TZ | NULL = non vérifié |
| `email_verified_at` | TIMESTAMP TZ | NULL = non vérifié |
| `status` | VARCHAR(40) | Enum: ACTIF, SUSPENDU, SUPPRIME |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `phone IS NOT NULL OR email IS NOT NULL` (au moins un contact)
- Pas de rôle fixe (bailleur/locataire) — voir `entity_roles`

---

### `otp_codes` - Codes de verification (SMS/Email)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `identifier` | VARCHAR(255) | Phone ou email, INDEX |
| `purpose` | VARCHAR(40) | Enum: INSCRIPTION, CONNEXION, RESET |
| `code_hash` | VARCHAR(255) | Hash SHA256, jamais en clair |
| `attempts` | INTEGER | Compte les tentatives |
| `expires_at` | TIMESTAMP TZ | TTL du code |
| `consumed_at` | TIMESTAMP TZ | NULL = non utilisé |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `entity_roles` - Rôles contextuels (polymorphes)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id |
| `entity_type` | VARCHAR(40) | Enum: HOUSE, UNIT (polymorphe) |
| `entity_id` | UUID | UUID de l'entité (pas FK SQL) |
| `role_type` | VARCHAR(40) | Enum: BAILLEUR, LOCATAIRE, etc. |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, ACTIF, REVOQUE |
| `created_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- UNIQUE : `(user_id, entity_type, entity_id, role_type)`
- INDEX : `(entity_type, entity_id)` pour requêtes inverse

**Architecture critique** : Un user peut être BAILLEUR sur une maison et LOCATAIRE sur une autre. Les rôles sont contextuels, pas fixes au compte.

---

### `delegations` - Délégation de gestion
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `owner_user_id` | UUID | FK → users.id (propriétaire) |
| `delegate_user_id` | UUID | FK → users.id (manager) |
| `scope_type` | VARCHAR(40) | Enum: HOUSE, UNIT |
| `scope_id` | UUID | UUID du périmètre délégué |
| `permissions` | JSONB | Permissions granulaires |
| `revoked_at` | TIMESTAMP TZ | NULL = actif, sinon révoqué |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `secondary_members` - Membres secondaires (colocataires, enfants)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `primary_tenant_user_id` | UUID | FK → users.id (locataire principal) |
| `member_user_id` | UUID | FK → users.id (membre secondaire) |
| `permissions` | JSONB | Permissions limitées |
| `added_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- UNIQUE : `(lease_id, member_user_id)`

---

### `device_tokens` - Tokens de notifications push
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id (CASCADE) |
| `token` | VARCHAR(500) | Unique, JWT FCM ou APNs |
| `platform` | VARCHAR(40) | Enum: IOS, ANDROID, WEB |
| `created_at` | TIMESTAMP TZ | Server-side |

---

## Module B : Propriétés (4 tables)

### `houses` - Maison/Immeuble
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `owner_user_id` | UUID | FK → users.id |
| `name` | VARCHAR(150) | Nom du bien |
| `address` | VARCHAR(300) | Adresse complète |
| `city` | VARCHAR(100) | Ville, INDEX |
| `photo_url` | VARCHAR(500) | Photo du bien |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

---

### `units` - Unités locatives (chambre, boutique, etc.)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `house_id` | UUID | FK → houses.id |
| `type` | VARCHAR(40) | Enum: CHAMBRE, BOUTIQUE, ESPACE_LIBRE |
| `label` | VARCHAR(100) | "Chambre 101", "Boutique A" |
| `status` | VARCHAR(40) | Enum: LIBRE, OCCUPEE, INDEX |
| `rent_amount` | NUMERIC(14, 2) | Loyer défaut (snapshot dans Lease) |
| `deposit_amount` | NUMERIC(14, 2) | Caution |
| `advance_amount` | NUMERIC(14, 2) | Avance |
| `extra_fees` | NUMERIC(14, 2) | Frais supplémentaires |
| `notice_period_days` | INTEGER | Délai de préavis (défaut: 30) |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

---

### `house_rules` - Règlement intérieur
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `house_id` | UUID | FK → houses.id |
| `content` | TEXT | Texte du règlement |
| `version` | INTEGER | Numéro de version |
| `published_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- UNIQUE : `(house_id, version)`

---

### `house_rule_acceptances` - Acceptation du réglement
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `house_rule_id` | UUID | FK → house_rules.id (CASCADE) |
| `user_id` | UUID | FK → users.id |
| `accepted_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- UNIQUE : `(house_rule_id, user_id)`

---

## Module C : Bails (6 tables)

### `leases` - Bail numérique
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `unit_id` | UUID | FK → units.id |
| `tenant_user_id` | UUID | FK → users.id |
| `previous_lease_id` | UUID | FK → leases.id (nullable, chaîne renouvellement) |
| `start_date` | DATE | Début du bail |
| `end_date` | DATE | Fin (nullable pour perpétuel) |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE_SIGNATURE, ACTIF, TERMINE, RENOUVELE |
| `rent_amount` | NUMERIC(14, 2) | **SNAPSHOT** au moment du bail |
| `deposit_amount` | NUMERIC(14, 2) | **SNAPSHOT** |
| `advance_amount` | NUMERIC(14, 2) | **SNAPSHOT** |
| `extra_fees` | NUMERIC(14, 2) | **SNAPSHOT** |
| `notice_period_days` | INTEGER | **SNAPSHOT** |
| `pdf_url` | VARCHAR(500) | PDF du bail signé |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `end_date IS NULL OR end_date > start_date`
- UNIQUE partiel INDEX : `(unit_id)` WHERE `status = 'actif'` (un seul bail actif par unité)

---

### `lease_invitations` - Invitation à signer un bail
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `unit_id` | UUID | FK → units.id |
| `lease_id` | UUID | FK → leases.id (nullable au départ) |
| `invited_by_user_id` | UUID | FK → users.id (bailleur) |
| `invitee_user_id` | UUID | FK → users.id (nullable si phone/email) |
| `invitee_phone` | VARCHAR(20) | Numéro du locataire (si pas user) |
| `invitee_email` | VARCHAR(255) | Email du locataire (si pas user) |
| `token_hash` | VARCHAR(255) | UNIQUE, lien sécurisé |
| `status` | VARCHAR(40) | Enum: ENVOYEE, VUE, SIGNEE, REFUSEE, EXPIREE |
| `viewed_at` | TIMESTAMP TZ | Quand vu |
| `responded_at` | TIMESTAMP TZ | Quand accepté/refusé |
| `last_reminder_at` | TIMESTAMP TZ | Dernier rappel envoyé |
| `expires_at` | TIMESTAMP TZ | TTL de l'invitation |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `invitee_user_id IS NOT NULL OR invitee_phone IS NOT NULL OR invitee_email IS NOT NULL`

---

### `lease_signatures` - Signature électronique
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `user_id` | UUID | FK → users.id |
| `signed_at` | TIMESTAMP TZ | Server-side |
| `signature_data` | TEXT | Base64 ou hash de signature |
| `ip_address` | VARCHAR(64) | IP du signataire |

---

### `lease_renewal_requests` - Demande de renouvellement
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `requested_by_user_id` | UUID | FK → users.id |
| `requested_at` | TIMESTAMP TZ | Server-side |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, CONFIRME, REFUSE |
| `new_end_date` | DATE | Nouvelle date de fin |
| `confirmed_at` | TIMESTAMP TZ | Accepté/rejeté |

---

### `departure_notices` - Préavis de départ
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `initiated_by` | VARCHAR(40) | Enum: LOCATAIRE, BAILLEUR |
| `reason` | TEXT | Motif (optionnel) |
| `notice_date` | DATE | Date du préavis |
| `effective_date` | DATE | Date effective (>= notice_date + délai) |
| `status` | VARCHAR(40) | Enum: EN_COURS, TERMINE, ANNULE |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `deposit_deductions` - Déduction sur caution
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `created_by_user_id` | UUID | FK → users.id |
| `label` | VARCHAR(200) | Motif (casse, dégâts) |
| `amount` | NUMERIC(14, 2) | Montant déduit |
| `evidence_url` | VARCHAR(500) | Justificatif **obligatoire** |
| `status` | VARCHAR(40) | Enum: PROPOSEE, CONTESTEE, VALIDEE |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `amount > 0`

---

## Module D : Relevés & Factures (2 tables)

### `meter_readings` - Relevé d'index (électricité/eau)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `unit_id` | UUID | FK → units.id |
| `lease_id` | UUID | FK → leases.id |
| `type` | VARCHAR(40) | Enum: ELECTRICITE, EAU |
| `value` | NUMERIC(12, 2) | Valeur manuelle/OCR |
| `photo_url` | VARCHAR(500) | Photo **obligatoire** |
| `ocr_value` | NUMERIC(12, 2) | Valeur extraite par OCR |
| `ocr_confidence` | NUMERIC(4, 3) | Confiance OCR (0.000-1.000) |
| `submitted_by_user_id` | UUID | FK → users.id |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, APPROUVE, CONTESTE |
| `validated_by_user_id` | UUID | FK → users.id (nullable) |
| `validated_at` | TIMESTAMP TZ | Quand validé |
| `client_request_id` | UUID | UNIQUE, idempotence offline |
| `created_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `validated_by_user_id IS NULL OR validated_by_user_id <> submitted_by_user_id` (validation croisée)

---

### `invoices` - Facture générée
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `meter_reading_id` | UUID | FK → meter_readings.id (UNIQUE) |
| `unit_id` | UUID | FK → units.id |
| `lease_id` | UUID | FK → leases.id |
| `amount` | NUMERIC(14, 2) | Montant facturé |
| `period_start` | DATE | Début période |
| `period_end` | DATE | Fin période |
| `pdf_url` | VARCHAR(500) | PDF facture |
| `generated_at` | TIMESTAMP TZ | Auto-généré après approbation index |

---

## Module I : Paiements (5 tables)

### `payments` - Paiement du loyer
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `payer_user_id` | UUID | FK → users.id |
| `recorded_by_user_id` | UUID | FK → users.id (nullable, pour cash) |
| `amount` | NUMERIC(14, 2) | Montant |
| `payment_method` | VARCHAR(40) | Enum: FEDAPAY, CASH |
| `status` | VARCHAR(40) | Enum: REUSSI, ECHOUE, EN_ATTENTE |
| `fedapay_transaction_id` | VARCHAR(100) | UNIQUE, webhook idempotence |
| `receipt_pdf_url` | VARCHAR(500) | Reçu PDF |
| `proof_photo_url` | VARCHAR(500) | Photo preuve (cash) |
| `paid_at` | TIMESTAMP TZ | Quand payé |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `amount > 0`
- CHECK : `payment_method <> 'fedapay' OR fedapay_transaction_id IS NOT NULL OR status = 'en_attente'`

---

### `wallets` - Portefeuille bailleur
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `owner_user_id` | UUID | FK → users.id (UNIQUE) |
| `balance` | NUMERIC(14, 2) | Solde actuel |
| `currency` | VARCHAR(3) | Défaut: "XOF" |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `balance >= 0`

---

### `wallet_transactions` - Transactions du portefeuille
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `wallet_id` | UUID | FK → wallets.id |
| `type` | VARCHAR(40) | Enum: CREDIT, DEBIT, RETRAIT |
| `amount` | NUMERIC(14, 2) | Montant |
| `related_payment_id` | UUID | FK → payments.id (UNIQUE, nullable) |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, REUSSI, ECHOUE |
| `created_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `amount > 0`

---

### `withdrawal_requests` - Demande de retrait
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `wallet_id` | UUID | FK → wallets.id |
| `requested_by_user_id` | UUID | FK → users.id |
| `amount` | NUMERIC(14, 2) | Montant |
| `destination` | VARCHAR(50) | N° Mobile Money |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, TRAITE, ECHOUE |
| `requested_at` | TIMESTAMP TZ | Demande |
| `processed_at` | TIMESTAMP TZ | Traité |

**Constraints** :
- CHECK : `amount > 0`

---

### `payment_reminders` - Relances de paiement
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `lease_id` | UUID | FK → leases.id |
| `period_label` | VARCHAR(7) | "2026-10" |
| `level` | INTEGER | 1/2/3 (niveau relance) |
| `channel` | VARCHAR(40) | Enum: PUSH, SMS, EMAIL |
| `sent_at` | TIMESTAMP TZ | Envoyée |

**Constraints** :
- UNIQUE : `(lease_id, period_label, level)`

---

## Module E-F : Cotisations & Salubrité (4 tables)

### `contributions` - Cotisation collective
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `house_id` | UUID | FK → houses.id |
| `created_by` | UUID | FK → users.id |
| `title` | VARCHAR(200) | Libellé |
| `description` | TEXT | Détails |
| `amount_per_unit` | NUMERIC(14, 2) | Par unité |
| `due_date` | DATE | **Obligatoire** |
| `justificatif_url` | VARCHAR(500) | Justificatif (optionnel) |
| `status` | VARCHAR(40) | Enum: OUVERTE, CLOTUREE, ANNULEE |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `amount_per_unit > 0`

---

### `contribution_payments` - Paiement cotisation
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `contribution_id` | UUID | FK → contributions.id |
| `unit_id` | UUID | FK → units.id |
| `user_id` | UUID | FK → users.id (nullable) |
| `amount` | NUMERIC(14, 2) | Montant |
| `status` | VARCHAR(40) | Enum: PAYE, NON_PAYE |
| `paid_at` | TIMESTAMP TZ | Quand payé |
| `payment_method` | VARCHAR(30) | Cash, Fedapay, etc. |

**Constraints** :
- UNIQUE : `(contribution_id, unit_id)`

---

### `cleaning_schedules` - Calendrier de salubrité
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `house_id` | UUID | FK → houses.id |
| `frequency` | VARCHAR(30) | "hebdomadaire", "bimensuel" |
| `spaces` | JSONB | Espaces à nettoyer |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `cleaning_turns` - Tour individuel
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `cleaning_schedule_id` | UUID | FK → cleaning_schedules.id (CASCADE) |
| `unit_id` | UUID | FK → units.id |
| `scheduled_date` | DATE | Quand nettoyer, INDEX |
| `status` | VARCHAR(40) | Enum: A_FAIRE, FAIT |
| `photo_url` | VARCHAR(500) | Photo post-nettoyage |
| `completed_by_user_id` | UUID | FK → users.id (nullable) |
| `completed_at` | TIMESTAMP TZ | Fait à |

---

## Module G-H : Communications (7 tables)

### `announcements` - Annonce urgente
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `house_id` | UUID | FK → houses.id |
| `author_id` | UUID | FK → users.id |
| `title` | VARCHAR(200) | Titre |
| `content` | TEXT | Contenu |
| `urgency` | VARCHAR(40) | Enum: NORMAL, URGENT |
| `channels` | JSONB | [PUSH, SMS, EMAIL] |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `announcement_reads` - Suivi lecture annonce
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `announcement_id` | UUID | FK → announcements.id (CASCADE) |
| `user_id` | UUID | FK → users.id |
| `read_at` | TIMESTAMP TZ | Quand lu |

**Constraints** :
- UNIQUE : `(announcement_id, user_id)`

---

### `notification_preferences` - Préférences notification
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id (CASCADE) |
| `event_type` | VARCHAR(50) | "paiement", "alerte", "cotisation" |
| `channel` | VARCHAR(40) | Enum: PUSH, SMS, EMAIL |
| `enabled` | BOOLEAN | Activé/désactivé |

**Constraints** :
- UNIQUE : `(user_id, event_type, channel)`

---

### `disputes` - Litige/Réclamation
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `related_object_type` | VARCHAR(40) | Enum: METER_READING, PAYMENT, etc. |
| `related_object_id` | UUID | UUID de l'objet |
| `opened_by_user_id` | UUID | FK → users.id |
| `against_user_id` | UUID | FK → users.id |
| `reason` | TEXT | Motif |
| `evidence_url` | VARCHAR(500) | Preuve **obligatoire** |
| `status` | VARCHAR(40) | Enum: OUVERTE, EN_DISCUSSION, RESOLUE |
| `resolved_at` | TIMESTAMP TZ | Résolu à |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- CHECK : `opened_by_user_id <> against_user_id`

---

### `dispute_messages` - Message dans litige
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `dispute_id` | UUID | FK → disputes.id (CASCADE) |
| `author_id` | UUID | FK → users.id |
| `message` | TEXT | Contenu |
| `attachment_url` | VARCHAR(500) | Pièce jointe |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `ai_recommendations` - Recommandation IA
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `dispute_id` | UUID | FK → disputes.id |
| `requested_by_user_id` | UUID | FK → users.id |
| `content` | TEXT | Recommandation **non-contraignante** |
| `based_on` | JSONB | Données de base |
| `generated_at` | TIMESTAMP TZ | Générée |

---

### `ai_conversations` - Historique Xwétô-Assist
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id |
| `message` | TEXT | Question |
| `response` | TEXT | Réponse IA |
| `context_type` | VARCHAR(30) | "situation", "usage_app" |
| `created_at` | TIMESTAMP TZ | Server-side |

---

## Module J : Contenu Social (5 tables)

### `posts` - Post social polymorphe
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `author_user_id` | UUID | FK → users.id |
| `type` | VARCHAR(40) | Enum: ANNONCE, STORY, REEL, ARTICLE |
| `house_id` | UUID | FK → houses.id (nullable) |
| `unit_id` | UUID | FK → units.id (nullable) |
| `title` | VARCHAR(200) | Titre |
| `description` | TEXT | Description |
| `price` | NUMERIC(14, 2) | Prix (nullable) |
| `media_urls` | JSONB | [url1, url2, ...] |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, APPROUVE, REJETE |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

---

### `comments` - Commentaire
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `post_id` | UUID | FK → posts.id (CASCADE) |
| `author_user_id` | UUID | FK → users.id |
| `content` | TEXT | Contenu |
| `status` | VARCHAR(40) | Enum: EN_ATTENTE, APPROUVE, REJETE |
| `created_at` | TIMESTAMP TZ | Server-side |

---

### `reactions` - Réaction (like, etc.)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `post_id` | UUID | FK → posts.id (CASCADE) |
| `user_id` | UUID | FK → users.id |
| `type` | VARCHAR(20) | "like", "love", etc. |
| `created_at` | TIMESTAMP TZ | Server-side |

**Constraints** :
- UNIQUE : `(post_id, user_id, type)`

---

### `moderation_logs` - Log de modération
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `content_type` | VARCHAR(40) | Enum: POST, COMMENT |
| `content_id` | UUID | UUID du contenu, INDEX |
| `moderator_id` | UUID | FK → users.id (NULL = automatique) |
| `decision` | VARCHAR(40) | Enum: EN_ATTENTE, APPROUVE, REJETE |
| `reason` | TEXT | Motif |
| `decided_at` | TIMESTAMP TZ | Décision prise |

---

### `certifications` - Certification bailleur
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `owner_user_id` | UUID | FK → users.id |
| `house_id` | UUID | FK → houses.id |
| `status` | VARCHAR(40) | Enum: SUGGEREE, VALIDEE, REJETEE |
| `suggested_at` | TIMESTAMP TZ | Suggérée |
| `validated_by_admin_id` | UUID | FK → users.id (nullable) |
| `validated_at` | TIMESTAMP TZ | Validée |

**Constraints** :
- UNIQUE : `(owner_user_id, house_id)` (certification par paire)

---

## Module K : Abonnements (3 tables)

### `subscription_plans` - Plan d'abonnement
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `name` | VARCHAR(50) | UNIQUE ("Free", "Pro") |
| `price` | NUMERIC(14, 2) | Prix |
| `billing_period` | VARCHAR(20) | "mensuel", "annuel" |
| `description` | TEXT | Description |
| `is_active` | BOOLEAN | Disponible |

---

### `plan_features` - Feature par plan
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `plan_id` | UUID | FK → subscription_plans.id (CASCADE) |
| `feature_key` | VARCHAR(80) | "advanced_analytics" |
| `enabled` | BOOLEAN | Activée |

**Constraints** :
- UNIQUE : `(plan_id, feature_key)`

---

### `subscriptions` - Abonnement utilisateur
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id |
| `plan_id` | UUID | FK → subscription_plans.id |
| `status` | VARCHAR(40) | Enum: ACTIF, EXPIRE, ANNULE |
| `started_at` | TIMESTAMP TZ | Commencé |
| `renewed_at` | TIMESTAMP TZ | Renouvelé |
| `expires_at` | TIMESTAMP TZ | Expire |
| `pending_plan_id` | UUID | FK → subscription_plans.id (downgrade différé) |

---

## Module L-M-N : Admin & Support (7 tables)

### `support_tickets` - Ticket support
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id |
| `category` | VARCHAR(50) | "bug", "acces", "paiement_echec" |
| `subject` | VARCHAR(200) | Sujet |
| `description` | TEXT | Description |
| `status` | VARCHAR(40) | Enum: OUVERT, EN_COURS, RESOLU, FERME |
| `assigned_admin_id` | UUID | FK → users.id (nullable) |
| `resolved_at` | TIMESTAMP TZ | Résolu |
| `created_at` | TIMESTAMP TZ | Server-side |
| `updated_at` | TIMESTAMP TZ | Server-side |

---

### `audit_logs` - Journal d'audit (append-only)
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `admin_id` | UUID | FK → users.id |
| `action_type` | VARCHAR(80) | "user_created", INDEX |
| `target_type` | VARCHAR(50) | "User", "Lease" |
| `target_id` | UUID | UUID cible |
| `before_state` | JSONB | État avant |
| `after_state` | JSONB | État après |
| `created_at` | TIMESTAMP TZ | Server-side |

**Important** : Append-only, jamais UPDATE/DELETE

---

### `admin_roles` - Rôle administrateur
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id (UNIQUE) |
| `role` | VARCHAR(40) | Enum: SUPER_ADMIN, MODERATEUR, etc. |
| `permissions` | JSONB | Permissions granulaires |

---

### `sync_logs` - Suivi synchro offline
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id |
| `entity_type` | VARCHAR(50) | "MeterReading", "Payment" |
| `entity_id` | UUID | UUID entité |
| `client_request_id` | UUID | UNIQUE, idempotence |
| `client_timestamp` | TIMESTAMP TZ | Timestamp client |
| `server_timestamp` | TIMESTAMP TZ | Timestamp serveur |
| `conflict_resolution` | VARCHAR(30) | "none", "user_arbitrated", "server_wins" |
| `synced_at` | TIMESTAMP TZ | Synchronisée |

---

### `legal_documents` - Contenu légal
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `type` | VARCHAR(40) | Enum: CGU, POLITIQUE_CONFIDENTIALITE |
| `content` | TEXT | Contenu (Markdown) |
| `version` | INTEGER | Numéro version |
| `published_at` | TIMESTAMP TZ | Publié |
| `created_by_admin_id` | UUID | FK → users.id |

**Constraints** :
- UNIQUE : `(type, version)`

---

### `site_settings` - Paramètres site
| Colonne | Type | Notes |
|---------|------|-------|
| `id` | UUID | PK |
| `key` | VARCHAR(100) | UNIQUE ("maintenance_mode") |
| `value` | JSONB | Valeur JSON |
| `updated_at` | TIMESTAMP TZ | Server-side |
| `updated_by_admin_id` | UUID | FK → users.id (nullable) |

---

## Résumé des Chiffres

| Catégorie | Nombre | Détails |
|-----------|--------|---------|
| **Modules** | 9 | A à N |
| **Tables** | 57 | Voir énumération ci-dessus |
| **Colonnes** | ~500+ | Avec indexes, constraints |
| **Enums** | 40+ | Tous les enums métier |
| **Indexes** | 30+ | Incluant indexes partiels |
| **FK** | 80+ | Toutes avec ondelete spécifié |
| **Constraints** | 20+ | CHECK, UNIQUE, indexes partiels |

---

## Stratégie de Typage

### Python (Type Hints)
```python
user_id: Mapped[uuid.UUID] = fk("users.id")
balance: Mapped[Decimal] = mapped_column(Money)
status: Mapped[UserStatus] = mapped_column(pg_enum(UserStatus))
```

### Base de Données
- UUID : `UUID (as_uuid=True)` → types NATIVE UUID en PG
- Money : `NUMERIC(14, 2)` → décimales précises
- Enums : `VARCHAR(40)` → pas ENUM PG natif (meilleure migration)
- JSONB : `JSONB` → JSON sans validation stricte (flexible)

---

## Points Clés de Sécurité

1. **Pas de rôles figés** : Les rôles viennent de `entity_roles`, contextuels
2. **Validation croisée** : MeterReading doit être validée par quelqu'un d'autre
3. **Justificatifs obligatoires** : Photo pour les index, preuve pour déditions, etc.
4. **Audit trail** : AuditLog append-only pour compliance
5. **Timestamps serveur** : Pas de confiance client pour les dates
6. **Contraintes BD** : CHECK et UNIQUE appliqués à la BD, pas juste en code

---

## Migration Alembic

Pour générer les migrations :

```bash
cd xwhetô_Backend
alembic revision --autogenerate -m "Initial: All 57 tables"
alembic upgrade head
```

Pour voir le statut :
```bash
alembic current
alembic history
```

---

**Document généré le 2026-10-21 | Xwétô Backend API v1.0**
