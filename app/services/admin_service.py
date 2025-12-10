"""
================================================================================
TheDraftClinic - Admin Service Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module provides administrative services including default admin user
creation and management utilities.
================================================================================
"""

import os
from app import db
from app.models.user import User


def create_default_admin():
    """
    Create a default administrator account if one doesn't exist.
    
    This function checks for existing admin user and creates one if:
    - No admin with the specified email exists
    - ADMIN_PASSWORD environment variable is set
    
    Environment Variables:
        ADMIN_EMAIL: Email for admin account (default: admin@thedraftclinic.com)
        ADMIN_PASSWORD: Password for admin account (required for creation)
    
    Returns:
        None
    """
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@thedraftclinic.com')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin and admin_password:
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='TheDraftClinic',
            is_admin=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
