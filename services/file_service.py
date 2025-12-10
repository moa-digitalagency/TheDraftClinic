"""
================================================================================
TheDraftClinic - Service de Gestion des Fichiers
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module fournit les utilitaires de gestion des fichiers uploadés:
- Validation des types de fichiers autorisés
- Génération de noms de fichiers uniques
- Sauvegarde sécurisée des uploads

Sécurité:
- Seules certaines extensions sont autorisées
- Les noms de fichiers sont sécurisés avec secure_filename
- Les fichiers sont renommés avec un UUID pour éviter les conflits
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

import os                                    # Opérations sur les fichiers
import uuid                                  # Génération d'identifiants uniques
import logging                               # Logging des opérations
from werkzeug.utils import secure_filename   # Sécurisation des noms de fichiers

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Extensions de fichiers autorisées pour l'upload
# Divisées en catégories pour plus de clarté
ALLOWED_EXTENSIONS = {
    # Documents texte
    'pdf',      # Adobe PDF
    'doc',      # Microsoft Word (ancien)
    'docx',     # Microsoft Word (nouveau)
    'txt',      # Texte brut
    'rtf',      # Rich Text Format
    'odt',      # OpenDocument Text
    
    # Images (pour les preuves de paiement)
    'png',      # PNG
    'jpg',      # JPEG
    'jpeg',     # JPEG (variante)
    'gif',      # GIF
}


# ==============================================================================
# FONCTIONS DE VALIDATION
# ==============================================================================

def allowed_file(filename):
    """
    Vérifie si un fichier a une extension autorisée.
    
    Cette fonction est utilisée pour filtrer les uploads et n'accepter
    que les types de fichiers définis dans ALLOWED_EXTENSIONS.
    
    Args:
        filename (str): Le nom du fichier à vérifier
        
    Returns:
        bool: True si l'extension est autorisée, False sinon
        
    Example:
        >>> allowed_file("document.pdf")
        True
        >>> allowed_file("script.exe")
        False
        >>> allowed_file("noextension")
        False
        
    Security Note:
        Cette vérification se base sur l'extension du fichier, pas sur son
        contenu réel. Pour une sécurité maximale, le contenu devrait aussi
        être vérifié avec une bibliothèque comme python-magic.
    """
    # Vérifie qu'il y a un point dans le nom (donc une extension)
    if '.' not in filename:
        logger.warning(f"Fichier sans extension rejeté: {filename}")
        return False
    
    # Extrait l'extension (après le dernier point) et la met en minuscules
    extension = filename.rsplit('.', 1)[1].lower()
    
    # Vérifie si l'extension est dans la liste autorisée
    is_allowed = extension in ALLOWED_EXTENSIONS
    
    if not is_allowed:
        logger.warning(f"Extension non autorisée: .{extension}")
    
    return is_allowed


# ==============================================================================
# FONCTIONS DE SAUVEGARDE
# ==============================================================================

def save_uploaded_file(file, upload_folder):
    """
    Sauvegarde un fichier uploadé avec un nom unique et sécurisé.
    
    Cette fonction:
    1. Vérifie que le fichier est valide et a une extension autorisée
    2. Sécurise le nom du fichier pour éviter les injections
    3. Génère un nom unique avec UUID pour éviter les conflits
    4. Sauvegarde le fichier dans le dossier spécifié
    
    Args:
        file: Objet FileStorage de Flask (request.files[...])
        upload_folder (str): Chemin vers le dossier de destination
        
    Returns:
        str: Le nom unique du fichier sauvegardé, ou None si échec
        
    Example:
        >>> from flask import request
        >>> file = request.files['document']
        >>> filename = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        >>> print(filename)
        "a1b2c3d4e5f6_document.pdf"
        
    Security Notes:
        - secure_filename supprime les caractères dangereux du nom
        - UUID garantit l'unicité et empêche l'écrasement de fichiers
        - L'extension est préservée pour la compatibilité
    """
    # Vérification de base: le fichier existe-t-il?
    if not file:
        logger.warning("Aucun fichier fourni pour l'upload")
        return None
    
    # Vérification de l'extension
    if not allowed_file(file.filename):
        logger.warning(f"Type de fichier non autorisé: {file.filename}")
        return None
    
    try:
        # Sécurisation du nom de fichier original
        # Supprime les caractères spéciaux et les chemins relatifs
        original_filename = secure_filename(file.filename)
        
        # Génération d'un préfixe UUID unique
        # Utilise les 8 premiers caractères pour un ID court mais unique
        unique_prefix = uuid.uuid4().hex[:8]
        
        # Construction du nom de fichier final
        unique_filename = f"{unique_prefix}_{original_filename}"
        
        # Construction du chemin complet
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Sauvegarde du fichier
        file.save(file_path)
        
        # Log de succès
        logger.info(f"Fichier sauvegardé: {unique_filename}")
        
        return unique_filename
        
    except Exception as e:
        # Log de l'erreur
        logger.error(f"Erreur lors de la sauvegarde du fichier: {e}")
        return None


def delete_file(filename, upload_folder):
    """
    Supprime un fichier du dossier d'uploads.
    
    Args:
        filename (str): Nom du fichier à supprimer
        upload_folder (str): Chemin vers le dossier contenant le fichier
        
    Returns:
        bool: True si la suppression a réussi, False sinon
        
    Example:
        >>> delete_file("a1b2c3d4_document.pdf", app.config['UPLOAD_FOLDER'])
        True
    """
    try:
        # Construction du chemin complet
        file_path = os.path.join(upload_folder, filename)
        
        # Vérification de l'existence du fichier
        if not os.path.exists(file_path):
            logger.warning(f"Fichier à supprimer non trouvé: {filename}")
            return False
        
        # Suppression du fichier
        os.remove(file_path)
        
        logger.info(f"Fichier supprimé: {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du fichier {filename}: {e}")
        return False


def get_file_size(filename, upload_folder):
    """
    Retourne la taille d'un fichier en octets.
    
    Args:
        filename (str): Nom du fichier
        upload_folder (str): Chemin vers le dossier contenant le fichier
        
    Returns:
        int: Taille en octets, ou 0 si le fichier n'existe pas
    """
    try:
        file_path = os.path.join(upload_folder, filename)
        
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        
        return 0
        
    except Exception as e:
        logger.error(f"Erreur lors de la lecture de la taille de {filename}: {e}")
        return 0
