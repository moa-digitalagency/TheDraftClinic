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
        # Récupération de l'email admin depuis les variables d'environnement
        # Utilise une valeur par défaut si non spécifié
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@thedraftclinic.com')
        
        # Récupération du mot de passe admin
        # Aucune valeur par défaut pour des raisons de sécurité
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        # Log de l'information (sans le mot de passe!)
        logger.info(f"Vérification du compte admin: {admin_email}")
        
        # Recherche d'un admin existant avec cet email
        admin = User.query.filter_by(email=admin_email).first()
        
        # Si l'admin existe déjà, ne rien faire
        if admin:
            logger.info(f"Compte admin existant trouvé: {admin_email}")
            return
        
        # Si aucun mot de passe n'est configuré, ne pas créer le compte
        if not admin_password:
            logger.warning(
                "Variable ADMIN_PASSWORD non définie. "
                "Le compte admin ne sera pas créé automatiquement."
            )
            return
        
        # Création du nouveau compte admin
        logger.info(f"Création du compte admin: {admin_email}")
        
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='TheDraftClinic',
            is_admin=True,
            account_active=True
        )
        
        # Définition du mot de passe (hashé automatiquement)
        admin.set_password(admin_password)
        
        # Sauvegarde en base de données
        db.session.add(admin)
        db.session.commit()
        
        logger.info(f"Compte admin créé avec succès: {admin_email}")
        
    except Exception as e:
        # Log de l'erreur sans interrompre le démarrage de l'application
        logger.error(f"Erreur lors de la création du compte admin: {e}")
        # Rollback de la transaction en cas d'erreur
        db.session.rollback()
