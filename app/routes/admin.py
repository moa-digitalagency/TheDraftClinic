from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.request import ServiceRequest
from app.models.document import Document
from app.models.payment import Payment
from app.services.file_service import save_uploaded_file
from datetime import datetime

bp = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_requests = ServiceRequest.query.count()
    pending_requests = ServiceRequest.query.filter(ServiceRequest.status.in_(['submitted', 'under_review'])).count()
    in_progress = ServiceRequest.query.filter(ServiceRequest.status.in_(['in_progress', 'revision'])).count()
    pending_payments = Payment.query.filter_by(status='pending').count()
    total_users = User.query.filter_by(is_admin=False).count()
    
    recent_requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).limit(10).all()
    pending_payment_verifications = Payment.query.filter_by(status='pending').order_by(Payment.created_at.desc()).all()
    
    stats = {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'in_progress': in_progress,
        'pending_payments': pending_payments,
        'total_users': total_users
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_requests=recent_requests,
                         pending_payments=pending_payment_verifications)


@bp.route('/requests')
@login_required
@admin_required
def requests_list():
    status_filter = request.args.get('status', 'all')
    
    query = ServiceRequest.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    requests_list = query.order_by(ServiceRequest.created_at.desc()).all()
    statuses = ServiceRequest.STATUS_CHOICES
    
    return render_template('admin/requests_list.html', 
                         requests=requests_list, 
                         statuses=statuses,
                         current_filter=status_filter)


@bp.route('/request/<int:request_id>')
@login_required
@admin_required
def view_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    documents = Document.query.filter_by(request_id=request_id).all()
    payments = Payment.query.filter_by(request_id=request_id).order_by(Payment.created_at.desc()).all()
    
    return render_template('admin/view_request.html', 
                         request=service_request, 
                         documents=documents,
                         payments=payments)


@bp.route('/request/<int:request_id>/send-quote', methods=['POST'])
@login_required
@admin_required
def send_quote(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    quote_amount = float(request.form.get('quote_amount', 0))
    deposit_required = float(request.form.get('deposit_required', 0))
    quote_message = request.form.get('quote_message', '')
    
    service_request.quote_amount = quote_amount
    service_request.deposit_required = deposit_required
    service_request.quote_message = quote_message
    service_request.quote_sent_at = datetime.utcnow()
    service_request.status = 'quote_sent'
    
    db.session.commit()
    flash('Devis envoyé avec succès!', 'success')
    return redirect(url_for('admin.view_request', request_id=request_id))


@bp.route('/request/<int:request_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_status(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    new_status = request.form.get('status')
    progress = request.form.get('progress', type=int)
    admin_notes = request.form.get('admin_notes')
    
    if new_status:
        service_request.status = new_status
        if new_status == 'delivered':
            service_request.delivered_at = datetime.utcnow()
            service_request.progress_percentage = 100
    
    if progress is not None:
        service_request.progress_percentage = progress
    
    if admin_notes:
        service_request.admin_notes = admin_notes
    
    db.session.commit()
    flash('Statut mis à jour!', 'success')
    return redirect(url_for('admin.view_request', request_id=request_id))


@bp.route('/request/<int:request_id>/upload-deliverable', methods=['POST'])
@login_required
@admin_required
def upload_deliverable(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    if 'deliverable' in request.files:
        file = request.files['deliverable']
        if file and file.filename:
            saved_filename = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
            if saved_filename:
                doc = Document(
                    request_id=request_id,
                    filename=saved_filename,
                    original_filename=file.filename,
                    file_type=file.content_type,
                    document_type='deliverable',
                    description=request.form.get('description', ''),
                    uploaded_by=current_user.id
                )
                db.session.add(doc)
                db.session.commit()
                flash('Livrable uploadé avec succès!', 'success')
    
    return redirect(url_for('admin.view_request', request_id=request_id))


@bp.route('/payment/<int:payment_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    action = request.form.get('action')
    
    if action == 'approve':
        payment.status = 'verified'
        payment.verified_by = current_user.id
        payment.verified_at = datetime.utcnow()
        
        service_request = payment.request
        service_request.deposit_paid = True
        service_request.status = 'in_progress'
        
        flash('Paiement vérifié! La demande est maintenant en traitement.', 'success')
    
    elif action == 'reject':
        payment.status = 'rejected'
        payment.rejection_reason = request.form.get('rejection_reason', '')
        payment.verified_by = current_user.id
        payment.verified_at = datetime.utcnow()
        
        service_request = payment.request
        service_request.status = 'awaiting_deposit'
        
        flash('Paiement rejeté.', 'warning')
    
    db.session.commit()
    return redirect(url_for('admin.view_request', request_id=payment.request_id))


@bp.route('/users')
@login_required
@admin_required
def users_list():
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin/users_list.html', users=users)


@bp.route('/user/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    user_requests = ServiceRequest.query.filter_by(user_id=user_id).order_by(ServiceRequest.created_at.desc()).all()
    return render_template('admin/view_user.html', user=user, requests=user_requests)
