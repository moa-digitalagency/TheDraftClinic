"""
================================================================================
TheDraftClinic - Routes Principales (Pages Publiques)
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module gère les pages publiques accessibles sans authentification:
- Page d'accueil (landing page)
- Page des services
- Page à propos
- Page de contact

Note:
    Ces routes n'ont pas besoin d'authentification car elles présentent
    l'information publique du site.
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from flask import Blueprint, render_template, abort
import logging

from models.request import ServiceRequest
from models.page import Page

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)

# Création du blueprint principal
bp = Blueprint('main', __name__)


# ==============================================================================
# PAGE D'ACCUEIL
# ==============================================================================

@bp.route('/')
def index():
    """
    Affiche la page d'accueil (landing page) du site.
    
    Cette page présente:
    - Les services offerts par TheDraftClinic
    - Le processus de travail
    - Les avantages de la plateforme
    - Les appels à l'action (inscription, contact)
    
    Returns:
        Template landing.html avec la liste des services
    """
    try:
        # Récupération des types de services disponibles
        services = ServiceRequest.SERVICE_TYPES
        
        return render_template('landing.html', services=services)
        
    except Exception as e:
        logger.error(f"Erreur sur la page d'accueil: {e}")
        # En cas d'erreur, afficher la page sans les services
        return render_template('landing.html', services=[])


# ==============================================================================
# PAGE DES SERVICES
# ==============================================================================

@bp.route('/services')
def services():
    """
    Affiche la page détaillée des services proposés.
    
    Liste tous les types de services avec leurs descriptions,
    permettant aux visiteurs de comprendre l'offre complète.
    
    Returns:
        Template services.html avec la liste des services
    """
    try:
        # Récupération des types de services
        services_list = ServiceRequest.SERVICE_TYPES
        
        return render_template('services.html', services=services_list)
        
    except Exception as e:
        logger.error(f"Erreur sur la page des services: {e}")
        return render_template('services.html', services=[])


# ==============================================================================
# PAGE À PROPOS
# ==============================================================================

@bp.route('/about')
def about():
    """
    Affiche la page "À propos" de TheDraftClinic.
    
    Présente:
    - L'histoire et la mission de l'entreprise
    - L'équipe
    - Les valeurs
    
    Returns:
        Template about.html
    """
    try:
        return render_template('about.html')
        
    except Exception as e:
        logger.error(f"Erreur sur la page À propos: {e}")
        # Retourner une page simple en cas d'erreur
        return render_template('about.html')


# ==============================================================================
# PAGE DE CONTACT
# ==============================================================================

@bp.route('/contact')
def contact():
    """
    Affiche la page de contact.
    
    Présente les informations de contact et éventuellement
    un formulaire pour envoyer un message.
    
    Returns:
        Template contact.html
    """
    try:
        return render_template('contact.html')
        
    except Exception as e:
        logger.error(f"Erreur sur la page Contact: {e}")
        return render_template('contact.html')


# ==============================================================================
# CONFIGURATION DU CACHE (ANTI-CACHE)
# ==============================================================================

@bp.route('/page/<slug>')
def view_page(slug):
    """
    Affiche une page dynamique par son slug.
    
    Args:
        slug: L'identifiant unique de la page
        
    Returns:
        Template page.html avec le contenu de la page
    """
    try:
        page = Page.query.filter_by(slug=slug, is_published=True).first()
        
        if not page:
            abort(404)
        
        return render_template('page.html', page=page)
        
    except Exception as e:
        logger.error(f"Erreur affichage page {slug}: {e}")
        abort(404)


@bp.after_request
def add_header(response):
    """
    Ajoute des en-têtes HTTP pour désactiver le cache.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response
