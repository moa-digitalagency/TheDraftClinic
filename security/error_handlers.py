"""
================================================================================
TheDraftClinic - Gestionnaires d'Erreurs
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
================================================================================

Ce module contient les gestionnaires d'erreurs personnalisés pour l'application.
Il gère les erreurs HTTP courantes et les erreurs internes du serveur.
================================================================================
"""

from flask import render_template, request, jsonify
import logging
import traceback

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """
    Enregistre les gestionnaires d'erreurs personnalisés pour l'application.
    
    Cette fonction doit être appelée lors de l'initialisation de l'application
    pour activer les pages d'erreur personnalisées.
    
    Args:
        app: L'instance Flask de l'application
        
    Example:
        app = Flask(__name__)
        register_error_handlers(app)
    """
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """
        Gestionnaire pour les erreurs 400 (Requête invalide).
        
        Args:
            error: L'objet erreur Flask
            
        Returns:
            tuple: (template, code_status)
        """
        # Log de l'erreur avec les détails
        logger.warning(
            f"Erreur 400 - Requête invalide: "
            f"URL={request.url}, IP={request.remote_addr}, "
            f"Erreur={str(error)}"
        )
        
        # Retour d'une réponse JSON si c'est une API
        if request.is_json:
            return jsonify({
                'error': 'Requête invalide',
                'message': str(error),
                'code': 400
            }), 400
        
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """
        Gestionnaire pour les erreurs 401 (Non autorisé).
        
        Args:
            error: L'objet erreur Flask
            
        Returns:
            tuple: (template, code_status)
        """
        logger.warning(
            f"Erreur 401 - Non autorisé: "
            f"URL={request.url}, IP={request.remote_addr}"
        )
        
        if request.is_json:
            return jsonify({
                'error': 'Non autorisé',
                'message': 'Authentification requise',
                'code': 401
            }), 401
        
        return render_template('errors/401.html', error=error), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """
        Gestionnaire pour les erreurs 403 (Accès refusé).
        
        Args:
            error: L'objet erreur Flask
            
        Returns:
            tuple: (template, code_status)
        """
        logger.warning(
            f"Erreur 403 - Accès refusé: "
            f"URL={request.url}, IP={request.remote_addr}"
        )
        
        if request.is_json:
            return jsonify({
                'error': 'Accès refusé',
                'message': 'Vous n\'avez pas les droits nécessaires',
                'code': 403
            }), 403
        
        return render_template('errors/403.html', error=error), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        """
        Gestionnaire pour les erreurs 404 (Page non trouvée).
        
        Args:
            error: L'objet erreur Flask
            
        Returns:
            tuple: (template, code_status)
        """
        logger.info(
            f"Erreur 404 - Page non trouvée: "
            f"URL={request.url}, IP={request.remote_addr}"
        )
        
        if request.is_json:
            return jsonify({
                'error': 'Page non trouvée',
                'message': 'La ressource demandée n\'existe pas',
                'code': 404
            }), 404
        
        return render_template('errors/404.html', error=error), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """
        Gestionnaire pour les erreurs 500 (Erreur interne du serveur).
        
        Cette erreur est loggée avec le traceback complet pour le débogage.
        
        Args:
            error: L'objet erreur Flask
            
        Returns:
            tuple: (template, code_status)
        """
        # Log détaillé avec traceback pour le débogage
        logger.error(
            f"Erreur 500 - Erreur interne: "
            f"URL={request.url}, IP={request.remote_addr}, "
            f"Méthode={request.method}, "
            f"Erreur={str(error)}"
        )
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        if request.is_json:
            return jsonify({
                'error': 'Erreur interne du serveur',
                'message': 'Une erreur inattendue s\'est produite',
                'code': 500
            }), 500
        
        return render_template('errors/500.html', error=error), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """
        Gestionnaire pour toutes les exceptions non gérées.
        
        Capture toute exception Python et la traite comme une erreur 500.
        
        Args:
            error: L'exception Python
            
        Returns:
            tuple: (template, code_status)
        """
        # Log complet de l'exception
        logger.critical(
            f"Exception non gérée: {type(error).__name__}: {str(error)}"
        )
        logger.critical(f"Traceback complet: {traceback.format_exc()}")
        
        if request.is_json:
            return jsonify({
                'error': 'Erreur inattendue',
                'message': 'Une erreur inattendue s\'est produite',
                'code': 500
            }), 500
        
        return render_template('errors/500.html', error=error), 500
