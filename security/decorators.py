"""
================================================================================
TheDraftClinic - Décorateurs de Sécurité
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
================================================================================

Ce module contient les décorateurs utilisés pour la sécurité:
- admin_required: Vérifie que l'utilisateur est administrateur
- client_required: Vérifie que l'utilisateur est un client (non-admin)
- login_required_with_message: Version personnalisée de login_required
================================================================================
"""

from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user
import logging

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


def admin_required(f):
    """
    Décorateur qui vérifie que l'utilisateur connecté est administrateur.
    
    Ce décorateur doit être utilisé après @login_required pour s'assurer
    que l'utilisateur est d'abord authentifié, puis vérifié comme admin.
    
    Args:
        f: La fonction à décorer
        
    Returns:
        function: La fonction décorée qui redirige si l'utilisateur n'est pas admin
        
    Example:
        @bp.route('/admin/dashboard')
        @login_required
        @admin_required
        def admin_dashboard():
            return render_template('admin/dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérification si l'utilisateur est authentifié et est admin
        if not current_user.is_authenticated:
            logger.warning(f"Tentative d'accès admin non authentifié depuis {request.remote_addr}")
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_admin:
            logger.warning(f"Tentative d'accès admin refusée pour l'utilisateur {current_user.id}")
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function


def super_admin_required(f):
    """
    Décorateur qui vérifie que l'utilisateur connecté est super administrateur.
    
    Le super admin est le premier compte admin créé et peut gérer les autres admins.
    
    Args:
        f: La fonction à décorer
        
    Returns:
        function: La fonction décorée qui redirige si l'utilisateur n'est pas super admin
        
    Example:
        @bp.route('/admin/admins')
        @login_required
        @super_admin_required
        def manage_admins():
            return render_template('admin/admins.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            logger.warning(f"Tentative d'accès super admin non authentifié depuis {request.remote_addr}")
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_admin:
            logger.warning(f"Tentative d'accès super admin refusée pour l'utilisateur {current_user.id}")
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        
        if not current_user.is_super_admin:
            logger.warning(f"Tentative d'accès super admin refusée pour l'admin {current_user.id}")
            flash('Cette fonctionnalité est réservée au super administrateur.', 'error')
            return redirect(url_for('admin.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function


def client_required(f):
    """
    Décorateur qui vérifie que l'utilisateur connecté est un client (non-admin).
    
    Les administrateurs sont redirigés vers leur propre tableau de bord.
    
    Args:
        f: La fonction à décorer
        
    Returns:
        function: La fonction décorée qui redirige les admins
        
    Example:
        @bp.route('/client/dashboard')
        @login_required
        @client_required
        def client_dashboard():
            return render_template('client/dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si l'utilisateur est admin, rediriger vers le dashboard admin
        if current_user.is_admin:
            logger.info(f"Admin {current_user.id} redirigé du dashboard client vers admin")
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def login_required_with_message(message="Veuillez vous connecter.", category="info"):
    """
    Décorateur personnalisé de login_required avec message flash personnalisable.
    
    Args:
        message: Message à afficher à l'utilisateur
        category: Catégorie du message flash (info, warning, error, success)
        
    Returns:
        function: Le décorateur configuré
        
    Example:
        @login_required_with_message("Connexion requise pour cette action.", "warning")
        def protected_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(message, category)
                return redirect(url_for('auth.login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
