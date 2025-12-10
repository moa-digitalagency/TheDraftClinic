"""
================================================================================
TheDraftClinic - Routes Client
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module gère toutes les routes de l'espace client:
- Dashboard client avec statistiques
- Soumission de nouvelles demandes
- Visualisation des demandes existantes
- Acceptation des devis
- Soumission des preuves de paiement
- Gestion du profil utilisateur

Sécurité:
- Toutes les routes nécessitent une authentification
- Vérification que l'utilisateur accède uniquement à ses propres données
- Protection CSRF sur les formulaires
================================================================================
"""

# ==============================================================================
# IMPORTATIONS
# ==============================================================================

from flask import (
    Blueprint, render_template, redirect, url_for, 
    flash, request, current_app
)
from flask_login import login_required, current_user
from functools import wraps
import logging

from app import db
from models.request import ServiceRequest
from models.document import Document
from models.payment import Payment
from utils.forms import ServiceRequestForm, PaymentProofForm
from services.file_service import save_uploaded_file

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)

# Création du blueprint client
bp = Blueprint('client', __name__)


# ==============================================================================
# DÉCORATEUR CLIENT REQUIRED
# ==============================================================================

def client_required(f):
    """
    Décorateur vérifiant que l'utilisateur est un client (non-admin).
    
    Les administrateurs sont automatiquement redirigés vers leur
    propre tableau de bord s'ils tentent d'accéder à l'espace client.
    
    Args:
        f: La fonction à décorer
        
    Returns:
        function: La fonction décorée
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Rediriger les admins vers leur dashboard
        if current_user.is_admin:
            logger.debug(f"Admin redirigé du dashboard client: {current_user.email}")
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# DASHBOARD CLIENT
# ==============================================================================

@bp.route('/dashboard')
@login_required
@client_required
def dashboard():
    """
    Affiche le tableau de bord principal du client.
    
    Présente:
    - Liste de toutes les demandes du client
    - Statistiques (total, en cours, en attente, terminées)
    - Actions rapides
    
    Returns:
        Template dashboard avec les demandes et statistiques
    """
    try:
        # Récupération des demandes du client, triées par date
        requests = ServiceRequest.query.filter_by(
            user_id=current_user.id
        ).order_by(ServiceRequest.created_at.desc()).all()
        
        # Calcul des statistiques
        stats = {
            'total': len(requests),
            'in_progress': len([r for r in requests if r.status in ['in_progress', 'revision']]),
            'pending_quote': len([r for r in requests if r.status in ['submitted', 'under_review', 'quote_sent']]),
            'completed': len([r for r in requests if r.status in ['completed', 'delivered']])
        }
        
        logger.debug(f"Dashboard client: {current_user.email}, {stats['total']} demandes")
        
        return render_template('client/dashboard.html', requests=requests, stats=stats)
        
    except Exception as e:
        logger.error(f"Erreur dashboard client pour {current_user.email}: {e}")
        flash('Une erreur est survenue lors du chargement du tableau de bord.', 'error')
        return render_template('client/dashboard.html', requests=[], stats={
            'total': 0, 'in_progress': 0, 'pending_quote': 0, 'completed': 0
        })


# ==============================================================================
# NOUVELLE DEMANDE
# ==============================================================================

@bp.route('/new-request', methods=['GET', 'POST'])
@login_required
@client_required
def new_request():
    """
    Permet au client de soumettre une nouvelle demande de service.
    
    GET: Affiche le formulaire de nouvelle demande
    POST: Traite la soumission de la demande
    
    Workflow:
    1. Valide le formulaire
    2. Crée la demande en base de données
    3. Sauvegarde les documents uploadés
    4. Redirige vers la page de détail de la demande
    
    Returns:
        - GET: Template du formulaire
        - POST (succès): Redirection vers la demande créée
        - POST (échec): Template avec erreurs
    """
    try:
        # Création du formulaire
        form = ServiceRequestForm()
        
        if form.validate_on_submit():
            # Création de la demande de service
            service_request = ServiceRequest(
                user_id=current_user.id,
                service_type=form.service_type.data,
                title=form.title.data.strip(),
                description=form.description.data.strip() if form.description.data else None,
                additional_info=form.additional_info.data.strip() if form.additional_info.data else None,
                word_count=form.word_count.data,
                pages_count=form.pages_count.data,
                deadline=form.deadline.data,
                urgency_level=form.urgency_level.data,
                status='submitted'
            )
            
            # Sauvegarde initiale pour obtenir l'ID
            db.session.add(service_request)
            db.session.commit()
            
            # Traitement des documents uploadés
            if form.documents.data:
                for file in request.files.getlist('documents'):
                    if file and file.filename:
                        saved_filename = save_uploaded_file(
                            file, 
                            current_app.config['UPLOAD_FOLDER']
                        )
                        if saved_filename:
                            doc = Document(
                                request_id=service_request.id,
                                filename=saved_filename,
                                original_filename=file.filename,
                                file_type=file.content_type,
                                document_type='client_upload',
                                uploaded_by=current_user.id
                            )
                            db.session.add(doc)
            
            # Sauvegarde finale avec les documents
            db.session.commit()
            
            logger.info(f"Nouvelle demande créée: {service_request.id} par {current_user.email}")
            flash('Votre demande a été soumise avec succès!', 'success')
            return redirect(url_for('client.view_request', request_id=service_request.id))
        
        return render_template(
            'client/new_request.html', 
            form=form, 
            service_types=ServiceRequest.SERVICE_TYPES
        )
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur création demande par {current_user.email}: {e}")
        flash('Une erreur est survenue lors de la soumission.', 'error')
        return render_template(
            'client/new_request.html', 
            form=ServiceRequestForm(), 
            service_types=ServiceRequest.SERVICE_TYPES
        )


# ==============================================================================
# DÉTAIL D'UNE DEMANDE
# ==============================================================================

@bp.route('/request/<int:request_id>')
@login_required
@client_required
def view_request(request_id):
    """
    Affiche les détails d'une demande spécifique.
    
    Vérifie que la demande appartient bien au client connecté.
    
    Args:
        request_id: ID de la demande à afficher
        
    Returns:
        Template avec les détails de la demande
        
    Raises:
        404: Si la demande n'existe pas ou n'appartient pas au client
    """
    try:
        # Récupération de la demande avec vérification du propriétaire
        service_request = ServiceRequest.query.filter_by(
            id=request_id, 
            user_id=current_user.id
        ).first_or_404()
        
        # Récupération des documents et paiements associés
        documents = Document.query.filter_by(request_id=request_id).all()
        payments = Payment.query.filter_by(request_id=request_id).order_by(
            Payment.created_at.desc()
        ).all()
        
        # Formulaire de paiement pour soumission d'acompte
        payment_form = PaymentProofForm()
        
        return render_template(
            'client/view_request.html', 
            request=service_request, 
            documents=documents, 
            payments=payments,
            payment_form=payment_form
        )
        
    except Exception as e:
        logger.error(f"Erreur affichage demande {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('client.dashboard'))


# ==============================================================================
# ACCEPTATION D'UN DEVIS
# ==============================================================================

@bp.route('/request/<int:request_id>/accept-quote', methods=['POST'])
@login_required
@client_required
def accept_quote(request_id):
    """
    Permet au client d'accepter un devis reçu.
    
    Change le statut de la demande de 'quote_sent' à 'awaiting_deposit'.
    
    Args:
        request_id: ID de la demande
        
    Returns:
        Redirection vers la page de la demande
    """
    try:
        # Récupération et vérification de la demande
        service_request = ServiceRequest.query.filter_by(
            id=request_id, 
            user_id=current_user.id
        ).first_or_404()
        
        # Vérification du statut actuel
        if service_request.status != 'quote_sent':
            flash('Cette action n\'est pas possible pour cette demande.', 'error')
            return redirect(url_for('client.view_request', request_id=request_id))
        
        # Mise à jour du statut
        service_request.quote_accepted = True
        service_request.status = 'awaiting_deposit'
        db.session.commit()
        
        logger.info(f"Devis accepté pour demande {request_id} par {current_user.email}")
        flash('Devis accepté! Veuillez maintenant soumettre votre acompte.', 'success')
        return redirect(url_for('client.view_request', request_id=request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur acceptation devis {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('client.view_request', request_id=request_id))


# ==============================================================================
# SOUMISSION DE PAIEMENT
# ==============================================================================

@bp.route('/request/<int:request_id>/submit-payment', methods=['POST'])
@login_required
@client_required
def submit_payment(request_id):
    """
    Permet au client de soumettre une preuve de paiement.
    
    Crée un enregistrement Payment et change le statut de la demande.
    
    Args:
        request_id: ID de la demande
        
    Returns:
        Redirection vers la page de la demande
    """
    try:
        # Récupération et vérification de la demande
        service_request = ServiceRequest.query.filter_by(
            id=request_id, 
            user_id=current_user.id
        ).first_or_404()
        
        form = PaymentProofForm()
        
        if form.validate_on_submit():
            # Sauvegarde de la preuve de paiement
            proof_filename = None
            if form.proof_document.data:
                proof_filename = save_uploaded_file(
                    form.proof_document.data, 
                    current_app.config['UPLOAD_FOLDER']
                )
            
            # Création du paiement
            payment = Payment(
                request_id=request_id,
                amount=form.amount.data,
                payment_type='deposit',
                payment_method=form.payment_method.data,
                proof_document=proof_filename,
                transaction_reference=form.transaction_reference.data.strip() if form.transaction_reference.data else None,
                notes=form.notes.data.strip() if form.notes.data else None,
                status='pending'
            )
            
            db.session.add(payment)
            service_request.status = 'deposit_pending'
            db.session.commit()
            
            logger.info(f"Paiement soumis pour demande {request_id} par {current_user.email}")
            flash('Preuve de paiement soumise! En attente de vérification.', 'success')
        else:
            flash('Erreur lors de la soumission. Vérifiez les informations.', 'error')
        
        return redirect(url_for('client.view_request', request_id=request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur soumission paiement {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('client.view_request', request_id=request_id))


# ==============================================================================
# PROFIL UTILISATEUR
# ==============================================================================

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
@client_required
def profile():
    """
    Gère la page de profil de l'utilisateur.
    
    GET: Affiche le profil actuel
    POST: Met à jour les informations du profil
    
    Returns:
        Template du profil
    """
    try:
        if request.method == 'POST':
            # Mise à jour des informations
            current_user.first_name = request.form.get('first_name', current_user.first_name).strip()
            current_user.last_name = request.form.get('last_name', current_user.last_name).strip()
            current_user.phone = request.form.get('phone', current_user.phone)
            current_user.institution = request.form.get('institution', current_user.institution)
            current_user.academic_level = request.form.get('academic_level', current_user.academic_level)
            current_user.field_of_study = request.form.get('field_of_study', current_user.field_of_study)
            
            db.session.commit()
            
            logger.info(f"Profil mis à jour: {current_user.email}")
            flash('Profil mis à jour avec succès!', 'success')
        
        return render_template('client/profile.html')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur mise à jour profil {current_user.email}: {e}")
        flash('Une erreur est survenue.', 'error')
        return render_template('client/profile.html')
