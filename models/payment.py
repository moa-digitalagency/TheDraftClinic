"""
================================================================================
TheDraftClinic - Modèle Paiement
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle Payment pour le suivi des paiements clients.
Il gère les acomptes, les paiements finaux et la vérification par l'admin.

Relations:
- Appartient à une demande de service (ServiceRequest)
- Vérifié par un utilisateur admin (User)
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
# MODÈLE PAIEMENT
# ==============================================================================

class Payment(db.Model):
    """
    Modèle représentant un paiement effectué par un client.
    
    Les paiements suivent un workflow de vérification:
    1. Le client soumet une preuve de paiement (status: pending)
    2. L'admin vérifie le paiement (status: verified ou rejected)
    3. Si vérifié, la demande passe en traitement
    
    Attributes:
        id (int): Clé primaire auto-incrémentée
        request_id (int): Clé étrangère vers la demande de service
        amount (float): Montant du paiement
        payment_type (str): Type de paiement (deposit, final, full)
        payment_method (str): Méthode utilisée (virement, PayPal, etc.)
        proof_document (str): Nom du fichier de preuve uploadé
        status (str): Statut du paiement (pending, verified, rejected)
        verified_by (int): ID de l'admin ayant vérifié
    
    Relationships:
        request: Demande de service associée
    """
    
    # Nom de la table dans la base de données
    __tablename__ = 'payments'
    
    # --------------------------------------------------------------------------
    # CLÉS
    # --------------------------------------------------------------------------
    
    # Clé primaire
    id = db.Column(
        db.Integer, 
        primary_key=True,
        doc="Identifiant unique du paiement"
    )
    
    # Clé étrangère vers la demande
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey('service_requests.id'), 
        nullable=False,
        index=True,
        doc="ID de la demande de service associée"
    )
    
    # --------------------------------------------------------------------------
    # INFORMATIONS DU PAIEMENT
    # --------------------------------------------------------------------------
    
    # Montant payé
    amount = db.Column(
        db.Float, 
        nullable=False,
        doc="Montant du paiement en euros"
    )
    
    # Type de paiement
    payment_type = db.Column(
        db.String(30), 
        default='deposit',
        doc="Type: deposit (acompte), final, ou full (complet)"
    )
    
    # Méthode de paiement
    payment_method = db.Column(
        db.String(50),
        doc="Méthode utilisée (bank_transfer, paypal, card, etc.)"
    )
    
    # --------------------------------------------------------------------------
    # PREUVE DE PAIEMENT
    # --------------------------------------------------------------------------
    
    # Fichier de preuve uploadé
    proof_document = db.Column(
        db.String(255),
        doc="Nom du fichier de preuve de paiement uploadé"
    )
    
    # Référence de transaction
    transaction_reference = db.Column(
        db.String(100),
        doc="Référence de la transaction bancaire"
    )
    
    # --------------------------------------------------------------------------
    # VÉRIFICATION
    # --------------------------------------------------------------------------
    
    # Statut du paiement
    status = db.Column(
        db.String(20), 
        default='pending',
        index=True,
        doc="Statut: pending, verified, rejected"
    )
    
    # Admin qui a vérifié
    verified_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        doc="ID de l'administrateur ayant vérifié le paiement"
    )
    
    # Date de vérification
    verified_at = db.Column(
        db.DateTime,
        doc="Date et heure de la vérification"
    )
    
    # Raison de rejet
    rejection_reason = db.Column(
        db.Text,
        doc="Explication en cas de rejet du paiement"
    )
    
    # Notes additionnelles
    notes = db.Column(
        db.Text,
        doc="Notes du client sur le paiement"
    )
    
    # --------------------------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------------------------
    
    # Date de création
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        doc="Date et heure de soumission du paiement"
    )
    
    # Date de modification
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        doc="Date et heure de dernière modification"
    )
    
    # --------------------------------------------------------------------------
    # CONSTANTES
    # --------------------------------------------------------------------------
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('verified', 'Vérifié'),
        ('rejected', 'Rejeté')
    ]
    
    PAYMENT_TYPES = [
        ('deposit', 'Acompte'),
        ('final', 'Paiement final'),
        ('full', 'Paiement complet')
    ]
    
    # --------------------------------------------------------------------------
    # MÉTHODES
    # --------------------------------------------------------------------------
    
    def get_status_display(self):
        """
        Retourne le libellé français du statut.
        
        Returns:
            str: Libellé du statut (ex: "En attente")
        """
        for code, label in self.STATUS_CHOICES:
            if code == self.status:
                return label
        logger.warning(f"Statut de paiement inconnu: {self.status}")
        return self.status
    
    def __repr__(self):
        """
        Représentation string du paiement pour le débogage.
        
        Returns:
            str: Représentation formatée du paiement
        """
        return f'<Payment {self.id} - {self.amount}€>'
