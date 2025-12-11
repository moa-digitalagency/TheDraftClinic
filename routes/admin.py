"""
================================================================================
TheDraftClinic - Routes Administrateur
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

Ce module gère toutes les routes du panel administrateur:
- Dashboard admin avec statistiques globales
- Gestion des demandes (liste, détail, devis, statut)
- Vérification des paiements
- Gestion des utilisateurs
- Upload des livrables

Sécurité:
- Toutes les routes nécessitent une authentification admin
- Logging complet des actions administratives
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
from datetime import datetime
import logging

from app import db
from models.user import User
from models.request import ServiceRequest
from models.document import Document
from models.payment import Payment
from models.activity_log import ActivityLog
from models.deadline_extension import DeadlineExtension
from models.revision_request import RevisionRequest
from services.file_service import save_uploaded_file

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)

# Création du blueprint admin
bp = Blueprint('admin', __name__)


# ==============================================================================
# DÉCORATEUR ADMIN REQUIRED
# ==============================================================================

def admin_required(f):
    """
    Décorateur vérifiant que l'utilisateur est administrateur.
    
    Combine la vérification d'authentification et de statut admin.
    Redirige vers l'accueil si l'utilisateur n'est pas admin.
    
    Args:
        f: La fonction à décorer
        
    Returns:
        function: La fonction décorée
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérification d'authentification
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Vérification du statut admin
        if not current_user.is_admin:
            logger.warning(f"Accès admin refusé pour: {current_user.email}")
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# DASHBOARD ADMIN
# ==============================================================================

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Affiche le tableau de bord administrateur.
    
    Présente:
    - Statistiques globales (demandes, utilisateurs, paiements)
    - Demandes récentes
    - Paiements en attente de vérification
    
    Returns:
        Template dashboard admin
    """
    try:
        # Calcul des statistiques
        total_requests = ServiceRequest.query.count()
        pending_requests = ServiceRequest.query.filter(
            ServiceRequest.status.in_(['submitted', 'under_review'])
        ).count()
        in_progress = ServiceRequest.query.filter(
            ServiceRequest.status.in_(['in_progress', 'revision'])
        ).count()
        pending_payments = Payment.query.filter_by(status='pending').count()
        total_users = User.query.filter_by(is_admin=False).count()
        
        # Demandes récentes
        recent_requests = ServiceRequest.query.order_by(
            ServiceRequest.created_at.desc()
        ).limit(10).all()
        
        # Paiements en attente
        pending_payment_verifications = Payment.query.filter_by(
            status='pending'
        ).order_by(Payment.created_at.desc()).all()
        
        stats = {
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'in_progress': in_progress,
            'pending_payments': pending_payments,
            'total_users': total_users
        }
        
        recent_activities = ActivityLog.query.order_by(
            ActivityLog.created_at.desc()
        ).limit(10).all()
        
        return render_template(
            'admin/dashboard.html', 
            stats=stats, 
            recent_requests=recent_requests,
            pending_payments=pending_payment_verifications,
            recent_activities=recent_activities
        )
        
    except Exception as e:
        logger.error(f"Erreur dashboard admin: {e}")
        flash('Une erreur est survenue.', 'error')
        return render_template('admin/dashboard.html', stats={}, recent_requests=[], pending_payments=[])


# ==============================================================================
# LISTE DES DEMANDES
# ==============================================================================

@bp.route('/requests')
@login_required
@admin_required
def requests_list():
    """
    Affiche la liste de toutes les demandes avec filtrage par statut.
    
    Query params:
        status: Filtre par statut (optionnel)
        
    Returns:
        Template liste des demandes
    """
    try:
        # Récupération du filtre de statut
        status_filter = request.args.get('status', 'all')
        
        # Construction de la requête
        query = ServiceRequest.query
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        # Exécution avec tri
        requests_list = query.order_by(ServiceRequest.created_at.desc()).all()
        
        # Liste des statuts pour le filtre
        statuses = ServiceRequest.STATUS_CHOICES
        
        return render_template(
            'admin/requests_list.html', 
            requests=requests_list, 
            statuses=statuses,
            current_filter=status_filter
        )
        
    except Exception as e:
        logger.error(f"Erreur liste demandes: {e}")
        flash('Une erreur est survenue.', 'error')
        return render_template('admin/requests_list.html', requests=[], statuses=[], current_filter='all')


# ==============================================================================
# DÉTAIL D'UNE DEMANDE (ADMIN)
# ==============================================================================

@bp.route('/request/<int:request_id>')
@login_required
@admin_required
def view_request(request_id):
    """
    Affiche les détails complets d'une demande pour l'admin.
    
    Inclut:
    - Informations du client
    - Documents uploadés
    - Historique des paiements
    - Formulaires d'action (devis, statut, livrable)
    
    Args:
        request_id: ID de la demande
        
    Returns:
        Template détail demande admin
    """
    try:
        service_request = ServiceRequest.query.get_or_404(request_id)
        documents = Document.query.filter_by(request_id=request_id).all()
        payments = Payment.query.filter_by(request_id=request_id).order_by(
            Payment.created_at.desc()
        ).all()
        
        return render_template(
            'admin/view_request.html', 
            request=service_request, 
            documents=documents,
            payments=payments
        )
        
    except Exception as e:
        logger.error(f"Erreur affichage demande admin {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.requests_list'))


# ==============================================================================
# ENVOI D'UN DEVIS
# ==============================================================================

@bp.route('/request/<int:request_id>/send-quote', methods=['POST'])
@login_required
@admin_required
def send_quote(request_id):
    """
    Envoie un devis pour une demande.
    
    Args:
        request_id: ID de la demande
        
    Form data:
        quote_amount: Montant total du devis
        deposit_required: Montant de l'acompte
        quote_message: Message accompagnant le devis
        
    Returns:
        Redirection vers la page de la demande
    """
    try:
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Récupération des données du formulaire
        quote_amount = float(request.form.get('quote_amount', 0))
        deposit_required = float(request.form.get('deposit_required', 0))
        quote_message = request.form.get('quote_message', '').strip()
        
        # Mise à jour de la demande
        service_request.quote_amount = quote_amount
        service_request.deposit_required = deposit_required
        service_request.quote_message = quote_message
        service_request.quote_sent_at = datetime.utcnow()
        service_request.status = 'quote_sent'
        
        db.session.commit()
        
        logger.info(f"Devis envoyé pour demande {request_id} par {current_user.email}: {quote_amount}€")
        flash('Devis envoyé avec succès!', 'success')
        return redirect(url_for('admin.view_request', request_id=request_id))
        
    except ValueError as e:
        flash('Montant invalide.', 'error')
        return redirect(url_for('admin.view_request', request_id=request_id))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur envoi devis {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.view_request', request_id=request_id))


# ==============================================================================
# MISE À JOUR DU STATUT
# ==============================================================================

@bp.route('/request/<int:request_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_status(request_id):
    """
    Met à jour le statut et la progression d'une demande.
    
    Args:
        request_id: ID de la demande
        
    Form data:
        status: Nouveau statut
        progress: Pourcentage de progression
        admin_notes: Notes internes
        
    Returns:
        Redirection vers la page de la demande
    """
    try:
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Récupération et application des modifications
        new_status = request.form.get('status')
        progress = request.form.get('progress', type=int)
        admin_notes = request.form.get('admin_notes', '').strip()
        
        old_status = service_request.status
        
        if new_status:
            service_request.status = new_status
            if new_status == 'delivered':
                service_request.delivered_at = datetime.utcnow()
                service_request.progress_percentage = 100
        
        if progress is not None:
            service_request.progress_percentage = progress
        
        if admin_notes:
            service_request.admin_notes = admin_notes
        
        if new_status and new_status != old_status:
            ActivityLog.log_action(
                request_id=request_id,
                user_id=current_user.id,
                action_type='status_change',
                title='Changement de statut',
                description=f"Statut modifié: {service_request.get_status_display()}",
                metadata={'old_status': old_status, 'new_status': new_status},
                visible_to_client=True
            )
        
        if progress is not None:
            ActivityLog.log_action(
                request_id=request_id,
                user_id=current_user.id,
                action_type='progress_update',
                title='Mise à jour progression',
                description=f"Progression: {progress}%",
                metadata={'progress': progress},
                visible_to_client=True
            )
        
        db.session.commit()
        
        logger.info(f"Statut mis à jour pour demande {request_id}: {new_status} par {current_user.email}")
        flash('Statut mis à jour!', 'success')
        return redirect(url_for('admin.view_request', request_id=request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur mise à jour statut {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.view_request', request_id=request_id))


# ==============================================================================
# UPLOAD DE LIVRABLE
# ==============================================================================

@bp.route('/request/<int:request_id>/upload-deliverable', methods=['POST'])
@login_required
@admin_required
def upload_deliverable(request_id):
    """
    Upload un fichier livrable pour une demande.
    
    Args:
        request_id: ID de la demande
        
    Returns:
        Redirection vers la page de la demande
    """
    try:
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        if 'deliverable' in request.files:
            file = request.files['deliverable']
            if file and file.filename:
                saved_filename = save_uploaded_file(
                    file, 
                    current_app.config['UPLOAD_FOLDER']
                )
                if saved_filename:
                    delivery_comment = request.form.get('delivery_comment', '').strip()
                    
                    doc = Document(
                        request_id=request_id,
                        filename=saved_filename,
                        original_filename=file.filename,
                        file_type=file.content_type,
                        document_type='deliverable',
                        description=delivery_comment,
                        uploaded_by=current_user.id
                    )
                    db.session.add(doc)
                    
                    ActivityLog.log_action(
                        request_id=request_id,
                        user_id=current_user.id,
                        action_type='delivery',
                        title='Livraison du travail',
                        description=delivery_comment or 'Un nouveau livrable a été uploadé.',
                        metadata={'document_filename': file.filename},
                        visible_to_client=True
                    )
                    
                    db.session.commit()
                    
                    logger.info(f"Livrable uploadé pour demande {request_id} par {current_user.email}")
                    flash('Livrable uploadé avec succès!', 'success')
        
        return redirect(url_for('admin.view_request', request_id=request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur upload livrable {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.view_request', request_id=request_id))


# ==============================================================================
# VÉRIFICATION DE PAIEMENT
# ==============================================================================

@bp.route('/payment/<int:payment_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_payment(payment_id):
    """
    Vérifie (approuve ou rejette) un paiement.
    
    Args:
        payment_id: ID du paiement
        
    Form data:
        action: 'approve' ou 'reject'
        rejection_reason: Raison du rejet (si rejeté)
        
    Returns:
        Redirection vers la page de la demande
    """
    try:
        payment = Payment.query.get_or_404(payment_id)
        action = request.form.get('action')
        
        if action == 'approve':
            # Approbation du paiement
            payment.status = 'verified'
            payment.verified_by = current_user.id
            payment.verified_at = datetime.utcnow()
            
            # Mise à jour de la demande
            service_request = payment.request
            service_request.deposit_paid = True
            service_request.status = 'in_progress'
            
            logger.info(f"Paiement {payment_id} approuvé par {current_user.email}")
            flash('Paiement vérifié! La demande est maintenant en traitement.', 'success')
        
        elif action == 'reject':
            # Rejet du paiement
            payment.status = 'rejected'
            payment.rejection_reason = request.form.get('rejection_reason', '').strip()
            payment.verified_by = current_user.id
            payment.verified_at = datetime.utcnow()
            
            # Retour au statut précédent
            service_request = payment.request
            service_request.status = 'awaiting_deposit'
            
            logger.info(f"Paiement {payment_id} rejeté par {current_user.email}")
            flash('Paiement rejeté.', 'warning')
        
        db.session.commit()
        return redirect(url_for('admin.view_request', request_id=payment.request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur vérification paiement {payment_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.dashboard'))


# ==============================================================================
# LISTE DES UTILISATEURS
# ==============================================================================

@bp.route('/users')
@login_required
@admin_required
def users_list():
    """
    Affiche la liste de tous les utilisateurs (clients).
    
    Returns:
        Template liste utilisateurs
    """
    try:
        users = User.query.filter_by(is_admin=False).order_by(
            User.created_at.desc()
        ).all()
        
        return render_template('admin/users_list.html', users=users)
        
    except Exception as e:
        logger.error(f"Erreur liste utilisateurs: {e}")
        flash('Une erreur est survenue.', 'error')
        return render_template('admin/users_list.html', users=[])


# ==============================================================================
# DÉTAIL D'UN UTILISATEUR
# ==============================================================================

@bp.route('/user/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """
    Affiche les détails d'un utilisateur et ses demandes.
    
    Args:
        user_id: ID de l'utilisateur
        
    Returns:
        Template détail utilisateur
    """
    try:
        user = User.query.get_or_404(user_id)
        user_requests = ServiceRequest.query.filter_by(user_id=user_id).order_by(
            ServiceRequest.created_at.desc()
        ).all()
        
        return render_template('admin/view_user.html', user=user, requests=user_requests)
        
    except Exception as e:
        logger.error(f"Erreur affichage utilisateur {user_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.users_list'))


@bp.route('/request/<int:request_id>/add-comment', methods=['POST'])
@login_required
@admin_required
def add_comment(request_id):
    """Ajoute un commentaire à une demande."""
    try:
        service_request = ServiceRequest.query.get_or_404(request_id)
        comment = request.form.get('comment', '').strip()
        
        if comment:
            ActivityLog.log_action(
                request_id=request_id,
                user_id=current_user.id,
                action_type='comment',
                title='Commentaire de l\'équipe',
                description=comment,
                visible_to_client=True
            )
            db.session.commit()
            flash('Commentaire ajouté.', 'success')
        
        return redirect(url_for('admin.view_request', request_id=request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur ajout commentaire {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.view_request', request_id=request_id))


@bp.route('/request/<int:request_id>/request-deadline-extension', methods=['POST'])
@login_required
@admin_required
def request_deadline_extension(request_id):
    """Demande une extension de délai (doit être validée par le client)."""
    try:
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        new_deadline_str = request.form.get('new_deadline', '')
        reason = request.form.get('reason', '').strip()
        
        if not new_deadline_str:
            flash('Veuillez spécifier une nouvelle date.', 'error')
            return redirect(url_for('admin.view_request', request_id=request_id))
        
        new_deadline = datetime.strptime(new_deadline_str, '%Y-%m-%dT%H:%M')
        
        extension = DeadlineExtension(
            request_id=request_id,
            requested_by=current_user.id,
            original_deadline=service_request.deadline,
            new_deadline=new_deadline,
            reason=reason,
            status='pending'
        )
        db.session.add(extension)
        
        ActivityLog.log_action(
            request_id=request_id,
            user_id=current_user.id,
            action_type='deadline_extension_request',
            title='Demande d\'extension de délai',
            description=f"Nouvelle date proposée: {new_deadline.strftime('%d/%m/%Y %H:%M')}. Raison: {reason}",
            visible_to_client=True
        )
        
        db.session.commit()
        flash('Demande d\'extension envoyée au client.', 'success')
        return redirect(url_for('admin.view_request', request_id=request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur demande extension {request_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.view_request', request_id=request_id))


@bp.route('/revision/<int:revision_id>/handle', methods=['POST'])
@login_required
@admin_required
def handle_revision(revision_id):
    """Traite une demande de révision."""
    try:
        revision = RevisionRequest.query.get_or_404(revision_id)
        action = request.form.get('action')
        response = request.form.get('response', '').strip()
        
        if action == 'accept':
            revision.status = 'in_progress'
            revision.admin_response = response
            revision.responded_by = current_user.id
            revision.responded_at = datetime.utcnow()
            
            revision.service_request.status = 'revision'
            
            ActivityLog.log_action(
                request_id=revision.request_id,
                user_id=current_user.id,
                action_type='comment',
                title='Révision acceptée',
                description=response or 'La demande de révision a été acceptée.',
                visible_to_client=True
            )
            
            flash('Révision acceptée.', 'success')
            
        elif action == 'complete':
            revision.status = 'completed'
            revision.responded_at = datetime.utcnow()
            
            ActivityLog.log_action(
                request_id=revision.request_id,
                user_id=current_user.id,
                action_type='revision_delivery',
                title='Révision terminée',
                description='La révision demandée a été effectuée.',
                visible_to_client=True
            )
            
            flash('Révision terminée.', 'success')
            
        elif action == 'reject':
            revision.status = 'rejected'
            revision.admin_response = response
            revision.responded_by = current_user.id
            revision.responded_at = datetime.utcnow()
            
            ActivityLog.log_action(
                request_id=revision.request_id,
                user_id=current_user.id,
                action_type='comment',
                title='Révision refusée',
                description=response or 'La demande de révision a été refusée.',
                visible_to_client=True
            )
            
            flash('Révision refusée.', 'warning')
        
        db.session.commit()
        return redirect(url_for('admin.view_request', request_id=revision.request_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur traitement révision {revision_id}: {e}")
        flash('Une erreur est survenue.', 'error')
        return redirect(url_for('admin.dashboard'))


# ==============================================================================
# GESTION DES ADMINISTRATEURS (SUPER ADMIN UNIQUEMENT)
# ==============================================================================

def super_admin_required(f):
    """
    Décorateur vérifiant que l'utilisateur est super administrateur.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        
        if not current_user.is_super_admin:
            flash('Cette fonctionnalité est réservée au super administrateur.', 'error')
            return redirect(url_for('admin.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/admins')
@login_required
@super_admin_required
def list_admins():
    """
    Liste tous les administrateurs (super admin uniquement).
    """
    admins = User.query.filter_by(is_admin=True).order_by(User.created_at.asc()).all()
    return render_template('admin/admins/list.html', admins=admins)


@bp.route('/admins/new', methods=['GET', 'POST'])
@login_required
@super_admin_required
def create_admin():
    """
    Créer un nouveau compte administrateur.
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        password = request.form.get('password', '')
        admin_role = request.form.get('admin_role', 'admin')
        
        if not all([email, first_name, last_name, password]):
            flash('Tous les champs sont requis.', 'error')
            return render_template('admin/admins/create.html')
        
        if User.query.filter_by(email=email).first():
            flash('Un compte avec cet email existe déjà.', 'error')
            return render_template('admin/admins/create.html')
        
        if len(password) < 8:
            flash('Le mot de passe doit contenir au moins 8 caractères.', 'error')
            return render_template('admin/admins/create.html')
        
        try:
            new_admin = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_admin=True,
                admin_role=admin_role,
                account_active=True
            )
            new_admin.set_password(password)
            db.session.add(new_admin)
            db.session.commit()
            
            logger.info(f"Nouvel admin créé par {current_user.email}: {email}")
            flash(f'Administrateur {email} créé avec succès.', 'success')
            return redirect(url_for('admin.list_admins'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur création admin: {e}")
            flash('Erreur lors de la création.', 'error')
    
    return render_template('admin/admins/create.html')


@bp.route('/admins/<int:admin_id>/edit', methods=['GET', 'POST'])
@login_required
@super_admin_required
def edit_admin(admin_id):
    """
    Modifier un compte administrateur.
    """
    admin = User.query.get_or_404(admin_id)
    
    if not admin.is_admin:
        flash('Cet utilisateur n\'est pas un administrateur.', 'error')
        return redirect(url_for('admin.list_admins'))
    
    if admin.id == current_user.id:
        flash('Vous ne pouvez pas modifier votre propre compte ici.', 'warning')
        return redirect(url_for('admin.list_admins'))
    
    if request.method == 'POST':
        admin_role = request.form.get('admin_role', 'admin')
        account_active = request.form.get('account_active') == 'on'
        new_password = request.form.get('new_password', '').strip()
        
        try:
            admin.admin_role = admin_role
            admin.account_active = account_active
            
            if new_password:
                if len(new_password) < 8:
                    flash('Le mot de passe doit contenir au moins 8 caractères.', 'error')
                    return render_template('admin/admins/edit.html', admin=admin)
                admin.set_password(new_password)
            
            db.session.commit()
            logger.info(f"Admin {admin.email} modifié par {current_user.email}")
            flash('Administrateur modifié avec succès.', 'success')
            return redirect(url_for('admin.list_admins'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur modification admin: {e}")
            flash('Erreur lors de la modification.', 'error')
    
    return render_template('admin/admins/edit.html', admin=admin)


@bp.route('/admins/<int:admin_id>/toggle-status', methods=['POST'])
@login_required
@super_admin_required
def toggle_admin_status(admin_id):
    """
    Activer/désactiver un compte administrateur.
    """
    admin = User.query.get_or_404(admin_id)
    
    if admin.id == current_user.id:
        flash('Vous ne pouvez pas désactiver votre propre compte.', 'error')
        return redirect(url_for('admin.list_admins'))
    
    if not admin.is_admin:
        flash('Cet utilisateur n\'est pas un administrateur.', 'error')
        return redirect(url_for('admin.list_admins'))
    
    try:
        admin.account_active = not admin.account_active
        db.session.commit()
        
        status = 'activé' if admin.account_active else 'désactivé'
        logger.info(f"Admin {admin.email} {status} par {current_user.email}")
        flash(f'Compte {admin.email} {status}.', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erreur toggle admin status: {e}")
        flash('Erreur lors de l\'opération.', 'error')
    
    return redirect(url_for('admin.list_admins'))
