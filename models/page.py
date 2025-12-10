"""
================================================================================
TheDraftClinic - Modèle Page Dynamique
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle Page pour les pages de contenu dynamique.
Permet de créer des pages comme CGU, CGV, Politique de confidentialité, etc.
================================================================================
"""

from app import db
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


class Page(db.Model):
    """
    Modèle pour les pages de contenu dynamique.
    
    Permet de créer et gérer des pages avec contenu HTML ou Markdown:
    - CGU (Conditions Générales d'Utilisation)
    - CGV (Conditions Générales de Vente)
    - Politique de confidentialité
    - Mentions légales
    - FAQ
    - Autres pages personnalisées
    """
    
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(200), nullable=False)
    
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    
    content = db.Column(db.Text)
    
    content_format = db.Column(db.String(20), default='html')
    
    meta_title = db.Column(db.String(70))
    meta_description = db.Column(db.String(160))
    
    is_published = db.Column(db.Boolean, default=False)
    
    show_in_footer = db.Column(db.Boolean, default=True)
    
    show_in_navigation = db.Column(db.Boolean, default=False)
    
    order_index = db.Column(db.Integer, default=0)
    
    page_type = db.Column(db.String(50), default='custom')
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = db.relationship('User', backref='pages')
    
    PAGE_TYPES = [
        ('cgu', 'Conditions Générales d\'Utilisation'),
        ('cgv', 'Conditions Générales de Vente'),
        ('privacy', 'Politique de Confidentialité'),
        ('legal', 'Mentions Légales'),
        ('faq', 'Foire Aux Questions'),
        ('about', 'À Propos'),
        ('contact', 'Contact'),
        ('custom', 'Page Personnalisée')
    ]
    
    @staticmethod
    def generate_slug(title):
        """
        Génère un slug à partir du titre.
        
        Args:
            title: Le titre de la page
            
        Returns:
            str: Le slug généré
        """
        slug = title.lower()
        slug = re.sub(r'[àáâãäå]', 'a', slug)
        slug = re.sub(r'[èéêë]', 'e', slug)
        slug = re.sub(r'[ìíîï]', 'i', slug)
        slug = re.sub(r'[òóôõö]', 'o', slug)
        slug = re.sub(r'[ùúûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[ñ]', 'n', slug)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    def get_rendered_content(self):
        """
        Retourne le contenu rendu (HTML ou Markdown converti).
        
        Returns:
            str: Le contenu HTML
        """
        if self.content_format == 'markdown':
            try:
                import markdown
                return markdown.markdown(
                    self.content or '',
                    extensions=['tables', 'fenced_code', 'toc']
                )
            except ImportError:
                logger.warning("Module markdown non installé, retour au contenu brut")
                return self.content or ''
        return self.content or ''
    
    def get_type_display(self):
        """Retourne le libellé du type de page."""
        for code, label in self.PAGE_TYPES:
            if code == self.page_type:
                return label
        return self.page_type
    
    @staticmethod
    def get_footer_pages():
        """Retourne les pages à afficher dans le footer."""
        return Page.query.filter_by(
            is_published=True,
            show_in_footer=True
        ).order_by(Page.order_index).all()
    
    @staticmethod
    def get_navigation_pages():
        """Retourne les pages à afficher dans la navigation."""
        return Page.query.filter_by(
            is_published=True,
            show_in_navigation=True
        ).order_by(Page.order_index).all()
    
    def __repr__(self):
        return f'<Page {self.slug}>'
