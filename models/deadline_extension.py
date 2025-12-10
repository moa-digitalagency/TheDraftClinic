"""
================================================================================
TheDraftClinic - Modèle Extension de Délai
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle DeadlineExtension pour les demandes
d'extension de délai sur les projets.
================================================================================
"""

from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DeadlineExtension(db.Model):
    """
    Modèle pour les demandes d'extension de délai.
    
    L'admin peut demander plus de temps, le client doit approuver.
    """
    
    __tablename__ = 'deadline_extensions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey('service_requests.id'), 
        nullable=False,
        index=True
    )
    
    requested_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        nullable=False
    )
    
    original_deadline = db.Column(db.DateTime, nullable=False)
    
    new_deadline = db.Column(db.DateTime, nullable=False)
    
    reason = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='pending')
    
    responded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    response_message = db.Column(db.Text)
    
    responded_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service_request = db.relationship(
        'ServiceRequest', 
        backref='deadline_extensions',
        foreign_keys=[request_id]
    )
    requester = db.relationship('User', foreign_keys=[requested_by])
    responder = db.relationship('User', foreign_keys=[responded_by])
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Refusée')
    ]
    
    def get_status_display(self):
        """Retourne le libellé du statut."""
        for code, label in self.STATUS_CHOICES:
            if code == self.status:
                return label
        return self.status
    
    def get_extension_days(self):
        """Retourne le nombre de jours d'extension demandés."""
        if self.new_deadline and self.original_deadline:
            delta = self.new_deadline - self.original_deadline
            return delta.days
        return 0
    
    def __repr__(self):
        return f'<DeadlineExtension {self.id} - {self.status}>'
