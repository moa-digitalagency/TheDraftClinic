"""
================================================================================
TheDraftClinic - Service Request Model Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module defines the ServiceRequest model for academic writing service
requests. It tracks the entire lifecycle from submission to delivery.
================================================================================
"""

from app import db
from datetime import datetime


class ServiceRequest(db.Model):
    """
    Service Request model representing academic writing project requests.
    
    This model tracks the complete workflow of a service request including:
    - Initial submission details
    - Quotation information
    - Payment status
    - Work progress
    - Delivery information
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        service_type: Type of academic service requested
        title: Project title
        description: Detailed project description
        status: Current request status
        quote_amount: Quoted price for the service
        deposit_required: Required deposit amount
        progress_percentage: Work completion percentage
    """
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    service_type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    additional_info = db.Column(db.Text)
    
    word_count = db.Column(db.Integer)
    pages_count = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    urgency_level = db.Column(db.String(20), default='standard')
    
    status = db.Column(db.String(30), default='submitted')
    progress_percentage = db.Column(db.Integer, default=0)
    
    quote_amount = db.Column(db.Float)
    quote_message = db.Column(db.Text)
    quote_sent_at = db.Column(db.DateTime)
    quote_accepted = db.Column(db.Boolean, default=False)
    
    deposit_required = db.Column(db.Float)
    deposit_paid = db.Column(db.Boolean, default=False)
    
    admin_notes = db.Column(db.Text)
    rejection_reason = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)
    
    documents = db.relationship('Document', backref='request', lazy='dynamic')
    payments = db.relationship('Payment', backref='request', lazy='dynamic')
    
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
    
    def get_status_display(self):
        for code, label in self.STATUS_CHOICES:
            if code == self.status:
                return label
        return self.status
    
    def get_service_display(self):
        for code, label in self.SERVICE_TYPES:
            if code == self.service_type:
                return label
        return self.service_type
    
    def __repr__(self):
        return f'<ServiceRequest {self.id} - {self.title}>'
