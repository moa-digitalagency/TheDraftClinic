"""
================================================================================
TheDraftClinic - Service Administrateur
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module fournit les services administratifs, notamment la création
automatique du compte administrateur par défaut au démarrage.

Fonctions:
- create_default_admin: Crée le compte admin si les variables sont configurées
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

import os                                    # Accès aux variables d'environnement
import logging                               # Logging des actions
from flask import current_app                # Accès à la config de l'app
from app import db                           # Instance SQLAlchemy
from models.user import User                 # Modèle utilisateur

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


# ==============================================================================
# CRÉATION DU COMPTE ADMIN PAR DÉFAUT
# ==============================================================================

def create_default_admin():
    """
    Crée un compte administrateur par défaut si nécessaire.
    
    Cette fonction est appelée automatiquement au démarrage de l'application.
    Elle vérifie si un compte admin existe déjà et en crée un nouveau
    uniquement si les conditions suivantes sont remplies:
    
    1. Aucun admin avec l'email spécifié n'existe
    2. Le mot de passe admin est configuré dans les variables d'environnement
    
    Variables d'environnement utilisées:
        ADMIN_EMAIL: Email du compte admin
            - Défaut: admin@thedraftclinic.com
        ADMIN_PASSWORD: Mot de passe du compte admin
            - Requis pour la création du compte
    
    Returns:
        None
        
    Raises:
        Exception: En cas d'erreur lors de la création (loggée mais non propagée)
        
    Example:
        # Appelé automatiquement dans app.py
        with app.app_context():
            create_default_admin()
    
    Security Notes:
        - Le mot de passe n'est JAMAIS loggé
        - Utilisez des mots de passe forts en production
        - Changez le mot de passe par défaut après la première connexion
    """
    try:
        # Récupération de l'email admin depuis les secrets (OBLIGATOIRE)
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        # Vérification que les credentials sont configurés
        if not admin_email or not admin_password:
            logger.warning(
                "ADMIN_EMAIL et ADMIN_PASSWORD doivent être configurés dans les secrets. "
                "Le compte admin ne sera pas créé automatiquement."
            )
            return
        
        logger.info(f"Vérification du compte admin: {admin_email}")
        
        # Recherche d'un admin existant avec cet email
        admin = User.query.filter_by(email=admin_email).first()
        
        if admin:
            # Met à jour le mot de passe si différent
            if not admin.check_password(admin_password):
                admin.set_password(admin_password)
                db.session.commit()
                logger.info(f"Mot de passe admin mis à jour: {admin_email}")
            else:
                logger.info(f"Compte admin existant trouvé: {admin_email}")
            return
        
        # Vérifier si c'est le premier admin (sera super_admin)
        existing_admins = User.query.filter_by(is_admin=True).count()
        is_first_admin = existing_admins == 0
        
        # Création du nouveau compte admin
        logger.info(f"Création du compte admin: {admin_email}")
        
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='TheDraftClinic',
            is_admin=True,
            admin_role='super_admin' if is_first_admin else 'admin',
            account_active=True
        )
        
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        
        role_label = "super administrateur" if is_first_admin else "administrateur"
        logger.info(f"Compte {role_label} créé avec succès: {admin_email}")
        
    except Exception as e:
        # Log de l'erreur sans interrompre le démarrage de l'application
        logger.error(f"Erreur lors de la création du compte admin: {e}")
        # Rollback de la transaction en cas d'erreur
        db.session.rollback()
