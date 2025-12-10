from app import db
from datetime import datetime


class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    
    document_type = db.Column(db.String(30), default='client_upload')
    description = db.Column(db.Text)
    
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    DOCUMENT_TYPES = [
        ('client_upload', 'Document client'),
        ('admin_upload', 'Document admin'),
        ('deliverable', 'Livrable'),
        ('revision', 'Révision')
    ]
    
    def get_type_display(self):
        for code, label in self.DOCUMENT_TYPES:
            if code == self.document_type:
                return label
        return self.document_type
    
    def __repr__(self):
        return f'<Document {self.id} - {self.original_filename}>'
