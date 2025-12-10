"""
================================================================================
TheDraftClinic - Modèle Journal d'Activité
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle ActivityLog pour l'historique des actions.
Il enregistre toutes les activités sur les projets (côté client et admin).

Relations:
- Appartient à une demande de service (ServiceRequest)
- Effectuée par un utilisateur (User)
================================================================================
"""

from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ActivityLog(db.Model):
    """
    Modèle représentant une entrée dans le journal d'activité.
    
    Enregistre toutes les actions effectuées sur un projet:
    - Commentaires pendant la rédaction
    - Livraisons de fichiers
    - Demandes de révision
    - Téléchargements de livrables
    - Changements de statut
    - Extensions de délai
    """
    
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey('service_requests.id'), 
        nullable=False,
        index=True
    )
    
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        nullable=False
    )
    
    action_type = db.Column(
        db.String(50), 
        nullable=False,
        index=True
    )
    
    title = db.Column(db.String(200))
    
    description = db.Column(db.Text)
    
    metadata_json = db.Column(db.Text)
    
    is_visible_to_client = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activity_logs', lazy='joined')
    service_request = db.relationship('ServiceRequest', backref='activity_logs', lazy='joined')
    
    ACTION_TYPES = [
        ('comment', 'Commentaire'),
        ('delivery', 'Livraison'),
        ('revision_request', 'Demande de révision'),
        ('revision_delivery', 'Livraison révision'),
        ('download', 'Téléchargement'),
        ('status_change', 'Changement de statut'),
        ('deadline_extension_request', 'Demande extension délai'),
        ('deadline_extension_approved', 'Extension délai approuvée'),
        ('deadline_extension_rejected', 'Extension délai refusée'),
        ('quote_sent', 'Devis envoyé'),
        ('quote_accepted', 'Devis accepté'),
        ('payment_submitted', 'Paiement soumis'),
        ('payment_verified', 'Paiement vérifié'),
        ('document_upload', 'Document uploadé'),
        ('progress_update', 'Mise à jour progression')
    ]
    
    def get_action_display(self):
        """Retourne le libellé français du type d'action."""
        for code, label in self.ACTION_TYPES:
            if code == self.action_type:
                return label
        return self.action_type
    
    def get_icon(self):
        """Retourne l'icône appropriée pour le type d'action."""
        icons = {
            'comment': 'message-circle',
            'delivery': 'package',
            'revision_request': 'edit-3',
            'revision_delivery': 'check-circle',
            'download': 'download',
            'status_change': 'refresh-cw',
            'deadline_extension_request': 'clock',
            'deadline_extension_approved': 'check',
            'deadline_extension_rejected': 'x',
            'quote_sent': 'file-text',
            'quote_accepted': 'thumbs-up',
            'payment_submitted': 'credit-card',
            'payment_verified': 'check-square',
            'document_upload': 'upload',
            'progress_update': 'trending-up'
        }
        return icons.get(self.action_type, 'activity')
    
    def get_color(self):
        """Retourne la couleur appropriée pour le type d'action."""
        colors = {
            'comment': 'blue',
            'delivery': 'green',
            'revision_request': 'orange',
            'revision_delivery': 'green',
            'download': 'gray',
            'status_change': 'purple',
            'deadline_extension_request': 'yellow',
            'deadline_extension_approved': 'green',
            'deadline_extension_rejected': 'red',
            'quote_sent': 'blue',
            'quote_accepted': 'green',
            'payment_submitted': 'yellow',
            'payment_verified': 'green',
            'document_upload': 'blue',
            'progress_update': 'indigo'
        }
        return colors.get(self.action_type, 'gray')
    
    @staticmethod
    def log_action(request_id, user_id, action_type, title=None, description=None, 
                   metadata=None, visible_to_client=True):
        """
        Helper pour créer une entrée de log d'activité.
        
        Args:
            request_id: ID de la demande
            user_id: ID de l'utilisateur
            action_type: Type d'action
            title: Titre de l'action
            description: Description détaillée
            metadata: Données supplémentaires (dict -> JSON)
            visible_to_client: Visible par le client
            
        Returns:
            ActivityLog: L'entrée créée
        """
        import json
        
        log = ActivityLog(
            request_id=request_id,
            user_id=user_id,
            action_type=action_type,
            title=title,
            description=description,
            metadata_json=json.dumps(metadata) if metadata else None,
            is_visible_to_client=visible_to_client
        )
        
        db.session.add(log)
        return log
    
    def __repr__(self):
        return f'<ActivityLog {self.id} - {self.action_type}>'
