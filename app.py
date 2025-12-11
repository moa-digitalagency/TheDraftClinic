"""
================================================================================
TheDraftClinic - Configuration et Initialisation de l'Application Flask
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module est le coeur de l'application. Il contient:
- La configuration de Flask et ses extensions
- L'initialisation de la base de données SQLAlchemy
- La configuration de Flask-Login pour l'authentification
- La protection CSRF avec Flask-WTF
- Le système de logging pour le suivi des erreurs
- L'enregistrement des blueprints (routes)
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

import os                                    # Accès aux variables d'environnement
import logging                               # Système de logging Python
from logging.handlers import RotatingFileHandler  # Rotation des fichiers de log
from flask import Flask                      # Framework web Flask
from flask_sqlalchemy import SQLAlchemy      # ORM pour la base de données
from flask_login import LoginManager         # Gestion de l'authentification
from flask_wtf.csrf import CSRFProtect       # Protection CSRF
from sqlalchemy.orm import DeclarativeBase   # Base pour les modèles SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix  # Fix pour les proxys inverses


# ==============================================================================
# CONFIGURATION DE LA BASE DE DONNÉES
# ==============================================================================

class Base(DeclarativeBase):
    """
    Classe de base pour tous les modèles SQLAlchemy.
    
    Cette classe sert de fondation pour la déclaration des modèles
    de la base de données en utilisant le style déclaratif de SQLAlchemy.
    """
    pass


# ==============================================================================
# INITIALISATION DES EXTENSIONS
# ==============================================================================

# Instance SQLAlchemy pour la gestion de la base de données
# Utilise notre classe Base personnalisée comme modèle de base
db = SQLAlchemy(model_class=Base)

# Instance LoginManager pour la gestion de l'authentification
# Gère les sessions utilisateur et la protection des routes
login_manager = LoginManager()

# Instance CSRFProtect pour la protection contre les attaques CSRF
# Ajoute automatiquement des tokens CSRF aux formulaires
csrf = CSRFProtect()


# ==============================================================================
# CONFIGURATION DU LOGGING
# ==============================================================================

def configure_logging(app):
    """
    Configure le système de logging de l'application.
    
    Cette fonction met en place:
    - Un handler pour la console (développement)
    - Un handler pour les fichiers (production)
    - Un format de log standardisé avec timestamp et niveau
    
    Args:
        app: L'instance Flask de l'application
        
    Note:
        Les fichiers de log sont stockés dans le dossier 'logs/'
        avec rotation automatique à 10MB et 10 fichiers maximum.
    """
    # Configuration du niveau de log de base
    log_level = logging.DEBUG if app.debug else logging.INFO
    
    # Format du log: timestamp - niveau - module - message
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configuration du logger racine
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Handler pour la console (toujours actif)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Création du dossier logs si nécessaire
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Handler pour les fichiers avec rotation
    # Rotation à 10MB, garde 10 fichiers d'historique
    file_handler = RotatingFileHandler(
        'logs/thedraftclinic.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Handler spécifique pour les erreurs
    error_handler = RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)
    
    # Log de démarrage
    app.logger.info('Application TheDraftClinic démarrée')


# ==============================================================================
# FONCTION DE CRÉATION DE L'APPLICATION (FACTORY PATTERN)
# ==============================================================================

def create_app():
    """
    Factory function pour créer et configurer l'application Flask.
    
    Cette fonction utilise le pattern Factory pour permettre:
    - La création de plusieurs instances de l'application
    - Des configurations différentes pour les tests
    - Une initialisation propre des extensions
    
    Returns:
        Flask: L'instance configurée de l'application
        
    Configuration:
        - SECRET_KEY: Depuis SESSION_SECRET (variable d'environnement)
        - DATABASE_URL: URL de connexion PostgreSQL
        - MAX_CONTENT_LENGTH: 50MB maximum pour les uploads
        - UPLOAD_FOLDER: Dossier pour les fichiers uploadés
    """
    # Création de l'instance Flask
    app = Flask(__name__)
    
    # --------------------------------------------------------------------------
    # CONFIGURATION DE BASE
    # --------------------------------------------------------------------------
    
    # Clé secrète pour les sessions (OBLIGATOIRE en production)
    # Récupérée depuis les variables d'environnement pour la sécurité
    app.config['SECRET_KEY'] = os.environ.get(
        'SESSION_SECRET', 
        'thedraftclinic-dev-key-change-in-production'
    )
    
    # Fix pour les proxys inverses (Replit, Nginx, etc.)
    # Permet d'obtenir les bonnes URLs avec HTTPS
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # --------------------------------------------------------------------------
    # CONFIGURATION DE LA BASE DE DONNÉES
    # --------------------------------------------------------------------------
    
    # URL de connexion à PostgreSQL depuis les variables d'environnement
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    
    # Désactivation du suivi des modifications (économie de mémoire)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Options du pool de connexions pour la stabilité
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,      # Recyclage des connexions après 5 minutes
        "pool_pre_ping": True,    # Vérification de la connexion avant utilisation
    }
    
    # --------------------------------------------------------------------------
    # CONFIGURATION DES UPLOADS
    # --------------------------------------------------------------------------
    
    # Taille maximale des fichiers uploadés (50 MB)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    
    # Dossier de stockage des fichiers uploadés
    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'static', 
        'uploads'
    )
    
    # Création du dossier uploads s'il n'existe pas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # --------------------------------------------------------------------------
    # CONFIGURATION DES IDENTIFIANTS ADMIN PAR DÉFAUT
    # --------------------------------------------------------------------------
    
    # Email de l'administrateur (depuis variable d'environnement)
    app.config['ADMIN_EMAIL'] = os.environ.get(
        'ADMIN_EMAIL', 
        'admin@thedraftclinic.com'
    )
    
    # Mot de passe admin (depuis variable d'environnement, requis pour création)
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD')
    
    # --------------------------------------------------------------------------
    # INITIALISATION DES EXTENSIONS
    # --------------------------------------------------------------------------
    
    # Initialisation de SQLAlchemy avec l'application
    db.init_app(app)
    
    # Initialisation de Flask-Login
    login_manager.init_app(app)
    
    # Initialisation de la protection CSRF
    csrf.init_app(app)
    
    # --------------------------------------------------------------------------
    # CONFIGURATION DE FLASK-LOGIN
    # --------------------------------------------------------------------------
    
    # Route vers laquelle rediriger les utilisateurs non connectés
    login_manager.login_view = 'auth.login'
    
    # Message affiché lors d'une tentative d'accès non autorisée
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    
    # Catégorie du message flash (pour le style CSS)
    login_manager.login_message_category = 'info'
    
    # --------------------------------------------------------------------------
    # CHARGEMENT DE L'UTILISATEUR POUR FLASK-LOGIN
    # --------------------------------------------------------------------------
    
    # Import du modèle User (doit être fait après db.init_app)
    from models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Fonction callback pour recharger l'utilisateur depuis la session.
        
        Flask-Login appelle cette fonction à chaque requête pour récupérer
        l'objet User correspondant à l'ID stocké en session.
        
        Args:
            user_id (str): L'ID de l'utilisateur stocké en session
            
        Returns:
            User: L'objet utilisateur ou None si non trouvé
        """
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            app.logger.error(f"Erreur lors du chargement de l'utilisateur {user_id}: {e}")
            return None
    
    # --------------------------------------------------------------------------
    # ENREGISTREMENT DES BLUEPRINTS (ROUTES)
    # --------------------------------------------------------------------------
    
    # Import des blueprints depuis le dossier routes
    from routes import auth, client, admin, main
    from routes import admin_settings
    
    # Blueprint principal (pages publiques: accueil, services, etc.)
    app.register_blueprint(main.bp)
    
    # Blueprint d'authentification (login, register, logout)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    
    # Blueprint client (dashboard client, demandes, profil)
    app.register_blueprint(client.bp, url_prefix='/client')
    
    # Blueprint administrateur (gestion des demandes, utilisateurs)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    
    # Blueprint paramètres admin (settings, pages, stats)
    app.register_blueprint(admin_settings.bp, url_prefix='/admin')
    
    # --------------------------------------------------------------------------
    # ENREGISTREMENT DES GESTIONNAIRES D'ERREURS
    # --------------------------------------------------------------------------
    
    from security.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # --------------------------------------------------------------------------
    # INITIALISATION DU SYSTEME DE TRADUCTION (i18n)
    # --------------------------------------------------------------------------
    
    from utils.i18n import init_i18n
    init_i18n(app)
    
    # --------------------------------------------------------------------------
    # CONTEXT PROCESSORS (Variables globales pour templates)
    # --------------------------------------------------------------------------
    
    @app.context_processor
    def inject_site_settings():
        """Injecte les paramètres du site dans tous les templates."""
        try:
            from models.site_settings import SiteSettings
            from models.page import Page
            settings = SiteSettings.get_settings()
            footer_pages = Page.get_footer_pages()
            return {
                'site_settings': settings,
                'footer_pages': footer_pages
            }
        except Exception:
            return {'site_settings': None, 'footer_pages': []}
    
    # --------------------------------------------------------------------------
    # INITIALISATION DE LA BASE DE DONNÉES ET ADMIN PAR DÉFAUT
    # --------------------------------------------------------------------------
    
    with app.app_context():
        # Création de toutes les tables définies dans les modèles
        db.create_all()
        
        # Création du compte administrateur par défaut si nécessaire
        from services.admin_service import create_default_admin
        create_default_admin()
    
    # --------------------------------------------------------------------------
    # CONFIGURATION DU LOGGING
    # --------------------------------------------------------------------------
    
    configure_logging(app)
    
    # Retour de l'application configurée
    return app
