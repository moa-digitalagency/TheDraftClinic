"""
================================================================================
TheDraftClinic - Modèle Utilisateur
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle User pour l'authentification et la gestion des 
utilisateurs. Il inclut les champs pour les informations personnelles, 
les détails académiques et le statut administrateur.

Relations:
- Un utilisateur peut avoir plusieurs demandes de service (ServiceRequest)
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from app import db                           # Instance SQLAlchemy
from flask_login import UserMixin            # Mixin pour Flask-Login
from werkzeug.security import (              # Fonctions de hachage de mot de passe
    generate_password_hash, 
    check_password_hash
)
from datetime import datetime                # Gestion des dates
import logging                               # Logging des erreurs

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


# ==============================================================================
# MODÈLE UTILISATEUR
# ==============================================================================

class User(UserMixin, db.Model):
    """
    Modèle représentant un utilisateur de l'application.
    
    Ce modèle gère à la fois les clients (chercheurs/doctorants) et les 
    administrateurs. La distinction se fait via le champ is_admin.
    
    Hérite de:
        UserMixin: Fournit les méthodes requises par Flask-Login
            - is_authenticated: Retourne True si l'utilisateur est connecté
            - is_active: Retourne True si le compte est actif
            - is_anonymous: Retourne True pour les utilisateurs anonymes
            - get_id: Retourne l'identifiant unique de l'utilisateur
        db.Model: Classe de base SQLAlchemy pour les modèles
    
    Attributes:
        id (int): Clé primaire auto-incrémentée
        email (str): Adresse email unique (utilisée pour la connexion)
        password_hash (str): Hash du mot de passe (256 caractères max)
        first_name (str): Prénom de l'utilisateur
        last_name (str): Nom de famille de l'utilisateur
        phone (str): Numéro de téléphone (optionnel)
        institution (str): Établissement académique (optionnel)
        academic_level (str): Niveau d'études (licence, master, doctorat, etc.)
        field_of_study (str): Domaine de recherche (optionnel)
        is_admin (bool): True si l'utilisateur est administrateur
        account_active (bool): True si le compte est actif (non désactivé)
        created_at (datetime): Date de création du compte
        updated_at (datetime): Date de dernière modification
    
    Relationships:
        requests: Relation one-to-many vers ServiceRequest
    """
    
    # Nom de la table dans la base de données
    __tablename__ = 'users'
    
    # --------------------------------------------------------------------------
    # COLONNES DE LA TABLE
    # --------------------------------------------------------------------------
    
    # Clé primaire
    id = db.Column(
        db.Integer, 
        primary_key=True,
        doc="Identifiant unique de l'utilisateur"
    )
    
    # Informations de connexion
    email = db.Column(
        db.String(120), 
        unique=True,          # Pas de doublons
        nullable=False,       # Obligatoire
        index=True,           # Index pour recherche rapide
        doc="Adresse email unique pour la connexion"
    )
    
    password_hash = db.Column(
        db.String(256), 
        nullable=False,
        doc="Hash du mot de passe (ne jamais stocker en clair)"
    )
    
    # Informations personnelles
    first_name = db.Column(
        db.String(50), 
        nullable=False,
        doc="Prénom de l'utilisateur"
    )
    
    last_name = db.Column(
        db.String(50), 
        nullable=False,
        doc="Nom de famille de l'utilisateur"
    )
    
    phone = db.Column(
        db.String(20),
        doc="Numéro de téléphone (optionnel)"
    )
    
    # Informations académiques
    institution = db.Column(
        db.String(200),
        doc="Nom de l'établissement académique"
    )
    
    academic_level = db.Column(
        db.String(50),
        doc="Niveau académique (licence, master, doctorat, etc.)"
    )
    
    field_of_study = db.Column(
        db.String(100),
        doc="Domaine d'étude ou de recherche"
    )
    
    # Statuts et permissions
    is_admin = db.Column(
        db.Boolean, 
        default=False,
        doc="True si l'utilisateur est administrateur"
    )
    
    # Rôle admin : 'super_admin' (premier compte), 'admin' (autres admins), None (utilisateur normal)
    admin_role = db.Column(
        db.String(20),
        nullable=True,
        default=None,
        doc="Rôle admin: 'super_admin' ou 'admin'. None pour les utilisateurs normaux"
    )
    
    # Note: Renommé de is_active pour éviter conflit avec UserMixin
    account_active = db.Column(
        db.Boolean, 
        default=True,
        doc="True si le compte est actif (non suspendu)"
    )
    
    # Timestamps
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        doc="Date et heure de création du compte"
    )
    
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        doc="Date et heure de dernière modification"
    )
    
    # --------------------------------------------------------------------------
    # RELATIONS
    # --------------------------------------------------------------------------
    
    # Relation vers les demandes de service de l'utilisateur
    requests = db.relationship(
        'ServiceRequest',         # Modèle cible
        backref='user',           # Référence inverse depuis ServiceRequest
        lazy='dynamic',           # Chargement paresseux (query)
        doc="Demandes de service soumises par cet utilisateur"
    )
    
    # --------------------------------------------------------------------------
    # MÉTHODES DE GESTION DU MOT DE PASSE
    # --------------------------------------------------------------------------
    
    def set_password(self, password):
        """
        Hash et stocke le mot de passe de l'utilisateur.
        
        Utilise Werkzeug pour générer un hash sécurisé du mot de passe.
        Le hash est stocké dans password_hash, jamais le mot de passe en clair.
        
        Args:
            password (str): Le mot de passe en clair à hasher
            
        Note:
            Werkzeug utilise par défaut pbkdf2:sha256 avec un salt aléatoire.
            Ne pas spécifier la méthode pour utiliser la valeur par défaut.
        """
        try:
            self.password_hash = generate_password_hash(password)
            logger.debug(f"Mot de passe mis à jour pour l'utilisateur {self.email}")
        except Exception as e:
            logger.error(f"Erreur lors du hachage du mot de passe: {e}")
            raise
    
    def check_password(self, password):
        """
        Vérifie si le mot de passe fourni correspond au hash stocké.
        
        Args:
            password (str): Le mot de passe en clair à vérifier
            
        Returns:
            bool: True si le mot de passe est correct, False sinon
            
        Note:
            Cette méthode ne log jamais le mot de passe pour des raisons de sécurité.
        """
        try:
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du mot de passe: {e}")
            return False
    
    # --------------------------------------------------------------------------
    # PROPRIÉTÉS
    # --------------------------------------------------------------------------
    
    @property
    def full_name(self):
        """
        Retourne le nom complet de l'utilisateur.
        
        Returns:
            str: Prénom et nom séparés par un espace
            
        Example:
            >>> user.full_name
            "Jean Dupont"
        """
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self):
        """
        Propriété requise par Flask-Login pour vérifier si le compte est actif.
        
        Surcharge de UserMixin.is_active pour utiliser notre champ account_active.
        
        Returns:
            bool: True si le compte est actif et peut se connecter
        """
        return self.account_active
    
    @property
    def is_super_admin(self):
        """
        Vérifie si l'utilisateur est un super administrateur.
        
        Le super admin est le premier compte admin créé et a tous les droits,
        y compris la gestion des autres administrateurs.
        
        Returns:
            bool: True si l'utilisateur est super admin
        """
        return self.is_admin and self.admin_role == 'super_admin'
    
    def can_manage_admins(self):
        """
        Vérifie si l'utilisateur peut gérer les autres administrateurs.
        
        Seul le super admin peut ajouter/modifier/supprimer des admins.
        
        Returns:
            bool: True si l'utilisateur peut gérer les admins
        """
        return self.is_super_admin
    
    # --------------------------------------------------------------------------
    # MÉTHODES SPÉCIALES
    # --------------------------------------------------------------------------
    
    def __repr__(self):
        """
        Représentation string de l'utilisateur pour le débogage.
        
        Returns:
            str: Représentation formatée de l'utilisateur
        """
        return f'<User {self.email}>'
