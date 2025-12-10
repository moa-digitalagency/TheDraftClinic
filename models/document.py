"""
================================================================================
TheDraftClinic - Modèle Document
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit le modèle Document pour la gestion des fichiers uploadés.
Il gère les documents clients, les uploads admin et les livrables.

Relations:
- Appartient à une demande de service (ServiceRequest)
- Uploadé par un utilisateur (User)
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from app import db                           # Instance SQLAlchemy
from datetime import datetime                # Gestion des dates
import logging                               # Logging des erreurs

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


# ==============================================================================
# MODÈLE DOCUMENT
# ==============================================================================

class Document(db.Model):
    """
    Modèle représentant un fichier uploadé dans le système.
    
    Les documents peuvent être de plusieurs types:
    - client_upload: Documents de référence fournis par le client
    - admin_upload: Documents ajoutés par l'administrateur
    - deliverable: Travail final livré au client
    - revision: Version révisée d'un livrable
    
    Attributes:
        id (int): Clé primaire auto-incrémentée
        request_id (int): Clé étrangère vers la demande
        filename (str): Nom unique du fichier stocké
        original_filename (str): Nom original du fichier uploadé
        file_type (str): Type MIME du fichier
        document_type (str): Catégorie du document
        uploaded_by (int): ID de l'utilisateur ayant uploadé
    
    Relationships:
        request: Demande de service associée
    """
    
    # Nom de la table dans la base de données
    __tablename__ = 'documents'
    
    # --------------------------------------------------------------------------
    # CLÉS
    # --------------------------------------------------------------------------
    
    # Clé primaire
    id = db.Column(
        db.Integer, 
        primary_key=True,
        doc="Identifiant unique du document"
    )
    
    # Clé étrangère vers la demande
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey('service_requests.id'), 
        nullable=False,
        index=True,
        doc="ID de la demande de service associée"
    )
    
    # --------------------------------------------------------------------------
    # INFORMATIONS DU FICHIER
    # --------------------------------------------------------------------------
    
    # Nom de fichier unique (généré par le système)
    filename = db.Column(
        db.String(255), 
        nullable=False,
        doc="Nom unique du fichier sur le serveur (avec UUID)"
    )
    
    # Nom original du fichier
    original_filename = db.Column(
        db.String(255), 
        nullable=False,
        doc="Nom original du fichier tel qu'uploadé"
    )
    
    # Type MIME
    file_type = db.Column(
        db.String(50),
        doc="Type MIME du fichier (application/pdf, etc.)"
    )
    
    # Taille du fichier
    file_size = db.Column(
        db.Integer,
        doc="Taille du fichier en octets"
    )
    
    # --------------------------------------------------------------------------
    # CATÉGORISATION
    # --------------------------------------------------------------------------
    
    # Type de document
    document_type = db.Column(
        db.String(30), 
        default='client_upload',
        doc="Catégorie: client_upload, admin_upload, deliverable, revision"
    )
    
    # Description
    description = db.Column(
        db.Text,
        doc="Description ou note sur le document"
    )
    
    # --------------------------------------------------------------------------
    # TRAÇABILITÉ
    # --------------------------------------------------------------------------
    
    # Utilisateur ayant uploadé le fichier
    uploaded_by = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        doc="ID de l'utilisateur ayant uploadé le fichier"
    )
    
    # Date de création
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        doc="Date et heure d'upload du document"
    )
    
    # --------------------------------------------------------------------------
    # CONSTANTES
    # --------------------------------------------------------------------------
    
    DOCUMENT_TYPES = [
        ('client_upload', 'Document client'),
        ('admin_upload', 'Document admin'),
        ('deliverable', 'Livrable'),
        ('revision', 'Révision')
    ]
    
    # --------------------------------------------------------------------------
    # MÉTHODES
    # --------------------------------------------------------------------------
    
    def get_type_display(self):
        """
        Retourne le libellé français du type de document.
        
        Returns:
            str: Libellé du type (ex: "Livrable")
        """
        for code, label in self.DOCUMENT_TYPES:
            if code == self.document_type:
                return label
        logger.warning(f"Type de document inconnu: {self.document_type}")
        return self.document_type
    
    def __repr__(self):
        """
        Représentation string du document pour le débogage.
        
        Returns:
            str: Représentation formatée du document
        """
        return f'<Document {self.id} - {self.original_filename}>'
