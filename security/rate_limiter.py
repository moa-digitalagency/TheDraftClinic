"""
================================================================================
TheDraftClinic - Limiteur de Taux (Rate Limiter)
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
================================================================================

Ce module implémente un système de limitation de taux pour prévenir:
- Les attaques par force brute sur les formulaires de connexion
- Les abus d'API
- Le spam de formulaires
================================================================================
"""

import time
from collections import defaultdict
from functools import wraps
from flask import request, jsonify, flash, redirect, url_for
import logging

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Classe pour gérer la limitation de taux des requêtes.
    
    Cette classe utilise un algorithme de fenêtre glissante pour
    limiter le nombre de requêtes par IP sur une période donnée.
    
    Attributes:
        requests (dict): Dictionnaire stockant les timestamps des requêtes par IP
        max_requests (int): Nombre maximum de requêtes autorisées
        window_seconds (int): Fenêtre de temps en secondes
        
    Example:
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        
        @limiter.limit
        def login():
            pass
    """
    
    def __init__(self, max_requests=10, window_seconds=60):
        """
        Initialise le limiteur de taux.
        
        Args:
            max_requests (int): Nombre maximum de requêtes dans la fenêtre
            window_seconds (int): Durée de la fenêtre en secondes
        """
        # Dictionnaire pour stocker les timestamps par IP
        self.requests = defaultdict(list)
        # Nombre maximum de requêtes autorisées
        self.max_requests = max_requests
        # Fenêtre de temps en secondes
        self.window_seconds = window_seconds
    
    def _cleanup_old_requests(self, ip_address):
        """
        Nettoie les anciennes requêtes hors de la fenêtre de temps.
        
        Args:
            ip_address (str): L'adresse IP à nettoyer
        """
        # Temps actuel
        current_time = time.time()
        # Timestamp limite (début de la fenêtre)
        cutoff_time = current_time - self.window_seconds
        
        # Conservation uniquement des requêtes dans la fenêtre
        self.requests[ip_address] = [
            timestamp for timestamp in self.requests[ip_address]
            if timestamp > cutoff_time
        ]
    
    def is_allowed(self, ip_address):
        """
        Vérifie si une nouvelle requête est autorisée pour cette IP.
        
        Args:
            ip_address (str): L'adresse IP à vérifier
            
        Returns:
            bool: True si la requête est autorisée, False sinon
        """
        # Nettoyage des anciennes requêtes
        self._cleanup_old_requests(ip_address)
        
        # Vérification du nombre de requêtes
        if len(self.requests[ip_address]) >= self.max_requests:
            logger.warning(f"Rate limit atteint pour IP: {ip_address}")
            return False
        
        return True
    
    def record_request(self, ip_address):
        """
        Enregistre une nouvelle requête pour cette IP.
        
        Args:
            ip_address (str): L'adresse IP à enregistrer
        """
        self.requests[ip_address].append(time.time())
    
    def get_remaining_requests(self, ip_address):
        """
        Retourne le nombre de requêtes restantes pour cette IP.
        
        Args:
            ip_address (str): L'adresse IP à vérifier
            
        Returns:
            int: Nombre de requêtes restantes
        """
        self._cleanup_old_requests(ip_address)
        return max(0, self.max_requests - len(self.requests[ip_address]))
    
    def limit(self, f):
        """
        Décorateur pour limiter le taux de requêtes sur une route.
        
        Args:
            f: La fonction à décorer
            
        Returns:
            function: La fonction décorée avec limitation de taux
            
        Example:
            @app.route('/login')
            @limiter.limit
            def login():
                pass
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Récupération de l'IP du client
            ip_address = request.remote_addr
            
            # Vérification si la requête est autorisée
            if not self.is_allowed(ip_address):
                logger.warning(f"Requête bloquée par rate limit: {ip_address}")
                flash('Trop de tentatives. Veuillez réessayer dans quelques minutes.', 'error')
                return redirect(url_for('main.index'))
            
            # Enregistrement de la requête
            self.record_request(ip_address)
            
            return f(*args, **kwargs)
        return decorated_function


# Instance globale du limiteur pour les tentatives de connexion
# 5 tentatives par minute maximum
login_limiter = RateLimiter(max_requests=5, window_seconds=60)

# Instance pour les soumissions de formulaires
# 10 soumissions par minute maximum
form_limiter = RateLimiter(max_requests=10, window_seconds=60)
