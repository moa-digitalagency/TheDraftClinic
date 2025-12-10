import os
from app import db
from app.models.user import User


def create_default_admin():
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@theraftclinic.com')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin and admin_password:
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='TheraftClinic',
            is_admin=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
