"""
================================================================================
TheDraftClinic - Modèle Demande de Révision
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle RevisionRequest pour les demandes de révision
sur les livrables. Le client peut demander des modifications après livraison.
================================================================================
"""

from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RevisionRequest(db.Model):
    """
    Modèle pour les demandes de révision.
    
    Après réception d'un livrable, le client peut demander des révisions
    en spécifiant les modifications souhaitées et en joignant des fichiers.
    """
    
    __tablename__ = 'revision_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey('service_requests.id'), 
        nullable=False,
        index=True
    )
    
    delivery_document_id = db.Column(
        db.Integer, 
        db.ForeignKey('documents.id')
    )
    
    requested_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        nullable=False
    )
    
    revision_details = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), default='pending')
    
    admin_response = db.Column(db.Text)
    
    responded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    responded_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    service_request = db.relationship(
        'ServiceRequest', 
        backref='revision_requests',
        foreign_keys=[request_id]
    )
    delivery_document = db.relationship('Document', foreign_keys=[delivery_document_id])
    requester = db.relationship('User', foreign_keys=[requested_by])
    responder = db.relationship('User', foreign_keys=[responded_by])
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('rejected', 'Refusée')
    ]
    
    def get_status_display(self):
        """Retourne le libellé du statut."""
        for code, label in self.STATUS_CHOICES:
            if code == self.status:
                return label
        return self.status
    
    def __repr__(self):
        return f'<RevisionRequest {self.id} - {self.status}>'


class RevisionAttachment(db.Model):
    """
    Modèle pour les fichiers joints aux demandes de révision.
    """
    
    __tablename__ = 'revision_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    revision_request_id = db.Column(
        db.Integer, 
        db.ForeignKey('revision_requests.id'), 
        nullable=False,
        index=True
    )
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    revision_request = db.relationship(
        'RevisionRequest', 
        backref='attachments'
    )
    uploader = db.relationship('User')
    
    def __repr__(self):
        return f'<RevisionAttachment {self.id} - {self.original_filename}>'
