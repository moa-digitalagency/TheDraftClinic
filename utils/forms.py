"""
================================================================================
TheDraftClinic - Forms Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module defines all WTForms used in the application including
login, registration, service request, and payment forms.
================================================================================
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, IntegerField, FloatField, DateTimeLocalField, MultipleFileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class LoginForm(FlaskForm):
    """
    Login form for user authentication.
    
    Fields:
        email: User email address
        password: User password
        remember: Remember me checkbox
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Téléphone', validators=[Optional(), Length(max=20)])
    institution = StringField('Établissement académique', validators=[Optional(), Length(max=200)])
    academic_level = SelectField('Niveau académique', choices=[
        ('', 'Sélectionner...'),
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('post_doc', 'Post-doctorat'),
        ('chercheur', 'Chercheur'),
        ('professeur', 'Professeur'),
        ('autre', 'Autre')
    ], validators=[Optional()])
    field_of_study = StringField('Domaine d\'étude', validators=[Optional(), Length(max=100)])


class ServiceRequestForm(FlaskForm):
    service_type = SelectField('Type de service', validators=[DataRequired()])
    title = StringField('Titre du travail', validators=[DataRequired(), Length(max=300)])
    description = TextAreaField('Description détaillée', validators=[Optional()])
    additional_info = TextAreaField('Informations supplémentaires', validators=[Optional()])
    word_count = IntegerField('Nombre de mots (estimé)', validators=[Optional(), NumberRange(min=0)])
    pages_count = IntegerField('Nombre de pages', validators=[Optional(), NumberRange(min=0)])
    deadline = DateTimeLocalField('Date limite', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    urgency_level = SelectField('Niveau d\'urgence', choices=[
        ('standard', 'Standard (48h+)'),
        ('express_24h', 'Express 24h (+25%)'),
        ('express_5h', 'Express 5h (+75%)')
    ], validators=[Optional()])
    documents = MultipleFileField('Documents à joindre')
    
    def __init__(self, *args, **kwargs):
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        from models.request import ServiceRequest
        self.service_type.choices = ServiceRequest.SERVICE_TYPES


class PaymentProofForm(FlaskForm):
    amount = FloatField('Montant payé', validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField('Méthode de paiement', choices=[
        ('bank_transfer', 'Virement bancaire'),
        ('paypal', 'PayPal'),
        ('card', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
        ('other', 'Autre')
    ], validators=[DataRequired()])
    proof_document = FileField('Capture/Justificatif de paiement', validators=[
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'Fichiers autorisés: PDF, PNG, JPG')
    ])
    transaction_reference = StringField('Référence de transaction', validators=[Optional(), Length(max=100)])
    notes = TextAreaField('Notes', validators=[Optional()])
