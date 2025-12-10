"""
================================================================================
TheDraftClinic - User Model Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module defines the User model for authentication and user management.
It includes fields for personal information, academic details, and admin status.
================================================================================
"""

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """
    User model representing both clients (researchers/students) and administrators.
    
    Attributes:
        id: Primary key
        email: Unique email address for login
        password_hash: Hashed password
        first_name: User's first name
        last_name: User's last name
        phone: Contact phone number
        institution: Academic institution
        academic_level: Level of study (licence, master, doctorat, etc.)
        field_of_study: Area of academic focus
        is_admin: Boolean flag for admin privileges
        is_active: Boolean flag for account status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    institution = db.Column(db.String(200))
    academic_level = db.Column(db.String(50))
    field_of_study = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requests = db.relationship('ServiceRequest', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.email}>'
