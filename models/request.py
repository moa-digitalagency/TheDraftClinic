"""
================================================================================
TheDraftClinic - Modèle Demande de Service
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle ServiceRequest pour les demandes de services
de rédaction académique. Il gère tout le cycle de vie d'une demande,
de la soumission à la livraison.

Relations:
- Appartient à un utilisateur (User)
- Peut avoir plusieurs documents (Document)
- Peut avoir plusieurs paiements (Payment)
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from app import db                           # Instance SQLAlchemy
from datetime import datetime                # Gestion des dates
import logging                               # Logging des erreurs

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


# ==============================================================================
# MODÈLE DEMANDE DE SERVICE
# ==============================================================================

class ServiceRequest(db.Model):
    """
    Modèle représentant une demande de service de rédaction académique.
    
    Ce modèle suit le cycle de vie complet d'une demande:
    1. Soumission par le client avec détails du projet
    2. Examen et devis par l'administrateur
    3. Acceptation du devis et paiement de l'acompte
    4. Traitement de la demande avec suivi de progression
    5. Livraison du travail final
    
    Attributes:
        id (int): Clé primaire auto-incrémentée
        user_id (int): Clé étrangère vers l'utilisateur
        service_type (str): Type de service demandé
        title (str): Titre du projet
        description (str): Description détaillée
        status (str): Statut actuel de la demande
        quote_amount (float): Montant du devis
        progress_percentage (int): Pourcentage d'avancement (0-100)
    
    Relationships:
        user: Utilisateur qui a soumis la demande
        documents: Documents associés à la demande
        payments: Paiements effectués pour cette demande
    """
    
    # Nom de la table dans la base de données
    __tablename__ = 'service_requests'
    
    # --------------------------------------------------------------------------
    # CLÉS
    # --------------------------------------------------------------------------
    
    # Clé primaire
    id = db.Column(
        db.Integer, 
        primary_key=True,
        doc="Identifiant unique de la demande"
    )
    
    # Clé étrangère vers l'utilisateur
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'), 
        nullable=False,
        index=True,
        doc="ID de l'utilisateur ayant soumis la demande"
    )
    
    # --------------------------------------------------------------------------
    # INFORMATIONS DU PROJET
    # --------------------------------------------------------------------------
    
    # Type de service demandé
    service_type = db.Column(
        db.String(100), 
        nullable=False,
        doc="Code du type de service (thesis, dissertation, etc.)"
    )
    
    # Titre du projet
    title = db.Column(
        db.String(300), 
        nullable=False,
        doc="Titre du travail académique"
    )
    
    # Description détaillée
    description = db.Column(
        db.Text,
        doc="Description complète du projet et des attentes"
    )
    
    # Informations supplémentaires
    additional_info = db.Column(
        db.Text,
        doc="Notes additionnelles ou instructions spéciales"
    )
    
    # --------------------------------------------------------------------------
    # SPÉCIFICATIONS TECHNIQUES
    # --------------------------------------------------------------------------
    
    # Nombre de mots estimé
    word_count = db.Column(
        db.Integer,
        doc="Nombre de mots estimé ou requis"
    )
    
    # Nombre de pages
    pages_count = db.Column(
        db.Integer,
        doc="Nombre de pages estimé"
    )
    
    # Date limite
    deadline = db.Column(
        db.DateTime,
        doc="Date limite de livraison souhaitée"
    )
    
    # Niveau d'urgence
    urgency_level = db.Column(
        db.String(20), 
        default='standard',
        doc="Niveau d'urgence (standard, express_24h, express_5h)"
    )
    
    # --------------------------------------------------------------------------
    # STATUT ET PROGRESSION
    # --------------------------------------------------------------------------
    
    # Statut actuel de la demande
    status = db.Column(
        db.String(30), 
        default='submitted',
        index=True,
        doc="Statut actuel (submitted, in_progress, completed, etc.)"
    )
    
    # Pourcentage de progression
    progress_percentage = db.Column(
        db.Integer, 
        default=0,
        doc="Pourcentage d'avancement du travail (0-100)"
    )
    
    # --------------------------------------------------------------------------
    # INFORMATIONS DE DEVIS
    # --------------------------------------------------------------------------
    
    # Montant du devis
    quote_amount = db.Column(
        db.Float,
        doc="Montant total du devis en euros"
    )
    
    # Message accompagnant le devis
    quote_message = db.Column(
        db.Text,
        doc="Message explicatif envoyé avec le devis"
    )
    
    # Date d'envoi du devis
    quote_sent_at = db.Column(
        db.DateTime,
        doc="Date et heure d'envoi du devis"
    )
    
    # Acceptation du devis
    quote_accepted = db.Column(
        db.Boolean, 
        default=False,
        doc="True si le client a accepté le devis"
    )
    
    # --------------------------------------------------------------------------
    # INFORMATIONS DE PAIEMENT
    # --------------------------------------------------------------------------
    
    # Montant de l'acompte requis
    deposit_required = db.Column(
        db.Float,
        doc="Montant de l'acompte requis (généralement 50%)"
    )
    
    # Statut de paiement de l'acompte
    deposit_paid = db.Column(
        db.Boolean, 
        default=False,
        doc="True si l'acompte a été payé et vérifié"
    )
    
    # --------------------------------------------------------------------------
    # NOTES ADMINISTRATIVES
    # --------------------------------------------------------------------------
    
    # Notes internes de l'admin
    admin_notes = db.Column(
        db.Text,
        doc="Notes internes visibles uniquement par les admins"
    )
    
    # Raison de rejet
    rejection_reason = db.Column(
        db.Text,
        doc="Explication en cas de rejet de la demande"
    )
    
    # --------------------------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------------------------
    
    # Date de création
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        doc="Date et heure de soumission de la demande"
    )
    
    # Date de modification
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        doc="Date et heure de dernière modification"
    )
    
    # Date de livraison
    delivered_at = db.Column(
        db.DateTime,
        doc="Date et heure de livraison du travail"
    )
    
    # --------------------------------------------------------------------------
    # RELATIONS
    # --------------------------------------------------------------------------
    
    # Documents associés à cette demande
    documents = db.relationship(
        'Document',
        backref='request',
        lazy='dynamic',
        doc="Documents uploadés pour cette demande"
    )
    
    # Paiements pour cette demande
    payments = db.relationship(
        'Payment',
        backref='request',
        lazy='dynamic',
        doc="Paiements effectués pour cette demande"
    )
    
    # --------------------------------------------------------------------------
    # CONSTANTES - CHOIX DE STATUTS
    # --------------------------------------------------------------------------
    
    STATUS_CHOICES = [
        ('submitted', 'Soumise'),
        ('under_review', 'En examen'),
        ('quote_sent', 'Devis envoyé'),
        ('quote_accepted', 'Devis accepté'),
        ('awaiting_deposit', 'En attente d\'acompte'),
        ('deposit_pending', 'Acompte en vérification'),
        ('in_progress', 'En cours de traitement'),
        ('revision', 'En révision'),
        ('completed', 'Terminée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
        ('rejected', 'Refusée')
    ]
    
    # --------------------------------------------------------------------------
    # CONSTANTES - TYPES DE SERVICES
    # --------------------------------------------------------------------------
    
    SERVICE_TYPES = [
        ('thesis', 'Thèse de doctorat'),
        ('dissertation', 'Mémoire de master'),
        ('research_proposal', 'Proposition de recherche'),
        ('academic_proposal', 'Proposition académique'),
        ('book_chapter', 'Chapitre de livre'),
        ('research_paper', 'Article de recherche'),
        ('literature_review', 'Revue de littérature'),
        ('proofreading', 'Relecture et correction'),
        ('editing', 'Édition académique'),
        ('formatting', 'Mise en forme'),
        ('consultation', 'Consultation académique'),
        ('cv_resume', 'CV/Résumé académique'),
        ('personal_statement', 'Lettre de motivation'),
        ('grant_proposal', 'Proposition de subvention'),
        ('poster_review', 'Révision de poster'),
        ('other', 'Autre service')
    ]
    
    # --------------------------------------------------------------------------
    # MÉTHODES D'AFFICHAGE
    # --------------------------------------------------------------------------
    
    def get_status_display(self):
        """
        Retourne le libellé français du statut actuel.
        
        Returns:
            str: Libellé du statut (ex: "En cours de traitement")
            
        Example:
            >>> request.status = 'in_progress'
            >>> request.get_status_display()
            "En cours de traitement"
        """
        for code, label in self.STATUS_CHOICES:
            if code == self.status:
                return label
        # Retourne le code brut si non trouvé
        logger.warning(f"Statut inconnu: {self.status}")
        return self.status
    
    def get_service_display(self):
        """
        Retourne le libellé français du type de service.
        
        Returns:
            str: Libellé du service (ex: "Thèse de doctorat")
            
        Example:
            >>> request.service_type = 'thesis'
            >>> request.get_service_display()
            "Thèse de doctorat"
        """
        for code, label in self.SERVICE_TYPES:
            if code == self.service_type:
                return label
        # Retourne le code brut si non trouvé
        logger.warning(f"Type de service inconnu: {self.service_type}")
        return self.service_type
    
    # --------------------------------------------------------------------------
    # MÉTHODES SPÉCIALES
    # --------------------------------------------------------------------------
    
    def __repr__(self):
        """
        Représentation string de la demande pour le débogage.
        
        Returns:
            str: Représentation formatée de la demande
        """
        return f'<ServiceRequest {self.id} - {self.title[:30]}>'
