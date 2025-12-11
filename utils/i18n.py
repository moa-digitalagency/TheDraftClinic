"""
================================================================================
TheDraftClinic - Module de gestion des langues (i18n)
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module gère l'internationalisation de l'application.
Fonctionnalités:
- Chargement des fichiers de langue JSON
- Fonction de traduction avec clés imbriquées
- Gestion de la langue courante via session
- Injection dans les templates Jinja2
================================================================================
"""

import os
import json
import glob
from flask import session, request, g
from functools import wraps

LANGUAGES = []
DEFAULT_LANGUAGE = 'en'
TRANSLATIONS = {}


def discover_languages():
    """
    Decouvre dynamiquement les fichiers de langue disponibles.
    Retourne une liste de codes de langue (ex: ['fr', 'en', 'es']).
    """
    global LANGUAGES
    lang_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lang')
    lang_files = glob.glob(os.path.join(lang_dir, '*.json'))
    LANGUAGES = [os.path.splitext(os.path.basename(f))[0] for f in lang_files]
    if 'fr' in LANGUAGES and 'en' in LANGUAGES:
        LANGUAGES = ['fr', 'en'] + [l for l in LANGUAGES if l not in ['fr', 'en']]
    return LANGUAGES


def load_translations():
    """
    Charge tous les fichiers de traduction JSON depuis le dossier lang/.
    Decouvre automatiquement les langues disponibles.
    Cette fonction doit etre appelee au demarrage de l'application.
    """
    global TRANSLATIONS
    discover_languages()
    
    lang_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lang')
    
    for lang in LANGUAGES:
        lang_file = os.path.join(lang_dir, f'{lang}.json')
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    TRANSLATIONS[lang] = json.load(f)
            except json.JSONDecodeError:
                TRANSLATIONS[lang] = {}
        else:
            TRANSLATIONS[lang] = {}


def reload_translations():
    """
    Recharge les traductions depuis les fichiers.
    Utile apres modification des fichiers de langue via l'admin.
    Decouvre egalement les nouvelles langues ajoutees.
    """
    load_translations()


def get_available_languages():
    """
    Retourne la liste des langues disponibles.
    Utile pour les templates.
    """
    if not LANGUAGES:
        discover_languages()
    return LANGUAGES


def get_locale():
    """
    Recupere la langue courante.
    Ordre de priorite:
    1. Session utilisateur
    2. Parametre URL (?lang=xx)
    3. Preference navigateur (FR = fr, autres = en)
    4. Langue par defaut (en pour non-francophones)
    """
    available = get_available_languages()
    
    if 'lang' in session and session['lang'] in available:
        return session['lang']
    
    if request and 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in available:
            session['lang'] = lang
            return lang
    
    if request and request.accept_languages:
        for lang_code, quality in request.accept_languages:
            if lang_code.lower().startswith('fr') and 'fr' in available:
                session['lang'] = 'fr'
                return 'fr'
        if 'en' in available:
            session['lang'] = 'en'
            return 'en'
    
    return DEFAULT_LANGUAGE if DEFAULT_LANGUAGE in available else (available[0] if available else 'en')


def set_locale(lang):
    """
    Definit la langue courante dans la session.
    
    Args:
        lang: Code de langue (ex: 'fr', 'en', 'es')
    """
    available = get_available_languages()
    if lang in available:
        session['lang'] = lang
        return True
    return False


def t(key, **kwargs):
    """
    Fonction de traduction principale.
    
    Args:
        key: Cle de traduction (ex: 'auth.login.title')
        **kwargs: Variables a substituer dans le texte
        
    Returns:
        str: Texte traduit ou la cle si non trouve
        
    Example:
        t('auth.login.title') -> 'Connexion'
        t('common.welcome', name='Jean') -> 'Bienvenue Jean'
    """
    lang = get_locale()
    
    if lang not in TRANSLATIONS:
        lang = DEFAULT_LANGUAGE
    
    translations = TRANSLATIONS.get(lang, {})
    
    keys = key.split('.')
    value = translations
    
    try:
        for k in keys:
            value = value[k]
    except (KeyError, TypeError):
        fallback = TRANSLATIONS.get(DEFAULT_LANGUAGE, {})
        try:
            value = fallback
            for k in keys:
                value = value[k]
        except (KeyError, TypeError):
            return key
    
    if isinstance(value, str) and kwargs:
        try:
            value = value.format(**kwargs)
        except KeyError:
            pass
    
    return value


def get_translations():
    """
    Retourne toutes les traductions pour la langue courante.
    Utile pour l'injection dans JavaScript.
    """
    lang = get_locale()
    return TRANSLATIONS.get(lang, TRANSLATIONS.get(DEFAULT_LANGUAGE, {}))


def init_i18n(app):
    """
    Initialise le systeme i18n avec l'application Flask.
    
    Args:
        app: Instance Flask
    """
    load_translations()
    
    @app.before_request
    def before_request():
        g.lang = get_locale()
    
    @app.context_processor
    def inject_i18n():
        """Injecte les fonctions de traduction dans tous les templates."""
        return {
            't': t,
            'get_locale': get_locale,
            'languages': LANGUAGES,
            'current_lang': get_locale()
        }
    
    @app.template_filter('translate')
    def translate_filter(key, **kwargs):
        """Filtre Jinja2 pour la traduction."""
        return t(key, **kwargs)
