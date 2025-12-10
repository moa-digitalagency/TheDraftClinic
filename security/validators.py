"""
================================================================================
TheDraftClinic - Validateurs de Sécurité
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
================================================================================

Ce module contient les fonctions de validation des entrées utilisateur:
- validate_email: Valide le format des emails
- validate_password: Vérifie la force des mots de passe
- sanitize_input: Nettoie les entrées contre les injections XSS
================================================================================
"""

import re
import html
import logging

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)

# Expression régulière pour la validation d'email (RFC 5322 simplifiée)
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Critères de mot de passe fort
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGIT = True
PASSWORD_REQUIRE_SPECIAL = False


def validate_email(email):
    """
    Valide le format d'une adresse email.
    
    Utilise une expression régulière basée sur RFC 5322 pour vérifier
    que l'email a un format valide.
    
    Args:
        email (str): L'adresse email à valider
        
    Returns:
        tuple: (bool, str) - (est_valide, message_erreur ou None)
        
    Example:
        is_valid, error = validate_email("user@example.com")
        if not is_valid:
            flash(error, 'error')
    """
    # Vérification si l'email est fourni
    if not email:
        return False, "L'adresse email est requise."
    
    # Nettoyage des espaces
    email = email.strip().lower()
    
    # Vérification de la longueur
    if len(email) > 254:
        logger.warning(f"Email trop long tenté: {len(email)} caractères")
        return False, "L'adresse email est trop longue."
    
    # Validation du format avec regex
    if not EMAIL_REGEX.match(email):
        return False, "Le format de l'adresse email est invalide."
    
    return True, None


def validate_password(password, confirm_password=None):
    """
    Valide la force d'un mot de passe selon les critères de sécurité.
    
    Vérifie:
    - Longueur minimale (8 caractères)
    - Présence de majuscules
    - Présence de minuscules
    - Présence de chiffres
    - Correspondance avec la confirmation (si fournie)
    
    Args:
        password (str): Le mot de passe à valider
        confirm_password (str, optional): La confirmation du mot de passe
        
    Returns:
        tuple: (bool, str) - (est_valide, message_erreur ou None)
        
    Example:
        is_valid, error = validate_password("MonMotDePasse123")
        if not is_valid:
            flash(error, 'error')
    """
    # Vérification si le mot de passe est fourni
    if not password:
        return False, "Le mot de passe est requis."
    
    # Liste des erreurs trouvées
    errors = []
    
    # Vérification de la longueur minimale
    if len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Le mot de passe doit contenir au moins {PASSWORD_MIN_LENGTH} caractères.")
    
    # Vérification de la présence de majuscules
    if PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        errors.append("Le mot de passe doit contenir au moins une majuscule.")
    
    # Vérification de la présence de minuscules
    if PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        errors.append("Le mot de passe doit contenir au moins une minuscule.")
    
    # Vérification de la présence de chiffres
    if PASSWORD_REQUIRE_DIGIT and not re.search(r'\d', password):
        errors.append("Le mot de passe doit contenir au moins un chiffre.")
    
    # Vérification de la présence de caractères spéciaux
    if PASSWORD_REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Le mot de passe doit contenir au moins un caractère spécial.")
    
    # Vérification de la correspondance avec la confirmation
    if confirm_password is not None and password != confirm_password:
        errors.append("Les mots de passe ne correspondent pas.")
    
    # Retour du résultat
    if errors:
        return False, " ".join(errors)
    
    return True, None


def sanitize_input(text, max_length=None):
    """
    Nettoie une entrée utilisateur contre les injections XSS.
    
    Cette fonction:
    - Échappe les caractères HTML spéciaux
    - Supprime les espaces en trop au début et à la fin
    - Limite la longueur si spécifié
    
    Args:
        text (str): Le texte à nettoyer
        max_length (int, optional): Longueur maximale autorisée
        
    Returns:
        str: Le texte nettoyé et sécurisé
        
    Example:
        user_input = sanitize_input(request.form.get('comment'), max_length=500)
    """
    # Vérification si le texte est None
    if text is None:
        return ""
    
    # Conversion en string si nécessaire
    text = str(text)
    
    # Suppression des espaces en trop
    text = text.strip()
    
    # Échappement des caractères HTML (protection XSS)
    text = html.escape(text)
    
    # Limitation de la longueur si spécifié
    if max_length and len(text) > max_length:
        logger.info(f"Entrée tronquée de {len(text)} à {max_length} caractères")
        text = text[:max_length]
    
    return text


def sanitize_filename(filename):
    """
    Nettoie un nom de fichier pour éviter les problèmes de sécurité.
    
    Supprime les caractères potentiellement dangereux et les chemins relatifs.
    
    Args:
        filename (str): Le nom de fichier à nettoyer
        
    Returns:
        str: Le nom de fichier sécurisé
        
    Example:
        safe_name = sanitize_filename(uploaded_file.filename)
    """
    # Suppression des caractères dangereux
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    
    # Suppression des espaces multiples
    filename = re.sub(r'\s+', '_', filename)
    
    # Suppression des points au début (fichiers cachés)
    filename = filename.lstrip('.')
    
    return filename
