"""
================================================================================
TheDraftClinic - Point d'Entrée de l'Application
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce fichier est le point d'entrée principal de l'application Flask.
Il utilise le pattern Factory pour créer l'instance de l'application.

Usage:
    # Développement avec Gunicorn (recommandé)
    uv run gunicorn --bind 0.0.0.0:5000 --reload main:app
    
    # Ou directement avec Python
    uv run python main.py
================================================================================
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# INITIALISATION DE LA BASE DE DONNÉES AU DÉMARRAGE
# ==============================================================================

def ensure_database_initialized():
    """
    S'assure que la base de données est initialisée avec toutes les tables
    et le compte admin configuré depuis les variables d'environnement.
    """
    from app import create_app, db
    from models.user import User
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        if not admin_email or not admin_password:
            print("WARNING: ADMIN_EMAIL and/or ADMIN_PASSWORD not configured in secrets.")
            print("Admin account will not be created. Configure them to enable admin access.")
        else:
            try:
                existing_admin = User.query.filter_by(email=admin_email).first()
                
                if existing_admin:
                    if not existing_admin.check_password(admin_password):
                        existing_admin.set_password(admin_password)
                        db.session.commit()
                        print(f"Admin password updated for: {admin_email}")
                else:
                    admin = User(
                        email=admin_email,
                        first_name='Admin',
                        last_name='TheDraftClinic',
                        is_admin=True,
                        account_active=True
                    )
                    admin.set_password(admin_password)
                    db.session.add(admin)
                    db.session.commit()
                    print(f"Admin user created: {admin_email}")
            except Exception as e:
                print(f"Warning: Could not create/update admin: {e}")
    
    return app

# ==============================================================================
# IMPORTATION ET CRÉATION DE L'APPLICATION
# ==============================================================================

app = ensure_database_initialized()


# ==============================================================================
# EXÉCUTION EN MODE DÉVELOPPEMENT
# ==============================================================================

if __name__ == '__main__':
    """
    Point d'entrée pour l'exécution directe avec Python.
    En production, utilisez Gunicorn au lieu de ce mode de développement.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)
