"""
================================================================================
TheDraftClinic - Client Routes Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module handles all client-facing routes including dashboard,
service request submission, payment submission, and profile management.
================================================================================
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models.request import ServiceRequest
from models.document import Document
from models.payment import Payment
from utils.forms import ServiceRequestForm, PaymentProofForm
from services.file_service import save_uploaded_file
import os

bp = Blueprint('client', __name__)


def client_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/dashboard')
@login_required
@client_required
def dashboard():
    requests = ServiceRequest.query.filter_by(user_id=current_user.id).order_by(ServiceRequest.created_at.desc()).all()
    
    stats = {
        'total': len(requests),
        'in_progress': len([r for r in requests if r.status in ['in_progress', 'revision']]),
        'pending_quote': len([r for r in requests if r.status in ['submitted', 'under_review', 'quote_sent']]),
        'completed': len([r for r in requests if r.status in ['completed', 'delivered']])
    }
    
    return render_template('client/dashboard.html', requests=requests, stats=stats)


@bp.route('/new-request', methods=['GET', 'POST'])
@login_required
@client_required
def new_request():
    form = ServiceRequestForm()
    
    if form.validate_on_submit():
        service_request = ServiceRequest(
            user_id=current_user.id,
            service_type=form.service_type.data,
            title=form.title.data,
            description=form.description.data,
            additional_info=form.additional_info.data,
            word_count=form.word_count.data,
            pages_count=form.pages_count.data,
            deadline=form.deadline.data,
            urgency_level=form.urgency_level.data,
            status='submitted'
        )
        
        db.session.add(service_request)
        db.session.commit()
        
        if form.documents.data:
            for file in request.files.getlist('documents'):
                if file and file.filename:
                    saved_filename = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
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
        
        db.session.commit()
        flash('Votre demande a été soumise avec succès!', 'success')
        return redirect(url_for('client.view_request', request_id=service_request.id))
    
    return render_template('client/new_request.html', form=form, service_types=ServiceRequest.SERVICE_TYPES)


@bp.route('/request/<int:request_id>')
@login_required
@client_required
def view_request(request_id):
    service_request = ServiceRequest.query.filter_by(id=request_id, user_id=current_user.id).first_or_404()
    documents = Document.query.filter_by(request_id=request_id).all()
    payments = Payment.query.filter_by(request_id=request_id).order_by(Payment.created_at.desc()).all()
    payment_form = PaymentProofForm()
    
    return render_template('client/view_request.html', 
                         request=service_request, 
                         documents=documents, 
                         payments=payments,
                         payment_form=payment_form)


@bp.route('/request/<int:request_id>/accept-quote', methods=['POST'])
@login_required
@client_required
def accept_quote(request_id):
    service_request = ServiceRequest.query.filter_by(id=request_id, user_id=current_user.id).first_or_404()
    
    if service_request.status != 'quote_sent':
        flash('Cette action n\'est pas possible pour cette demande.', 'error')
        return redirect(url_for('client.view_request', request_id=request_id))
    
    service_request.quote_accepted = True
    service_request.status = 'awaiting_deposit'
    db.session.commit()
    
    flash('Devis accepté! Veuillez maintenant soumettre votre acompte.', 'success')
    return redirect(url_for('client.view_request', request_id=request_id))


@bp.route('/request/<int:request_id>/submit-payment', methods=['POST'])
@login_required
@client_required
def submit_payment(request_id):
    service_request = ServiceRequest.query.filter_by(id=request_id, user_id=current_user.id).first_or_404()
    form = PaymentProofForm()
    
    if form.validate_on_submit():
        proof_filename = None
        if form.proof_document.data:
            proof_filename = save_uploaded_file(form.proof_document.data, current_app.config['UPLOAD_FOLDER'])
        
        payment = Payment(
            request_id=request_id,
            amount=form.amount.data,
            payment_type='deposit',
            payment_method=form.payment_method.data,
            proof_document=proof_filename,
            transaction_reference=form.transaction_reference.data,
            notes=form.notes.data,
            status='pending'
        )
        
        db.session.add(payment)
        service_request.status = 'deposit_pending'
        db.session.commit()
        
        flash('Preuve de paiement soumise! En attente de vérification.', 'success')
    else:
        flash('Erreur lors de la soumission. Vérifiez les informations.', 'error')
    
    return redirect(url_for('client.view_request', request_id=request_id))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
@client_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        current_user.last_name = request.form.get('last_name', current_user.last_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.institution = request.form.get('institution', current_user.institution)
        current_user.academic_level = request.form.get('academic_level', current_user.academic_level)
        current_user.field_of_study = request.form.get('field_of_study', current_user.field_of_study)
        
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
    
    return render_template('client/profile.html')
