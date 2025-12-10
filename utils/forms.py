"""
================================================================================
TheDraftClinic - Module des Formulaires
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module définit tous les formulaires WTForms utilisés dans l'application:
- LoginForm: Formulaire de connexion
- RegistrationForm: Formulaire d'inscription
- ServiceRequestForm: Formulaire de nouvelle demande
- PaymentProofForm: Formulaire de soumission de paiement

Chaque formulaire inclut:
- Validation des champs
- Messages d'erreur en français
- Protection CSRF (via FlaskForm)
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from flask_wtf import FlaskForm                    # Base pour les formulaires
from flask_wtf.file import FileField, FileAllowed  # Gestion des uploads
from wtforms import (                              # Types de champs
    StringField, 
    PasswordField, 
    BooleanField, 
    TextAreaField, 
    SelectField, 
    IntegerField, 
    FloatField, 
    DateTimeLocalField, 
    MultipleFileField
)
from wtforms.validators import (                    # Validateurs
    DataRequired, 
    Email, 
    Length, 
    EqualTo, 
    Optional, 
    NumberRange
)


# ==============================================================================
# FORMULAIRE DE CONNEXION
# ==============================================================================

class LoginForm(FlaskForm):
    """
    Formulaire de connexion pour l'authentification des utilisateurs.
    
    Champs:
        email: Adresse email de l'utilisateur (requis, format email)
        password: Mot de passe (requis)
        remember: Case à cocher "Se souvenir de moi"
    
    Utilisation:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
    """
    
    # Champ email avec validation de format
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='L\'email est requis.'),
            Email(message='Format d\'email invalide.')
        ],
        render_kw={'placeholder': 'votre@email.com'}
    )
    
    # Champ mot de passe
    password = PasswordField(
        'Mot de passe',
        validators=[
            DataRequired(message='Le mot de passe est requis.')
        ],
        render_kw={'placeholder': 'Votre mot de passe'}
    )
    
    # Case "Se souvenir de moi"
    remember = BooleanField('Se souvenir de moi')


# ==============================================================================
# FORMULAIRE D'INSCRIPTION
# ==============================================================================

class RegistrationForm(FlaskForm):
    """
    Formulaire d'inscription pour les nouveaux utilisateurs.
    
    Champs obligatoires:
        email: Adresse email unique
        password: Mot de passe (min 6 caractères)
        confirm_password: Confirmation du mot de passe
        first_name: Prénom
        last_name: Nom de famille
    
    Champs optionnels:
        phone: Numéro de téléphone
        institution: Établissement académique
        academic_level: Niveau d'études
        field_of_study: Domaine d'étude
    """
    
    # Informations de connexion
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='L\'email est requis.'),
            Email(message='Format d\'email invalide.')
        ],
        render_kw={'placeholder': 'votre@email.com'}
    )
    
    password = PasswordField(
        'Mot de passe',
        validators=[
            DataRequired(message='Le mot de passe est requis.'),
            Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères.')
        ],
        render_kw={'placeholder': 'Minimum 6 caractères'}
    )
    
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(message='Veuillez confirmer le mot de passe.'),
            EqualTo('password', message='Les mots de passe ne correspondent pas.')
        ],
        render_kw={'placeholder': 'Répétez le mot de passe'}
    )
    
    # Informations personnelles
    first_name = StringField(
        'Prénom',
        validators=[
            DataRequired(message='Le prénom est requis.'),
            Length(max=50, message='Le prénom ne peut pas dépasser 50 caractères.')
        ],
        render_kw={'placeholder': 'Votre prénom'}
    )
    
    last_name = StringField(
        'Nom',
        validators=[
            DataRequired(message='Le nom est requis.'),
            Length(max=50, message='Le nom ne peut pas dépasser 50 caractères.')
        ],
        render_kw={'placeholder': 'Votre nom'}
    )
    
    phone = StringField(
        'Téléphone',
        validators=[
            Optional(),
            Length(max=20, message='Le numéro ne peut pas dépasser 20 caractères.')
        ],
        render_kw={'placeholder': '+33 6 12 34 56 78'}
    )
    
    # Informations académiques
    institution = StringField(
        'Établissement académique',
        validators=[
            Optional(),
            Length(max=200, message='Le nom de l\'établissement est trop long.')
        ],
        render_kw={'placeholder': 'Université, École...'}
    )
    
    # Liste des niveaux académiques
    academic_level = SelectField(
        'Niveau académique',
        choices=[
            ('', 'Sélectionner...'),
            ('licence', 'Licence'),
            ('master', 'Master'),
            ('doctorat', 'Doctorat'),
            ('post_doc', 'Post-doctorat'),
            ('chercheur', 'Chercheur'),
            ('professeur', 'Professeur'),
            ('autre', 'Autre')
        ],
        validators=[Optional()]
    )
    
    field_of_study = StringField(
        'Domaine d\'étude',
        validators=[
            Optional(),
            Length(max=100, message='Le domaine ne peut pas dépasser 100 caractères.')
        ],
        render_kw={'placeholder': 'Sciences, Lettres, Droit...'}
    )


# ==============================================================================
# FORMULAIRE DE DEMANDE DE SERVICE
# ==============================================================================

class ServiceRequestForm(FlaskForm):
    """
    Formulaire pour soumettre une nouvelle demande de service.
    
    Champs obligatoires:
        service_type: Type de service souhaité
        title: Titre du travail
    
    Champs optionnels:
        description: Description détaillée du projet
        additional_info: Informations supplémentaires
        word_count: Nombre de mots estimé
        pages_count: Nombre de pages
        deadline: Date limite souhaitée
        urgency_level: Niveau d'urgence
        documents: Fichiers à joindre
    """
    
    # Type de service (les choix sont chargés dynamiquement)
    service_type = SelectField(
        'Type de service',
        validators=[
            DataRequired(message='Veuillez sélectionner un type de service.')
        ]
    )
    
    # Titre du projet
    title = StringField(
        'Titre du travail',
        validators=[
            DataRequired(message='Le titre est requis.'),
            Length(max=300, message='Le titre ne peut pas dépasser 300 caractères.')
        ],
        render_kw={'placeholder': 'Ex: Thèse sur l\'impact du changement climatique...'}
    )
    
    # Description détaillée
    description = TextAreaField(
        'Description détaillée',
        validators=[Optional()],
        render_kw={
            'placeholder': 'Décrivez votre projet en détail...',
            'rows': 5
        }
    )
    
    # Informations supplémentaires
    additional_info = TextAreaField(
        'Informations supplémentaires',
        validators=[Optional()],
        render_kw={
            'placeholder': 'Instructions spéciales, références à inclure...',
            'rows': 3
        }
    )
    
    # Spécifications techniques
    word_count = IntegerField(
        'Nombre de mots (estimé)',
        validators=[
            Optional(),
            NumberRange(min=0, message='Le nombre doit être positif.')
        ],
        render_kw={'placeholder': '5000'}
    )
    
    pages_count = IntegerField(
        'Nombre de pages',
        validators=[
            Optional(),
            NumberRange(min=0, message='Le nombre doit être positif.')
        ],
        render_kw={'placeholder': '20'}
    )
    
    # Date limite
    deadline = DateTimeLocalField(
        'Date limite',
        format='%Y-%m-%dT%H:%M',
        validators=[Optional()]
    )
    
    # Niveau d'urgence
    urgency_level = SelectField(
        'Niveau d\'urgence',
        choices=[
            ('standard', 'Standard (48h+)'),
            ('express_24h', 'Express 24h (+25%)'),
            ('express_5h', 'Express 5h (+75%)')
        ],
        validators=[Optional()]
    )
    
    # Documents à joindre
    documents = MultipleFileField(
        'Documents à joindre',
        render_kw={'accept': '.pdf,.doc,.docx,.txt,.rtf,.odt,.png,.jpg,.jpeg,.gif'}
    )
    
    def __init__(self, *args, **kwargs):
        """
        Initialise le formulaire en chargeant dynamiquement les types de services.
        
        Les types de services sont récupérés depuis le modèle ServiceRequest
        pour maintenir la cohérence avec la base de données.
        """
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        
        # Import du modèle pour récupérer les types de services
        from models.request import ServiceRequest
        self.service_type.choices = ServiceRequest.SERVICE_TYPES


# ==============================================================================
# FORMULAIRE DE PREUVE DE PAIEMENT
# ==============================================================================

class PaymentProofForm(FlaskForm):
    """
    Formulaire pour soumettre une preuve de paiement.
    
    Champs obligatoires:
        amount: Montant payé
        payment_method: Méthode de paiement utilisée
    
    Champs optionnels:
        proof_document: Fichier de preuve (capture d'écran, reçu...)
        transaction_reference: Référence de la transaction
        notes: Notes additionnelles
    """
    
    # Montant payé
    amount = FloatField(
        'Montant payé',
        validators=[
            DataRequired(message='Le montant est requis.'),
            NumberRange(min=0, message='Le montant doit être positif.')
        ],
        render_kw={'placeholder': '500.00', 'step': '0.01'}
    )
    
    # Méthode de paiement
    payment_method = SelectField(
        'Méthode de paiement',
        choices=[
            ('bank_transfer', 'Virement bancaire'),
            ('paypal', 'PayPal'),
            ('card', 'Carte bancaire'),
            ('mobile_money', 'Mobile Money'),
            ('other', 'Autre')
        ],
        validators=[
            DataRequired(message='Veuillez sélectionner une méthode de paiement.')
        ]
    )
    
    # Document de preuve
    proof_document = FileField(
        'Capture/Justificatif de paiement',
        validators=[
            FileAllowed(
                ['pdf', 'png', 'jpg', 'jpeg'],
                message='Fichiers autorisés: PDF, PNG, JPG'
            )
        ]
    )
    
    # Référence de transaction
    transaction_reference = StringField(
        'Référence de transaction',
        validators=[
            Optional(),
            Length(max=100, message='La référence ne peut pas dépasser 100 caractères.')
        ],
        render_kw={'placeholder': 'REF-12345'}
    )
    
    # Notes
    notes = TextAreaField(
        'Notes',
        validators=[Optional()],
        render_kw={
            'placeholder': 'Informations complémentaires sur le paiement...',
            'rows': 2
        }
    )
