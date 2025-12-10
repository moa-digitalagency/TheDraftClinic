from app import db
from datetime import datetime


class Payment(db.Model):
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
