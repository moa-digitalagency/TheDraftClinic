"""
================================================================================
TheDraftClinic - Point d'Entrée de l'Application
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce fichier est le point d'entrée principal de l'application Flask.
Il utilise le pattern Factory pour créer l'instance de l'application.

Usage:
    # Développement avec Gunicorn (recommandé)
    uv run gunicorn --bind 0.0.0.0:5000 --reload main:app
    
    # Ou directement avec Python
    uv run python main.py
================================================================================
"""

# ==============================================================================
# IMPORTATION ET CRÉATION DE L'APPLICATION
# ==============================================================================

from app import create_app

# Création de l'instance de l'application Flask
# La fonction create_app() configure: DB, Auth, CSRF, Routes, Logging
app = create_app()


# ==============================================================================
# EXÉCUTION EN MODE DÉVELOPPEMENT
# ==============================================================================

if __name__ == '__main__':
    """
    Point d'entrée pour l'exécution directe avec Python.
    En production, utilisez Gunicorn au lieu de ce mode de développement.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)
