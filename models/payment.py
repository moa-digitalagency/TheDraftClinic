"""
================================================================================
TheDraftClinic - Payment Model Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module defines the Payment model for tracking client payments
including deposits, final payments, and verification status.
================================================================================
"""

from app import db
from datetime import datetime


class Payment(db.Model):
    """
    Payment model for tracking client payments.
    
    Supports different payment types and verification workflow:
    - Clients submit payment proof
    - Admins verify and approve/reject payments
    - Status tracking throughout the process
    
    Attributes:
        id: Primary key
        request_id: Foreign key to ServiceRequest
        amount: Payment amount
        payment_type: Type (deposit, final, full)
        payment_method: Method used for payment
        proof_document: Uploaded payment proof filename
        status: Verification status
        verified_by: Admin who verified the payment
    """
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(30), default='deposit')
    payment_method = db.Column(db.String(50))
    
    proof_document = db.Column(db.String(255))
    transaction_reference = db.Column(db.String(100))
    
    status = db.Column(db.String(20), default='pending')
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
    
    def get_status_display(self):
        for code, label in self.STATUS_CHOICES:
            if code == self.status:
                return label
        return self.status
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount}>'
