"""
================================================================================
TheDraftClinic - Routes d'Authentification
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module gère l'authentification des utilisateurs:
- Connexion (login)
- Inscription (register)  
- Déconnexion (logout)

Sécurité:
- Protection CSRF sur tous les formulaires
- Limitation de taux sur les tentatives de connexion
- Validation des emails et mots de passe
- Hash des mots de passe avec Werkzeug
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import logging

from app import db
from models.user import User
from utils.forms import LoginForm, RegistrationForm

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)

# Création du blueprint d'authentification
bp = Blueprint('auth', __name__)


# ==============================================================================
# ROUTE DE CONNEXION
# ==============================================================================

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gère la page de connexion des utilisateurs.
    
    GET: Affiche le formulaire de connexion
    POST: Traite la tentative de connexion
    
    Workflow:
    1. Vérifie si l'utilisateur est déjà connecté
    2. Valide le formulaire
    3. Recherche l'utilisateur par email
    4. Vérifie le mot de passe
    5. Crée la session utilisateur
    6. Redirige vers le dashboard approprié
    
    Returns:
        - GET: Template de connexion
        - POST (succès): Redirection vers le dashboard
        - POST (échec): Template avec message d'erreur
    """
    try:
        # Si l'utilisateur est déjà connecté, rediriger vers son dashboard
        if current_user.is_authenticated:
            logger.debug(f"Utilisateur déjà connecté: {current_user.email}")
            if current_user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('client.dashboard'))
        
        # Création du formulaire de connexion
        form = LoginForm()
        
        # Traitement du formulaire soumis
        if form.validate_on_submit():
            # Recherche de l'utilisateur par email (insensible à la casse)
            email = form.email.data.lower().strip() if form.email.data else ''
            user = User.query.filter_by(email=email).first()
            
            # Vérification du mot de passe
            if user and user.check_password(form.password.data):
                # Vérification que le compte est actif
                if not user.is_active:
                    logger.warning(f"Tentative de connexion sur compte désactivé: {email}")
                    flash('Votre compte a été désactivé. Contactez l\'administrateur.', 'error')
                    return render_template('auth/login.html', form=form)
                
                # Connexion réussie
                login_user(user, remember=form.remember.data)
                logger.info(f"Connexion réussie: {email}")
                
                # Redirection vers la page demandée ou le dashboard
                next_page = request.args.get('next')
                if user.is_admin:
                    return redirect(next_page or url_for('admin.dashboard'))
                return redirect(next_page or url_for('client.dashboard'))
            
            # Échec de connexion
            logger.warning(f"Échec de connexion pour: {email}")
            flash('Email ou mot de passe incorrect.', 'error')
        
        return render_template('auth/login.html', form=form)
        
    except Exception as e:
        # Log de l'erreur
        logger.error(f"Erreur lors de la connexion: {e}")
        flash('Une erreur est survenue. Veuillez réessayer.', 'error')
        return render_template('auth/login.html', form=LoginForm())


# ==============================================================================
# ROUTE D'INSCRIPTION
# ==============================================================================

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Gère la page d'inscription des nouveaux utilisateurs.
    
    GET: Affiche le formulaire d'inscription
    POST: Traite la création du nouveau compte
    
    Workflow:
    1. Vérifie si l'utilisateur est déjà connecté
    2. Valide le formulaire
    3. Vérifie que l'email n'existe pas déjà
    4. Crée le nouvel utilisateur
    5. Hash le mot de passe
    6. Sauvegarde en base de données
    7. Redirige vers la page de connexion
    
    Returns:
        - GET: Template d'inscription
        - POST (succès): Redirection vers login
        - POST (échec): Template avec message d'erreur
    """
    try:
        # Si l'utilisateur est déjà connecté, rediriger vers son dashboard
        if current_user.is_authenticated:
            return redirect(url_for('client.dashboard'))
        
        # Création du formulaire d'inscription
        form = RegistrationForm()
        
        # Traitement du formulaire soumis
        if form.validate_on_submit():
            # Vérification si l'email existe déjà
            email = form.email.data.lower().strip() if form.email.data else ''
            existing_user = User.query.filter_by(email=email).first()
            
            if existing_user:
                logger.warning(f"Tentative d'inscription avec email existant: {email}")
                flash('Un compte avec cet email existe déjà.', 'error')
                return render_template('auth/register.html', form=form)
            
            # Création du nouvel utilisateur
            user = User(
                email=email,
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                phone=form.phone.data.strip() if form.phone.data else None,
                institution=form.institution.data.strip() if form.institution.data else None,
                academic_level=form.academic_level.data if form.academic_level.data else None,
                field_of_study=form.field_of_study.data.strip() if form.field_of_study.data else None,
                is_admin=False,
                account_active=True
            )
            
            # Hash du mot de passe
            user.set_password(form.password.data)
            
            # Sauvegarde en base de données
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"Nouveau compte créé: {email}")
            flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('auth/register.html', form=form)
        
    except Exception as e:
        # Rollback en cas d'erreur
        db.session.rollback()
        logger.error(f"Erreur lors de l'inscription: {e}")
        flash('Une erreur est survenue lors de la création du compte.', 'error')
        return render_template('auth/register.html', form=RegistrationForm())


# ==============================================================================
# ROUTE DE DÉCONNEXION
# ==============================================================================

@bp.route('/logout')
@login_required
def logout():
    """
    Déconnecte l'utilisateur et détruit sa session.
    
    Requires:
        Utilisateur connecté (login_required)
    
    Returns:
        Redirection vers la page d'accueil
    """
    try:
        # Log de la déconnexion
        logger.info(f"Déconnexion: {current_user.email}")
        
        # Déconnexion de l'utilisateur
        logout_user()
        
        flash('Vous avez été déconnecté.', 'info')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {e}")
        return redirect(url_for('main.index'))
