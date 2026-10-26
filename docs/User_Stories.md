**XWÉTÔ**
 
**Backlog des User Stories**
 
*Gestion locative résidentielle transparente **&** collaborative*
 
**Légende priorité (MoSCoW) : **
 
| **Must — indispensable** | **Should — important** | **Could — souhaitable** |
| --- | --- | --- |
 
## **EP1 — Comptes, Entités de logement ****&**** Confidentialité**
 
*Le bailleur et le locataire créent chacun leur propre compte. Le bailleur structure ensuite ses biens en entités (Maison **>** Chambre / Boutique / Espace libre) avant d**'**y rattacher un locataire. **"**Bailleur**"** et **"**Locataire**"** sont des rôles contextuels liés à une relation avec une entité précise, et non des types de compte figés : un même utilisateur peut être bailleur sur une maison et locataire sur une autre entité ailleurs.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US1.1** | Bailleur | En tant que bailleur, je veux créer mon compte (téléphone/email + infos personnelles) pour accéder à mon espace de gestion. | Inscription possible par téléphone ou email ; vérification par OTP ; profil créé. | **Must** |
| **US1.2** | Locataire | En tant que locataire, je veux créer un compte unique et personnel, utilisable ensuite chez n'importe quel bailleur partenaire sur l'app, y compris si je deviens moi-même bailleur ailleurs. | Un seul compte par personne ; le compte porte plusieurs rôles contextuels selon les entités, sans duplication. | **Must** |
| **US1.3** | Bailleur | En tant que bailleur, je veux créer une entité "Maison" (nom, adresse, photo) comme conteneur principal de mon bien. | Une maison possède un nom, une adresse et peut recevoir plusieurs sous-entités. | **Must** |
| **US1.4** | Bailleur | En tant que bailleur, je veux créer, à l'intérieur d'une maison, des entités de type Chambre, Boutique ou Espace libre, chacune avec ses propres conditions financières (loyer, caution, avances, frais annexes). | Chaque entité a un type, un statut (libre/occupée) et ses propres conditions ; une maison peut contenir un nombre illimité d'entités. | **Must** |
| **US1.5** | Bailleur | En tant que bailleur, je veux rattacher un locataire (compte existant ou invitation par téléphone/email) à une entité précise de ma maison. | L'invitation cible une entité unique ; le locataire invité reçoit une notification avec le résumé des conditions. | **Must** |
| **US1.6** | Locataire | En tant que locataire, je veux consulter les conditions proposées et signer électroniquement pour valider mon entrée dans le logement, distinctement de la simple création de mon compte. | La signature électronique est requise avant activation du bail ; tant qu'elle n'est pas faite, le statut reste "en attente de validation". | **Must** |
| **US1.7** | Bailleur | En tant que bailleur, je veux suivre le statut de chaque invitation envoyée (envoyée / vue / signée / refusée) pour relancer si besoin. | Liste des invitations avec statut horodaté et possibilité de renvoyer un rappel. | **Should** |
| **US1.8** | Bailleur | En tant que bailleur, je veux pouvoir compléter volontairement mon profil (photo, pièce d'identité, justificatif) pour obtenir un badge "Profil complété", sans que ce soit exigé pour publier une maison. | Le badge s'affiche si toutes les pièces optionnelles sont fournies ; son absence ne bloque aucune fonctionnalité de gestion locative. | **Could** |
| **US1.9** | Locataire | En tant que locataire, je veux voir si un bailleur a un badge "Profil complété" pour me faire une idée de sa transparence, sans que ce soit un critère bloquant pour signer un bail. | Badge affiché comme simple indicateur informatif, jamais comme condition d'accès à une entité. | **Could** |
| **US1.10** | Locataire | En tant que locataire, je ne veux voir que les informations du bien où je suis actuellement rattaché, et rien d'autre concernant mon bailleur ou ses autres biens. | Aucune donnée d'une autre entité ou d'une autre maison du même bailleur n'est accessible au locataire ; règle vérifiée à chaque appel API, pas seulement côté interface. | **Must** |
 
## **EP2 — Multi-maisons ****&**** tableau de bord bailleur**
 
*Un bailleur peut posséder et gérer plusieurs maisons depuis un compte unique.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US2.1** | Bailleur | En tant que bailleur, je veux créer et gérer plusieurs maisons depuis mon compte unique. | Aucune limite fonctionnelle au nombre de maisons ; création aussi rapide que la première. | **Must** |
| **US2.2** | Bailleur | En tant que bailleur, je veux un tableau de bord consolidé (occupation, impayés, alertes) tous biens confondus, avec filtre par maison. | Vue globale + vue filtrée par maison ; indicateurs mis à jour en temps réel. | **Should** |
| **US2.3** | Bailleur | En tant que bailleur, je veux basculer rapidement d'une maison à l'autre, et plus largement d'un rôle (casquette) à l'autre si je suis aussi locataire ailleurs, sans me déconnecter. | Sélecteur de "contexte actif" (maison + rôle) persistant pendant la session. | **Should** |
 
## **EP3 — Compte utilisateur unique ****&**** relations multi-bailleurs**
 
*L**'**utilisateur n**'**a qu**'**un seul compte, même s**'**il cumule plusieurs rôles (bailleur sur un bien, locataire sur un autre) ou loue chez plusieurs bailleurs ; les statistiques restent cloisonnées par relation.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US3.1** | Locataire | En tant que locataire, je veux voir la liste de tous mes logements (actifs et passés), chez tous mes bailleurs, et basculer entre eux. | Liste chronologique des logements avec statut (actif/terminé) et bailleur associé. | **Must** |
| **US3.2** | Locataire / Bailleur | En tant qu'utilisateur, je veux que mes statistiques (ponctualité, historique) restent propres à chaque relation, sans mélange entre mes différents logements ou biens. | Chaque score/historique est calculé et affiché par relation ; aucune donnée d'une relation A visible dans une relation B. | **Must** |
| **US3.3** | Locataire | En tant que locataire, je veux consulter un indicateur de fiabilité de mon bailleur (délai de restitution de caution, réactivité, régularité des reçus) pour évaluer la relation. | Score calculé à partir d'événements factuels enregistrés dans l'app ; visible uniquement par les locataires liés à ce bailleur. | **Should** |
 
## **EP4 — Bail numérique, Règlement intérieur ****&**** Renouvellement**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US4.1** | Bailleur | En tant que bailleur, je veux enregistrer les conditions financières d'une entité (loyer, caution, avances, frais annexes, délai de préavis légal) pour générer un bail numérique clair et incontestable. | Bail généré en PDF horodaté, reprenant toutes les conditions saisies. | **Must** |
| **US4.2** | Bailleur | En tant que bailleur, je veux rédiger et publier le règlement intérieur de la maison (horaires, gestion du bruit, etc.) pour que chaque locataire le valide numériquement à son entrée. | Le règlement est présenté au moment de la signature (US1.6) et son acceptation est horodatée. | **Should** |
| **US4.3** | Locataire | En tant que locataire, je veux consulter mon bail, le règlement intérieur et les dates clés à tout moment depuis l'application. | Accès permanent en lecture seule depuis l'espace "Mon logement". | **Must** |
| **US4.4** | Locataire | En tant que locataire, je veux faire une demande de renouvellement de mon bail à l'approche de son échéance. | Demande envoyée au bailleur avec la date d'échéance actuelle ; statut "en attente de confirmation". | **Must** |
| **US4.5** | Bailleur | En tant que bailleur, je veux confirmer une demande de renouvellement, ce qui déclenche automatiquement le renouvellement effectif du bail. | À la confirmation, une nouvelle période de bail est générée automatiquement avec les mêmes conditions (modifiables avant validation finale). | **Must** |
 
## **EP5 — Départs ****&**** Préavis**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US5.1** | Locataire | En tant que locataire, je veux poser mon préavis de départ en respectant le délai fixé par mon bail, pour planifier mon déménagement légalement. | Le système bloque une date de départ antérieure au délai contractuel minimum. | **Must** |
| **US5.2** | Bailleur | En tant que bailleur, je veux envoyer un préavis officiel de libération à un locataire, avec motif et date d'échéance conforme au contrat. | Préavis généré en document daté, notifié au locataire, conforme au délai légal du bail. | **Must** |
| **US5.3** | Locataire / Bailleur | En tant que locataire et bailleur, je veux voir un compteur de jours restants avant la fin du bail/préavis, avec rappel des obligations de loyer jusqu'à la libération. | Compteur visible sur le tableau de bord ; rappel automatique X jours avant échéance. | **Should** |
 
## **EP6 — Consommation, Charges ****&**** Validation croisée**
 
*L**'**index (kWh/eau) peut être saisi par le locataire ou le bailleur ; l**'**autre partie doit toujours l**'**approuver avant génération de la facture.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US6.1** | Locataire / Bailleur | En tant que locataire ou bailleur, je veux saisir un relevé d'index (kWh ou eau) avec photo justificative du compteur. | Saisie possible par les deux rôles ; photo obligatoire ; horodatage automatique. | **Must** |
| **US6.2** | Locataire / Bailleur | En tant que partie n'ayant pas saisi l'index, je veux approuver ou contester la valeur soumise avant que la facture ne soit générée. | Tant que l'index n'est pas approuvé, aucune facture n'est émise ; une contestation ouvre automatiquement une réclamation (voir EP9). | **Must** |
| **US6.3** | Locataire / Bailleur | En tant que locataire et bailleur, je veux visualiser un graphique d'évolution des consommations sur les derniers mois pour détecter les surconsommations. | Graphique mensuel disponible dès 2 relevés validés ; alerte visuelle en cas de hausse anormale. | **Should** |
 
## **EP7 — Cotisations Collectives ****&**** Projets Communs**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US7.1** | Bailleur | En tant que bailleur, je veux créer une collecte de fonds ponctuelle (ampoules, vidange, réparation, gardiennage) en définissant le montant par ménage et la date limite. | Montant réparti automatiquement entre les entités occupées concernées ; date limite obligatoire. | **Must** |
| **US7.2** | Locataire | En tant que locataire, je veux être notifié pour payer ma part via Mobile Money/Carte et suivre l'avancement global ainsi que la facture justificative téléversée par le bailleur. | Statut de paiement individuel + barre de progression collective + pièce justificative consultable. | **Must** |
 
## **EP8 — Salubrité ****&**** Entretien Communal**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US8.1** | Bailleur | En tant que bailleur, je veux définir un calendrier de nettoyage (fréquence, jours, espaces) et distribuer automatiquement les tours entre locataires. | Rotation automatique équitable ; calendrier modifiable manuellement en cas d'exception. | **Should** |
| **US8.2** | Locataire | En tant que locataire, je veux recevoir un rappel avant mon tour, consulter le planning global et marquer ma tâche comme effectuée avec option photo. | Rappel envoyé la veille ; validation en un clic + photo optionnelle. | **Should** |
 
## **EP9 — Communication, Alertes ****&**** Litiges**
 
*Les notifications passent par plusieurs canaux (push, SMS, email). En cas de désaccord, l**'**IA peut proposer une recommandation, mais la plateforme n**'**intervient jamais comme tiers décisionnaire.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US9.1** | Bailleur | En tant que bailleur, je veux diffuser une alerte (coupure d'eau, travaux, réunion) simultanément par push, SMS et email à tous les locataires concernés. | Le canal SMS/email est utilisé automatiquement pour les alertes marquées "urgentes", même sans connexion à l'app. | **Must** |
| **US9.2** | Locataire / Bailleur | En tant qu'utilisateur, je veux choisir mes canaux préférés (push / SMS / email) par type d'événement (paiement, alerte, cotisation, salubrité). | Préférences enregistrées par catégorie d'événement, modifiables à tout moment. | **Should** |
| **US9.3** | Locataire | En tant que locataire, je veux consulter les annonces urgentes directement sur mon écran d'accueil. | Bandeau prioritaire persistant tant que l'annonce n'est pas lue. | **Must** |
| **US9.4** | Locataire / Bailleur | En tant que partie en désaccord (index contesté, déduction de caution contestée), je veux ouvrir une réclamation avec preuve à l'appui. | Réclamation liée à l'élément contesté (index, cotisation, caution) ; preuve (photo/texte) jointe obligatoire. | **Must** |
| **US9.5** | Locataire / Bailleur | En tant qu'utilisateur, je veux suivre le statut de ma réclamation (ouverte / en discussion / résolue) et être notifié de chaque évolution. | Historique de la réclamation horodaté et visible par les deux parties jusqu'à résolution. | **Should** |
| **US9.6** | Locataire / Bailleur | En tant que partie en réclamation, je veux que Xwétor-Assist me propose une recommandation de résolution basée sur l'historique de notre relation et des références juridiques en ligne. | Recommandation générée à la demande, non contraignante, avec mention explicite qu'elle ne remplace pas un conseil juridique formel ; la plateforme reste neutre et n'impose aucune décision. | **Should** |
 
## **EP10 — Assistant Virtuel ****&**** IA (****"****Xwétor-Assist****"****)**
 
*L**'**IA connaît en détail le fonctionnement de l**'**application en plus des données du compte de l**'**utilisateur.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US10.1** | Locataire / Bailleur | En tant qu'utilisateur, je veux poser à Xwétor-Assist des questions sur ma situation ("Quand finit mon préavis ?", "Combien dois-je pour le courant ?") ou sur le fonctionnement de l'app ("Comment créer une cotisation ?", "Où je vois ma caution ?"), pour obtenir une réponse immédiate sans passer par le support. | Réponse générée en moins de 3 secondes, à partir des données réelles du compte et d'une base de connaissance complète des fonctionnalités de l'app. | **Should** |
| **US10.2** | Locataire | En tant que locataire, je veux que l'IA analyse la photo du compteur pour pré-remplir automatiquement la valeur en kWh, avant validation croisée (US6.2). | Pré-remplissage éditable avant soumission ; l'OCR ne remplace jamais l'approbation humaine. | **Should** |
| **US10.3** | Bailleur | En tant que bailleur, je veux utiliser l'IA pour générer des rappels de paiement courtois ou des lettres de préavis formelles. | Texte généré modifiable avant envoi ; ton "courtois" ou "formel" sélectionnable. | **Could** |
 
## **EP11 — Transparence Financière, Historique ****&**** Caution**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US11.1** | Locataire | En tant que locataire, je veux visualiser le montant exact de ma caution bloquée et le solde de mes avances. | Montants toujours à jour, détaillés ligne par ligne (versements, déductions). | **Must** |
| **US11.2** | Locataire | En tant que locataire, je veux consulter l'historique complet de mes paiements et télécharger mes reçus horodatés en PDF. | Reçu PDF généré pour chaque paiement validé, téléchargeable individuellement ou en lot. | **Must** |
| **US11.3** | Bailleur | En tant que bailleur, je veux consulter un score de ponctualité par locataire (loyers à temps vs en retard). | Score recalculé automatiquement à chaque échéance de paiement. | **Should** |
| **US11.4** | Locataire | En tant que locataire, je veux voir un récapitulatif de mon temps d'occupation et mon historique de ponctualité pour valoriser mon profil. | Synthèse exportable, utilisable comme référence auprès d'un futur bailleur. | **Could** |
| **US11.5** | Bailleur | En tant que bailleur, je veux lister les déductions éventuelles (dégâts, impayés) avec justificatifs lors du départ, pour calculer le montant net de la caution à restituer. | Chaque déduction nécessite un justificatif ; le locataire peut contester via US9.4 avant restitution finale. | **Must** |
 
## **EP12 — Mode Hors-ligne (Offline-first)**
 
*Priorité forte compte tenu du contexte de connectivité du public cible.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US12.1** | Locataire / Bailleur | En tant qu'utilisateur, je veux pouvoir saisir un index, marquer une tâche de salubrité effectuée ou consulter mes documents même sans connexion. | Les actions clés (saisie d'index, tâches, consultation) fonctionnent hors-ligne et sont mises en file d'attente locale. | **Must** |
| **US12.2** | Système | En tant qu'utilisateur, je veux que mes actions hors-ligne se synchronisent automatiquement dès le retour de la connexion, avec gestion des conflits. | Synchronisation en arrière-plan ; en cas de conflit (ex: deux index soumis), l'utilisateur est alerté pour arbitrage. | **Must** |
| **US12.3** | Locataire / Bailleur | En tant qu'utilisateur, je veux voir clairement si une donnée est "en attente de synchronisation" ou "confirmée serveur". | Indicateur visuel distinct (icône/couleur) sur chaque élément non encore synchronisé. | **Should** |
 
## **EP13 — Exports Comptables**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US13.1** | Bailleur | En tant que bailleur, je veux exporter en PDF/Excel tous les loyers et charges perçus sur une période donnée, par maison ou de façon consolidée. | Export filtrable par période et par maison ; format PDF et Excel disponibles. | **Must** |
| **US13.2** | Locataire | En tant que locataire, je veux exporter mon propre historique de paiements pour mes démarches personnelles (justificatif de domicile, dossier). | Export PDF de l'historique complet, horodaté et signé numériquement par la plateforme. | **Should** |
 
## **EP14 — Administration de la plateforme (Admin)**
 
*L**'**admin supervise la plateforme mais n**'**intervient jamais comme tiers décisionnaire dans une relation bailleur-locataire. Pas de vérification KYC obligatoire pour l**'**usage de l**'**app.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US14.1** | Admin | En tant qu'admin, je veux consulter en lecture seule toutes les réclamations ouvertes sur la plateforme, sans pouvoir agir comme tiers décisionnaire. | Vue globale des réclamations avec statut et ancienneté ; aucune action de résolution disponible pour l'admin. | **Must** |
| **US14.2** | Admin | En tant qu'admin, je veux suspendre, réactiver ou supprimer un compte en cas d'abus avéré ou de demande légale (droit à l'oubli). | Action tracée et justifiée ; notification automatique à l'utilisateur concerné. | **Must** |
| **US14.3** | Admin | En tant qu'admin, je veux un tableau de bord global (nombre de maisons, utilisateurs actifs, volume de transactions, taux de réclamations) pour piloter la plateforme. | Indicateurs mis à jour en continu, filtrables par période et zone géographique. | **Must** |
| **US14.4** | Admin principal | En tant qu'admin principal, je veux créer d'autres comptes admin/modérateur avec des permissions différenciées (lecture seule, support, finance, modération). | Rôles internes distincts des rôles bailleur/locataire ; permissions granulaires. | **Should** |
| **US14.5** | Admin | En tant qu'admin, je veux configurer les paramètres globaux (CGU, textes légaux) sans intervention technique. | Interface de configuration versionnée ; historique des changements de CGU. | **Should** |
| **US14.6** | Admin | En tant qu'admin, je veux traiter les tickets de support liés à la plateforme (bugs, perte d'accès, paiement techniquement en échec, signalement de fraude), distincts des réclamations entre bailleur et locataire et des questions d'usage (absorbées par l'IA). | File de tickets avec statut et SLA ; aucun litige financier entre parties ni question d'usage classique n'y apparaît. | **Must** |
| **US14.7** | Admin | En tant qu'admin, je veux consulter un journal d'audit des actions sensibles (suspension de compte, modification de configuration, remboursement manuel) pour la traçabilité. | Chaque action sensible loggée avec auteur, date, avant/après. | **Must** |
| **US14.8** | Admin | En tant qu'admin, je veux superviser les transactions du portefeuille et les paiements Fedapay, et traiter les anomalies techniques (paiement en échec, double débit). | Vue des transactions filtrable par statut ; remboursement manuel possible en cas d'anomalie technique confirmée. | **Should** |
| **US14.9** | Admin | En tant qu'admin, je veux superviser les recommandations générées par Xwétor-Assist et pouvoir désactiver une fonctionnalité IA à chaud en cas de dérive. | Historique des recommandations IA consultable ; interrupteur global par fonctionnalité IA. | **Could** |
| **US14.10** | Admin | En tant qu'admin, je veux créer et gérer des plans d'abonnement (ex: Basique, Standard, Premium) et activer/désactiver des fonctionnalités par plan, sans intervention technique. | Interface de gestion des feature flags par plan ; changement appliqué immédiatement sans déploiement de code. | **Must** |
| **US14.11** | Admin | En tant qu'admin, je veux voir quel bailleur est sur quel plan et suivre les changements d'abonnement (upgrade/downgrade, expiration). | Vue par bailleur du plan actif, date de renouvellement et historique de changement. | **Must** |
| **US14.12** | Admin | En tant qu'admin, je veux valider ou rejeter une suggestion de certification "publication d'annonce" faite par l'algorithme pour un bailleur sur un bien précis. | L'algorithme propose, l'admin décide seul ; la certification est liée à la paire (bailleur, bien), pas au compte bailleur global. | **Must** |
| **US14.13** | Admin | En tant qu'admin, je veux modérer la file des annonces et commentaires en attente avant ou après publication. | File avec statut (en attente/approuvé/rejeté) ; action manuelle au départ, automatisable plus tard sans changer le flux. | **Must** |
| **US14.14** | Admin | En tant qu'admin, je veux envoyer une communication ciblée (tous les utilisateurs ou un segment) pour une maintenance ou une nouveauté. | Segmentation par rôle/zone/plan ; envoi multicanal (push/SMS/email). | **Could** |
| **US14.15** | Admin | En tant qu'admin, je veux exporter des rapports globaux (croissance, volume financier, taux d'usage par plan) pour le pilotage stratégique. | Export PDF/Excel filtrable par période. | **Should** |
 
## **EP15 — Paiement du loyer ****&**** Portefeuille**
 
*Paiement en ligne via Fedapay avec portefeuille bailleur (solution transitoire en attendant les API directes MTN/Moov), ou enregistrement manuel d**'**un paiement en espèces.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US15.1** | Locataire | En tant que locataire, je veux payer mon loyer en ligne directement depuis l'app via Fedapay. | Paiement traité via Fedapay ; confirmation immédiate ; échec géré avec message clair et possibilité de réessayer. | **Must** |
| **US15.2** | Bailleur | En tant que bailleur, je veux recevoir une confirmation et un reçu automatique dès qu'un paiement en ligne est reçu. | Reçu PDF généré et notifié immédiatement après confirmation Fedapay. | **Must** |
| **US15.3** | Bailleur | En tant que bailleur, je veux disposer d'un portefeuille alimenté par les loyers perçus en ligne, et pouvoir retirer mon argent à tout moment. | Solde du portefeuille toujours à jour ; demande de retrait déclenchée depuis l'app. | **Must** |
| **US15.4** | Bailleur | En tant que bailleur, je veux enregistrer manuellement un paiement reçu en espèces, avec une preuve optionnelle (photo du reçu papier), pour garder un historique complet même hors app. | Saisie manuelle possible à tout moment ; le paiement cash apparaît dans le même historique que les paiements en ligne. | **Must** |
| **US15.5** | Système | En tant que système, je veux envoyer des relances graduées automatiques en cas de retard de paiement du loyer. | Relance à J+X, J+Y avec intensité croissante ; alerte au bailleur si le retard dépasse un seuil qu'il a défini. | **Should** |
| **US15.6** | Locataire / Bailleur | En tant qu'utilisateur, je veux consulter un historique unifié de toutes les transactions (en ligne et cash), peu importe le canal utilisé. | Historique unique, trié chronologiquement, avec indication claire du mode de paiement pour chaque ligne. | **Must** |
 
## **EP16 — Colocation ****&**** Délégation de gestion**
 
*Deux logiques distinctes : un membre secondaire ajouté par un locataire (accès limité, ne peut pas engager la relation contractuelle) et un manager délégué par un propriétaire (permissions plus larges, mais certaines actions restent réservées au propriétaire lui-même).*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US16.1** | Locataire | En tant que locataire légal, je veux ajouter un membre secondaire (enfant, frère) à mon entité pour partager le suivi de ma location. | Le membre secondaire est rattaché à l'entité, distinct du locataire légal, avec un accès limité défini par défaut. | **Should** |
| **US16.2** | Membre secondaire | En tant que membre secondaire, je veux utiliser Xwétor-Assist et effectuer des actions limitées (ex: valider une tâche de salubrité) sans engager la relation contractuelle. | Accès restreint : pas de signature, pas de gestion de paiement ni d'index ; chaque action reste attribuée nominativement à l'auteur réel. | **Should** |
| **US16.3** | Bailleur | En tant que bailleur, je veux voir combien de membres sont rattachés à une entité et savoir qui a réalisé chaque action. | Liste des membres par entité ; chaque action de l'historique affiche l'auteur exact (locataire légal ou membre). | **Should** |
| **US16.4** | Bailleur / Propriétaire | En tant que propriétaire, je veux déléguer la gestion d'un bien ou d'une entité à un manager (enfant, employé) avec des permissions définies. | Le manager peut agir sur le périmètre confié (bien ou entité) selon les permissions accordées par le propriétaire. | **Should** |
| **US16.5** | Système | En tant que système, je dois bloquer certaines actions sensibles pour un manager délégué, même avec des permissions larges : partage d'une annonce, signature de documents légaux, résiliation d'une entité, retrait du portefeuille. | Ces actions ne sont exécutables que par le compte du propriétaire lui-même, quelle que soit l'étendue des permissions déléguées. | **Must** |
 
## **EP17 — Onboarding ****&**** Prise en main**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US17.1** | Locataire / Bailleur | En tant que nouvel utilisateur, je veux suivre un tutoriel guidé à ma première connexion, adapté à mon rôle du moment. | Tutoriel contextuel affiché une seule fois (rejouable depuis les paramètres), différent selon le premier rôle actif de l'utilisateur. | **Should** |
| **US17.2** | Locataire / Bailleur | En tant qu'utilisateur, je veux accéder à une aide contextuelle depuis n'importe quel écran de l'application. | Bouton d'aide toujours visible, redirigeant vers Xwétor-Assist ou une fiche d'aide pertinente à l'écran courant. | **Should** |
 
## **EP18 — Contenu social ****&**** Annonces (MVP)**
 
*Version simplifiée pour le MVP : annonces structurées et commentaires uniquement, réservées aux bailleurs certifiés par bien. Pas d**'**agences ni de particuliers immobiliers externes. Le contenu de type reels/stories et les recommandations d**'**amis sont envisagés en version future (voir note technique en fin de document).*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US18.1** | Bailleur | En tant que bailleur certifié pour un bien donné, je veux publier une annonce structurée (photos, description, prix) pour ce bien précis. | Publication possible uniquement si la certification est active pour ce bien exact ; refusée pour tout autre bien non certifié du même bailleur. | **Must** |
| **US18.2** | Visiteur | En tant que visiteur (connecté ou non), je veux consulter les annonces publiques, y compris hors-ligne via le dernier cache synchronisé. | Accès sans authentification au fil public ; affichage du dernier contenu mis en cache si hors-ligne, sans chargement de nouveau contenu. | **Should** |
| **US18.3** | Locataire / Bailleur | En tant qu'utilisateur connecté, je veux commenter une annonce. | Commentaire visible après modération (US14.13) ; auteur identifié. | **Should** |
| **US18.4** | Admin | Voir US14.13 — modération des annonces et commentaires. | — | **Must** |
| **US18.5** | Algorithme / Admin | Voir US14.12 — suggestion de certification par bien, validée manuellement par l'admin. | — | **Must** |
 
## **EP19 — Abonnements (souscription utilisateur)**
 
*Gestion des plans côté admin en EP14 (US14.10/US14.11) ; ici, le parcours côté utilisateur.*
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US19.1** | Locataire / Bailleur | En tant qu'utilisateur, je veux consulter les plans disponibles et les fonctionnalités incluses dans chacun. | Page de comparaison des plans toujours accessible, sans engagement à la consulter. | **Must** |
| **US19.2** | Locataire / Bailleur | En tant qu'utilisateur, je veux souscrire ou changer de plan (upgrade/downgrade) directement depuis l'app. | Changement de plan effectif immédiatement après paiement confirmé ; rétrogradation effective à la fin de la période en cours. | **Must** |
 
## **EP20 — Internationalisation (Langues locales)**
 
| **ID** | **Acteur** | **User Story** | **Critères d****'****acceptation** | **Priorité** |
| --- | --- | --- | --- | --- |
| **US20.1** | Locataire / Bailleur | En tant qu'utilisateur, je veux choisir la langue de l'interface parmi le français et les langues locales disponibles (fon, yoruba, etc.). | Changement de langue appliqué immédiatement à toute l'interface, sans redémarrage de l'app. | **Should** |
| **US20.2** | Locataire / Bailleur | En tant qu'utilisateur, je veux que les réponses de Xwétor-Assist soient formulées dans la langue que j'ai choisie. | Réponses IA générées dans la langue active du profil utilisateur. | **Should** |
 
## **Note technique — Évolution future du contenu social (V2/V3)**
 
Le MVP (EP18) se limite volontairement aux annonces structurées et commentaires simples. Pour permettre une évolution ultérieure vers un contenu social plus riche (reels, stories, recommandations d'amis) sans refonte majeure, les principes suivants sont à respecter dès la conception :
 
- Modéliser le contenu comme une entité générique "Post" polymorphe (type : annonce, story, reel, article...) partageant auteur, média(s), légende, visibilité, commentaires et réactions — plutôt qu'une table figée "Annonce".
 
- Les recommandations d'amis pourront s'appuyer directement sur les relations déjà modélisées (co-locataires d'une même entité, locataires d'une même maison, anciens locataires d'un même bailleur), sans système de graphe social externe.
 
- Prévoir dès le MVP une file de modération avec statut (en attente / approuvé / rejeté), traitée manuellement au départ, afin de pouvoir y brancher un modèle de modération automatique plus tard sans changer le flux existant.
 
- Élargir progressivement le périmètre (messagerie privée, partage, fil algorithmique) uniquement une fois la gestion locative de base stabilisée et adoptée.