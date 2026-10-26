"""Énumérations métier (valeurs stockées en français, alignées sur le modèle de données)."""
import enum


class UserStatus(str, enum.Enum):
    """Statut d'un utilisateur."""

    ACTIF = "actif"
    SUSPENDU = "suspendu"
    SUPPRIME = "supprime"


class OtpPurpose(str, enum.Enum):
    """Contexte de génération d'un OTP."""

    INSCRIPTION = "inscription"
    CONNEXION = "connexion"
    RESET = "reset"


class EntityType(str, enum.Enum):
    """Type d'entité dans le système de rôles contextuels."""

    HOUSE = "house"
    UNIT = "unit"


class RoleType(str, enum.Enum):
    """Rôle contextuel d'un utilisateur vis-à-vis d'une entité."""

    BAILLEUR = "bailleur"
    LOCATAIRE = "locataire"
    MEMBRE_SECONDAIRE = "membre_secondaire"
    MANAGER_DELEGUE = "manager_delegue"


class RoleStatus(str, enum.Enum):
    """Statut d'une attribution de rôle."""

    EN_ATTENTE = "en_attente"
    ACTIF = "actif"
    REVOQUE = "revoque"


class Platform(str, enum.Enum):
    """Plateforme d'un dispositif (pour les tokens de notification)."""

    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class UnitType(str, enum.Enum):
    """Type d'unité locative."""

    CHAMBRE = "chambre"
    BOUTIQUE = "boutique"
    ESPACE_LIBRE = "espace_libre"


class UnitStatus(str, enum.Enum):
    """Statut d'occupation d'une unité."""

    LIBRE = "libre"
    OCCUPEE = "occupee"


class LeaseStatus(str, enum.Enum):
    """Statut du cycle de vie d'un bail."""

    EN_ATTENTE_SIGNATURE = "en_attente_signature"
    ACTIF = "actif"
    TERMINE = "termine"
    RENOUVELE = "renouvele"


class InvitationStatus(str, enum.Enum):
    """Statut d'une invitation à signer un bail."""

    ENVOYEE = "envoyee"
    VUE = "vue"
    SIGNEE = "signee"
    REFUSEE = "refusee"
    EXPIREE = "expiree"


class RenewalStatus(str, enum.Enum):
    """Statut d'une demande de renouvellement."""

    EN_ATTENTE = "en_attente"
    CONFIRME = "confirme"
    REFUSE = "refuse"


class Initiator(str, enum.Enum):
    """Qui a initié une action (locataire ou bailleur)."""

    LOCATAIRE = "locataire"
    BAILLEUR = "bailleur"


class NoticeStatus(str, enum.Enum):
    """Statut d'un préavis de départ."""

    EN_COURS = "en_cours"
    TERMINE = "termine"
    ANNULE = "annule"


class MeterType(str, enum.Enum):
    """Type de compteur (électricité ou eau)."""

    ELECTRICITE = "electricite"
    EAU = "eau"


class ReadingStatus(str, enum.Enum):
    """Statut d'un relevé d'index."""

    EN_ATTENTE = "en_attente"
    APPROUVE = "approuve"
    CONTESTE = "conteste"


class ContributionStatus(str, enum.Enum):
    """Statut d'une cotisation collective."""

    OUVERTE = "ouverte"
    CLOTUREE = "cloturee"
    ANNULEE = "annulee"


class ContributionPaymentStatus(str, enum.Enum):
    """Statut du paiement d'une cotisation."""

    PAYE = "paye"
    NON_PAYE = "non_paye"


class TurnStatus(str, enum.Enum):
    """Statut d'un tour de salubrité."""

    A_FAIRE = "a_faire"
    FAIT = "fait"


class Urgency(str, enum.Enum):
    """Niveau d'urgence d'une annonce."""

    NORMAL = "normal"
    URGENT = "urgent"


class Channel(str, enum.Enum):
    """Canal de communication."""

    PUSH = "push"
    SMS = "sms"
    EMAIL = "email"


class DisputeObjectType(str, enum.Enum):
    """Type d'objet en litige."""

    METER_READING = "meter_reading"
    CONTRIBUTION_PAYMENT = "contribution_payment"
    DEPOSIT_DEDUCTION = "deposit_deduction"
    LEASE = "lease"


class DisputeStatus(str, enum.Enum):
    """Statut d'un litige."""

    OUVERTE = "ouverte"
    EN_DISCUSSION = "en_discussion"
    RESOLUE = "resolue"


class PaymentMethod(str, enum.Enum):
    """Méthode de paiement du loyer."""

    FEDAPAY = "fedapay"
    CASH = "cash"


class PaymentStatus(str, enum.Enum):
    """Statut d'un paiement."""

    REUSSI = "reussi"
    ECHOUE = "echoue"
    EN_ATTENTE = "en_attente"


class WalletTxType(str, enum.Enum):
    """Type de mouvement dans le portefeuille bailleur."""

    CREDIT = "credit"
    DEBIT = "debit"
    RETRAIT = "retrait"


class TxStatus(str, enum.Enum):
    """Statut d'une transaction."""

    EN_ATTENTE = "en_attente"
    REUSSI = "reussi"
    ECHOUE = "echoue"


class WithdrawalStatus(str, enum.Enum):
    """Statut d'une demande de retrait."""

    EN_ATTENTE = "en_attente"
    TRAITE = "traite"
    ECHOUE = "echoue"


class DeductionStatus(str, enum.Enum):
    """Statut d'une déduction sur caution."""

    PROPOSEE = "proposee"
    CONTESTEE = "contestee"
    VALIDEE = "validee"


class PostType(str, enum.Enum):
    """Type de post social."""

    ANNONCE = "annonce"
    STORY = "story"
    REEL = "reel"
    ARTICLE = "article"


class ModerationStatus(str, enum.Enum):
    """Statut de modération d'un contenu."""

    EN_ATTENTE = "en_attente"
    APPROUVE = "approuve"
    REJETE = "rejete"


class ContentType(str, enum.Enum):
    """Type de contenu à modérer."""

    POST = "post"
    COMMENT = "comment"


class CertificationStatus(str, enum.Enum):
    """Statut de certification d'un bailleur."""

    SUGGEREE = "suggeree"
    VALIDEE = "validee"
    REJETEE = "rejetee"


class SubscriptionStatus(str, enum.Enum):
    """Statut d'un abonnement."""

    ACTIF = "actif"
    EXPIRE = "expire"
    ANNULE = "annule"


class TicketStatus(str, enum.Enum):
    """Statut d'un ticket support."""

    OUVERT = "ouvert"
    EN_COURS = "en_cours"
    RESOLU = "resolu"
    FERME = "ferme"


class AdminRoleType(str, enum.Enum):
    """Rôle administrateur."""

    SUPER_ADMIN = "super_admin"
    MODERATEUR = "moderateur"
    SUPPORT = "support"
    FINANCE = "finance"
    LECTURE_SEULE = "lecture_seule"


class LegalDocType(str, enum.Enum):
    """Type de document légal."""

    CGU = "cgu"
    POLITIQUE_CONFIDENTIALITE = "politique_confidentialite"
