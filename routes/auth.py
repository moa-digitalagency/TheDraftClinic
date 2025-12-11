"""
================================================================================
TheDraftClinic - Routes d'Authentification
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module gere l'authentification des utilisateurs:
- Connexion (login)
- Inscription (register)  
- Deconnexion (logout)

Securite:
- Protection CSRF sur tous les formulaires
- Limitation de taux sur les tentatives de connexion
- Validation des emails et mots de passe
- Hash des mots de passe avec Werkzeug
================================================================================
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import logging

from app import db
from models.user import User
from utils.forms import LoginForm, RegistrationForm
from utils.i18n import t

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gere la page de connexion des utilisateurs.
    """
    try:
        if current_user.is_authenticated:
            logger.debug(f"Utilisateur deja connecte: {current_user.email}")
            if current_user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('client.dashboard'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            email = form.email.data.lower().strip() if form.email.data else ''
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    logger.warning(f"Tentative de connexion sur compte desactive: {email}")
                    flash(t('auth.messages.login_required'), 'error')
                    return render_template('auth/login.html', form=form)
                
                login_user(user, remember=form.remember.data)
                logger.info(f"Connexion reussie: {email}")
                
                next_page = request.args.get('next')
                if user.is_admin:
                    return redirect(next_page or url_for('admin.dashboard'))
                return redirect(next_page or url_for('client.dashboard'))
            
            logger.warning(f"Echec de connexion pour: {email}")
            flash(t('auth.messages.login_error'), 'error')
        
        return render_template('auth/login.html', form=form)
        
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {e}")
        flash(t('auth.messages.login_error'), 'error')
        return render_template('auth/login.html', form=LoginForm())


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Gere la page d'inscription des nouveaux utilisateurs.
    """
    try:
        if current_user.is_authenticated:
            return redirect(url_for('client.dashboard'))
        
        form = RegistrationForm()
        
        if form.validate_on_submit():
            email = form.email.data.lower().strip() if form.email.data else ''
            existing_user = User.query.filter_by(email=email).first()
            
            if existing_user:
                logger.warning(f"Tentative d'inscription avec email existant: {email}")
                flash(t('auth.messages.email_exists'), 'error')
                return render_template('auth/register.html', form=form)
            
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
            
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"Nouveau compte cree: {email}")
            flash(t('auth.messages.register_success'), 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('auth/register.html', form=form)
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur lors de l'inscription: {e}")
        flash(t('auth.messages.register_error'), 'error')
        return render_template('auth/register.html', form=RegistrationForm())


@bp.route('/logout')
@login_required
def logout():
    """
    Deconnecte l'utilisateur et detruit sa session.
    """
    try:
        logger.info(f"Deconnexion: {current_user.email}")
        logout_user()
        flash(t('auth.messages.logout_success'), 'info')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        logger.error(f"Erreur lors de la deconnexion: {e}")
        return redirect(url_for('main.index'))
