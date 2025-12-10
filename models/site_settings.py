"""
================================================================================
TheDraftClinic - Modèle Paramètres du Site
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle SiteSettings pour la configuration du site.
Il stocke les paramètres globaux comme le logo, SEO, mentions légales, etc.
================================================================================
"""

from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SiteSettings(db.Model):
    """
    Modèle pour les paramètres globaux du site.
    
    Stocke une seule entrée avec tous les paramètres configurables:
    - Branding (logo, favicon, nom)
    - SEO et OpenGraph
    - Informations légales
    - Configuration régionale
    """
    
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    site_name = db.Column(db.String(100), default='TheDraftClinic')
    site_description = db.Column(db.Text)
    
    logo_filename = db.Column(db.String(255))
    favicon_filename = db.Column(db.String(255))
    
    seo_title = db.Column(db.String(70))
    seo_description = db.Column(db.String(160))
    seo_keywords = db.Column(db.String(255))
    
    og_title = db.Column(db.String(70))
    og_description = db.Column(db.String(200))
    og_image_filename = db.Column(db.String(255))
    og_type = db.Column(db.String(50), default='website')
    
    twitter_card = db.Column(db.String(20), default='summary_large_image')
    twitter_site = db.Column(db.String(50))
    
    timezone = db.Column(db.String(50), default='Europe/Paris')
    country = db.Column(db.String(100), default='France')
    default_language = db.Column(db.String(10), default='fr')
    currency = db.Column(db.String(10), default='EUR')
    
    company_name = db.Column(db.String(200))
    company_address = db.Column(db.Text)
    company_email = db.Column(db.String(120))
    company_phone = db.Column(db.String(30))
    company_registration = db.Column(db.String(100))
    vat_number = db.Column(db.String(50))
    
    legal_status = db.Column(db.String(200))
    share_capital = db.Column(db.String(100))
    rcs_number = db.Column(db.String(100))
    siret_number = db.Column(db.String(50))
    ape_code = db.Column(db.String(20))
    
    hosting_provider = db.Column(db.String(200))
    hosting_address = db.Column(db.Text)
    dpo_name = db.Column(db.String(200))
    dpo_email = db.Column(db.String(120))
    
    google_analytics_id = db.Column(db.String(50))
    google_tag_manager_id = db.Column(db.String(50))
    facebook_pixel_id = db.Column(db.String(50))
    
    robots_txt_content = db.Column(db.Text)
    custom_head_scripts = db.Column(db.Text)
    custom_body_scripts = db.Column(db.Text)
    
    maintenance_mode = db.Column(db.Boolean, default=False)
    maintenance_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_settings():
        """
        Récupère les paramètres du site (crée une entrée si inexistante).
        
        Returns:
            SiteSettings: L'instance des paramètres
        """
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        return settings
    
    def get_logo_url(self):
        """Retourne l'URL du logo ou None."""
        if self.logo_filename:
            from flask import url_for
            return url_for('static', filename=f'uploads/branding/{self.logo_filename}')
        return None
    
    def get_favicon_url(self):
        """Retourne l'URL du favicon ou None."""
        if self.favicon_filename:
            from flask import url_for
            return url_for('static', filename=f'uploads/branding/{self.favicon_filename}')
        return None
    
    def get_og_image_url(self):
        """Retourne l'URL de l'image OG ou None."""
        if self.og_image_filename:
            from flask import url_for
            return url_for('static', filename=f'uploads/branding/{self.og_image_filename}')
        return None
    
    def __repr__(self):
        return f'<SiteSettings {self.site_name}>'
