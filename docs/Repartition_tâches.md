**XWÉTÔ**
 
**Répartition des Tâches — Roadmap de Développement**
 
*Backend **&** Frontend synchronisés, du niveau actuel jusqu**'**au déploiement*
 
Ce document découpe le développement de Xwétô en 10 phases séquentielles (Phase 0 à Phase 9), chacune couvrant un ou plusieurs modules du backlog. Pour chaque phase, les tâches backend et frontend sont présentées côte à côte, avec un point de synchronisation explicite qui indique la dépendance critique entre les deux équipes. Les phases sont conçues pour être menées dans l'ordre, sauf mention contraire.
 
## **Phase 0 — Fondations techniques (Sprint 0)**
 
***Objectif : ****Poser les fondations communes avant toute fonctionnalité métier, pour que backend et frontend démarrent sur des bases stables et compatibles.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Core] Finaliser config.py et .env ; connexion PostgreSQL asynchrone (asyncpg) ; session SQLAlchemy async [Core] Implémenter security.py (hash de mot de passe, JWT access + refresh) [Core] Implémenter exceptions.py (gestion d'erreurs centralisée, format de réponse uniforme) [Module A] Modèles SQLAlchemy : users, entity_roles, device_tokens [Auth] Endpoints auth.py : inscription (téléphone/email + OTP), connexion, refresh token [Infra] Initialiser Alembic, première migration (users, entity_roles) [Infra] Configurer CORS pour autoriser les origines du frontend [Infra] Exposer un schéma OpenAPI propre et documenté (tags, descriptions) dès le départ | [Setup] Initialiser le projet Expo (TypeScript strict) [Setup] Configurer NativeWind + tailwind.config.js (couleur primaire confirmée #96E1E9) [Setup] Mettre en place React Navigation (stack + tabs) et l'architecture Feature-First [Setup] Configurer le client Axios (intercepteurs, gestion et refresh automatique du token) [Setup] Mettre en place le script gen:types (codegen OpenAPI → TypeScript) [Setup] Configurer TanStack Query (provider, cache par défaut) et Zustand (store de session) [Auth] Écrans : inscription, connexion, saisie OTP [UI] Charger les polices Sora/Inter, construire les composants UI de base (Button, Input, Card) |
 
| **🔗 Point de synchronisation — **le frontend ne peut lancer gen:types qu'une fois les endpoints /auth exposés avec un schéma OpenAPI stable côté backend. Convenir d'un jour de "kickoff API" où le backend livre une v0 fonctionnelle de l'auth avant que le frontend n'attaque ses écrans connectés. |
| --- |
 
## **Phase 1 — Comptes, Entités ****&**** Rôles contextuels (EP1, EP2, EP3)**
 
***Objectif : ****Permettre à un bailleur de structurer ses biens et d**'**y rattacher un locataire, avec la logique de rôle contextuel pleinement opérationnelle.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Module A] Modèles : delegations, secondary_members [Module B] Modèles : houses, house_rules, house_rule_acceptances, units [Module C] Modèles : leases, lease_signatures [Services] house_service, unit_service, lease_service (création, invitation, signature) [CRUD] crud_house, crud_unit, crud_lease, crud_user [Endpoints] houses.py, units.py, leases.py (création, invitation, signature) [Dependencies] get_current_user, require_role(role_type, entity_id) — vérification de rôle contextuel systématique [Règle transverse] Isolation des données (US1.10) vérifiée à chaque endpoint, jamais uniquement côté UI | [EP1] Écrans bailleur : création de maison, création d'entité (chambre/boutique/espace libre) [EP1] Écran d'invitation d'un locataire (téléphone/email) [EP1] Écran locataire : consultation des conditions + signature électronique [EP2] Tableau de bord multi-maisons (liste, filtre, sélecteur de maison active) [EP3] Sélecteur de "contexte actif" (maison + rôle) persistant, visible dans toute l'app [EP3] Écran "Mes logements" (relations locataire actives/passées) [UI] Badge "Profil complété" (affichage conditionnel, jamais bloquant) |
 
| **🔗 Point de synchronisation — **convenir du contrat d'API pour l'objet "contexte actif" (quelles informations le frontend doit stocker après chaque connexion/changement de rôle) avant de coder le sélecteur, pour éviter des allers-retours de spécification. |
| --- |
 
## **Phase 2 — Bail (renouvellement / départs), Consommation ****&**** Charges (EP4, EP5, EP6)**
 
***Objectif : ****Couvrir le cycle de vie complet du bail au-delà de la signature, et mettre en place la validation croisée des index de consommation.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Module C] Modèles : lease_renewal_requests, departure_notices [Module D] Modèles : meter_readings, invoices [Services] meter_reading_service (validation croisée), invoice_service (calcul de facture), ocr_service (intégration Xwétô-Assist) [Endpoints] meter_readings.py (saisie, approbation/contestation), leases.py (renouvellement, préavis) [Tasks] génération asynchrone de la facture après validation d'un index | [EP4] Écran demande de renouvellement (locataire) + confirmation (bailleur) [EP5] Écran pose de préavis (locataire) + émission de préavis (bailleur), compteur de jours restants [EP6] Écran de saisie d'index avec appareil photo (react-native-vision-camera) + pré-remplissage OCR [EP6] Écran d'approbation/contestation d'un index [EP6] Graphique d'évolution de consommation ⚠️ décision à prendre : choisir une librairie de graphiques React Native (fl_chart était spécifique à Flutter, obsolète pour cette stack) |
 
| **🔗 Point de synchronisation — **définir conjointement le format exact de la réponse OCR (valeur détectée + niveau de confiance) avant que le frontend ne code l'écran de pré-remplissage, pour bien gérer le cas "confiance faible". |
| --- |
 
## **Phase 3 — Cotisations, Salubrité, Communication ****&**** Litiges (EP7, EP8, EP9)**
 
***Objectif : ****Mettre en place les fonctionnalités collaboratives de la maison et le canal de résolution des désaccords.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Module E] Modèles : contributions, contribution_payments [Module F] Modèles : cleaning_schedules, cleaning_turns [Module G] Modèles : announcements, notification_preferences, disputes, dispute_messages, ai_recommendations [Services] contribution_service (répartition automatique), cleaning_service (rotation équitable), notification_service (routage push/SMS/email), dispute_service [Tasks] notification_tasks (envoi asynchrone multicanal), rappel automatique avant tour de salubrité [Intégrations] connexion aux fournisseurs SMS/email retenus | [EP7] Écran création de cotisation (bailleur), écran de paiement de part + barre de progression (locataire) [EP8] Calendrier de salubrité, écran de validation de tâche avec photo optionnelle [EP9] Bandeau d'annonces urgentes sur l'écran d'accueil, écran de préférences de notification par canal [EP9] Écran d'ouverture de réclamation (preuve à l'appui), fil de suivi du statut |
 
| **🔗 Point de synchronisation — **convenir du format des pièces jointes (photos/preuves) — upload direct vers un stockage objet (type S3) avec URL retournée à l'API, jamais de transfert binaire via un endpoint JSON. |
| --- |
 
## **Phase 4 — Assistant IA, Paiement ****&**** Portefeuille (EP10, EP15)**
 
***Objectif : ****Mettre en place le paiement réel du loyer et l**'**assistant conversationnel, les deux fonctionnalités les plus visibles pour l**'**utilisateur final.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Module H] Modèle : ai_conversations [Module I] Modèles : payments, wallets, wallet_transactions, withdrawal_requests, payment_reminders [Services] payment_service (Fedapay + webhook), wallet_service, ai_service (Xwétô-Assist : réponses situationnelles + usage de l'app) [Tasks] relances graduées (payment_reminders), génération PDF du reçu après paiement confirmé [Sécurité] vérification stricte de la signature des webhooks Fedapay | [EP10] Écran de chat Xwétô-Assist [EP15] Écran de paiement du loyer (checkout Fedapay), écran portefeuille + demande de retrait (bailleur) [EP15] Formulaire d'enregistrement manuel d'un paiement cash (avec photo de preuve) [EP15] Historique unifié des transactions (en ligne + cash) |
 
| **🔗 Point de synchronisation — **tester le flux Fedapay de bout en bout en sandbox avant tout développement d'écran définitif côté frontend — le comportement du webhook conditionne l'état affiché après paiement (confirmation parfois différée). |
| --- |
 
## **Phase 5 — Transparence financière, Offline ****&**** Exports (EP11, EP12, EP13)**
 
***Objectif : ****Sécuriser la confiance financière (caution, historique) et livrer le mode hors-ligne, priorité forte du projet.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Module I/L] Endpoints de calcul du score de ponctualité, gestion des déductions de caution [Module M] Modèle : sync_logs ; endpoint de synchronisation par lot avec résolution de conflits [Services] pdf_service (reçus), export_service (génération PDF/Excel filtrable par période/maison) | [EP11] Écran caution/avances (détail ligne par ligne), historique de paiements + téléchargement de reçus [EP12] File d'attente locale pour les actions hors-ligne, indicateur "en attente de synchronisation" [EP12] Synchronisation automatique au retour du réseau + UI d'arbitrage en cas de conflit [EP13] Écran d'export (sélection de période, choix du format PDF/Excel) |
 
| **🔗 Point de synchronisation — **définir ensemble le contrat de synchronisation par lot (un endpoint unique acceptant un tableau d'actions horodatées) avant de commencer l'implémentation offline — c'est la partie la plus risquée techniquement du projet. |
| --- |
 
## **Phase 6 — Administration, Abonnements ****&**** Contenu social (EP14, EP16, EP18, EP19)**
 
***Objectif : ****Outiller l**'**administration de la plateforme et lancer la version MVP du contenu social et des abonnements.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Module J] Modèles : posts, comments, reactions, moderation_logs, certifications [Module K] Modèles : subscription_plans, plan_features, subscriptions [Module L] Modèles : support_tickets, audit_logs, admin_roles [Module N] Modèles : legal_documents, site_settings [Services] moderation_service, subscription_service (vérification de feature flag par plan), certification_service, legal_content_service (versioning CGU/PC), site_settings_service [Endpoints] endpoints admin protégés (admin_roles) pour créer/éditer une version de document légal ou un paramètre de site ; endpoints publics en lecture seule GET /legal/{type} et GET /site-settings (pas d'authentification requise, consommés par la landing/pages légales hébergées à part) [Sécurité] application des permissions non-délégables (US16.5) au niveau service, jamais seulement côté UI | [EP16] Écran de gestion des membres secondaires / managers délégués (ajout, permissions) [EP18] Fil d'annonces (public + connecté), écran de publication (bailleur certifié), commentaires [EP19] Écran de comparaison des plans, souscription/upgrade [Admin] Écran d'édition des CGU/Politique de Confidentialité (versionnée, historique consultable) et écran de gestion des site_settings (liens stores, stats affichées, coordonnées de contact) [Landing/pages légales — hors app mobile] consommation des endpoints publics /legal et /site-settings au chargement (ou à la régénération, si site statique) [Admin] ⚠️ décision à prendre : construire l'admin comme back-office web séparé (recommandé vu le volume de tableaux/filtres) plutôt que dans l'app mobile |
 
| **🔗 Point de synchronisation — **si un back-office web est retenu pour l'admin, il consommera la même API — s'assurer que les endpoints admin sont isolés par permission (admin_roles) côté backend, et non simplement cachés côté interface. Convenir aussi du format de contenu des documents légaux (markdown vs HTML) avant de coder l'éditeur admin ET la page de rendu côté landing, pour que les deux s'accordent sur le même format d'affichage. |
| --- |
 
## **Phase 7 — Onboarding ****&**** Internationalisation (EP17, EP20)**
 
***Objectif : ****Faciliter la prise en main pour un public peu technophile et ouvrir l**'**app aux langues locales.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| [Léger] Le champ preferred_language est déjà prévu sur users ; adapter ai_service pour répondre dans la langue active | [EP17] Tutoriel de première connexion (contextuel au rôle), aide contextuelle accessible partout [EP20] Mise en place de l'i18n (ex: i18next), sélecteur de langue, traduction des contenus statiques (français + langues locales) |
 
| **🔗 Point de synchronisation — **aucun point bloquant majeur — module largement frontend, peut être mené en parallèle d'une autre phase pour accélérer le planning global. |
| --- |
 
## **Phase 8 — Qualité, Sécurité ****&**** Mise au propre du code**
 
***Objectif : ****Stabiliser les deux bases de code avant le déploiement — aucune nouvelle fonctionnalité dans cette phase.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| Suite de tests pytest + pytest-asyncio (couverture des services critiques : validation croisée, paiement, permissions) Lint/format (ruff, black), typage statique (mypy) exécutés en CI Revue de sécurité des endpoints sensibles (paiement, résiliation, retrait) et des permissions non-délégables Logging structuré et gestion centralisée des erreurs Rate limiting sur les endpoints sensibles (auth, paiement) | Suite de tests Jest + React Native Testing Library (écrans critiques : auth, paiement, saisie d'index) Lint (ESLint) + vérification TypeScript stricte en CI Revue des cas limites offline et des erreurs réseau Audit du stockage sécurisé des tokens (expo-secure-store plutôt qu'AsyncStorage brut) Optimisation des performances (taille du bundle, chargement des images) |
 
| **🔗 Point de synchronisation — **geler les deux bases de code sur une version stable commune avant cette phase — c'est un jalon de stabilisation, pas une fenêtre pour de nouvelles fonctionnalités. |
| --- |
 
## **Phase 9 — Déploiement**
 
***Objectif : ****Mettre Xwétô en production de façon sécurisée, reproductible et supervisée.*
 
| **🔧 Backend** | **📱 Frontend** |
| --- | --- |
| Choix de l'hébergement (ex: Railway, Render, VPS) et de la base managée (Neon, Supabase, RDS…) Pipeline CI/CD (GitHub Actions) : lint → tests → migration → déploiement Configuration des secrets de production (jamais commités, via un gestionnaire de secrets) Monitoring et alerting (ex: Sentry pour les erreurs, logs centralisés) Sauvegardes automatiques de la base de production + test de restauration | Configuration EAS Build (profils dev / preview / production) Soumission aux stores (Google Play / App Store) ou déploiement web si applicable Monitoring des crashs (ex: Sentry pour React Native) Configuration des variables d'environnement par environnement (dev/staging/prod) |
 
| **🔗 Point de synchronisation — **le déploiement backend doit précéder toute soumission de build frontend en production — un build de prod ne doit jamais pointer vers un environnement de développement. |
| --- |
 
# **Décisions ouvertes à trancher avant/pendant le développement**
 
- Librairie de graphiques pour React Native (remplaçant fl_chart, spécifique à Flutter) — ex: Victory Native, react-native-chart-kit.
 
- Architecture de l'interface d'administration : back-office web séparé (recommandé) ou intégré à l'app mobile.
 
- Choix définitif de l'hébergement backend et de la base de données managée pour la production.
 
- Fournisseurs SMS et email retenus pour les notifications multicanal (EP9).
 
- Stratégie technique du mode hors-ligne côté mobile (file d'attente maison vs librairie dédiée type WatermelonDB).
 
- Réception du document officiel de charte graphique complète (nuances secondaires, états d'interaction, iconographie).