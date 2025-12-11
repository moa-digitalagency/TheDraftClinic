"""
================================================================================
TheDraftClinic - Routes Admin Settings
================================================================================
By MOA Digital Agency LLC
================================================================================

Routes pour la gestion des paramètres du site:
- Paramètres généraux (nom, description)
- Branding (logo, favicon)
- SEO et OpenGraph
- Informations légales
- Gestion des pages dynamiques
- Statistiques
================================================================================
"""

from flask import (
    Blueprint, render_template, redirect, url_for, 
    flash, request, current_app
)
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
import os
import logging

from app import db
from models.site_settings import SiteSettings
from models.page import Page
from models.request import ServiceRequest
from models.activity_log import ActivityLog
from models.user import User
from services.file_service import save_uploaded_file

logger = logging.getLogger(__name__)

bp = Blueprint('admin_settings', __name__)


def admin_required(f):
    """Décorateur vérifiant que l'utilisateur est administrateur."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/settings')
@login_required
@admin_required
def settings():
    """Affiche la page des paramètres du site."""
    settings = SiteSettings.get_settings()
    return render_template('admin/settings/index.html', settings=settings)


@bp.route('/settings/general', methods=['GET', 'POST'])
@login_required
@admin_required
def settings_general():
    """Gère les paramètres généraux du site."""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        settings.site_name = request.form.get('site_name', settings.site_name)
        settings.site_description = request.form.get('site_description', '')
        settings.timezone = request.form.get('timezone', 'Europe/Paris')
        settings.country = request.form.get('country', 'France')
        settings.default_language = request.form.get('default_language', 'fr')
        settings.currency = request.form.get('currency', 'EUR')
        
        db.session.commit()
        flash('Paramètres généraux mis à jour.', 'success')
        return redirect(url_for('admin_settings.settings'))
    
    return render_template('admin/settings/general.html', settings=settings)


@bp.route('/settings/branding', methods=['GET', 'POST'])
@login_required
@admin_required
def settings_branding():
    """Gère le branding (logo, favicon)."""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        branding_folder = os.path.join(
            current_app.config['UPLOAD_FOLDER'], 
            'branding'
        )
        os.makedirs(branding_folder, exist_ok=True)
        
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo and logo.filename:
                logo_filename = save_uploaded_file(logo, branding_folder)
                if logo_filename:
                    settings.logo_filename = logo_filename
        
        if 'favicon' in request.files:
            favicon = request.files['favicon']
            if favicon and favicon.filename:
                favicon_filename = save_uploaded_file(favicon, branding_folder)
                if favicon_filename:
                    settings.favicon_filename = favicon_filename
        
        db.session.commit()
        flash('Branding mis à jour.', 'success')
        return redirect(url_for('admin_settings.settings'))
    
    return render_template('admin/settings/branding.html', settings=settings)


@bp.route('/settings/seo', methods=['GET', 'POST'])
@login_required
@admin_required
def settings_seo():
    """Gère les paramètres SEO et OpenGraph."""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        settings.seo_title = request.form.get('seo_title', '')
        settings.seo_description = request.form.get('seo_description', '')
        settings.seo_keywords = request.form.get('seo_keywords', '')
        
        settings.og_title = request.form.get('og_title', '')
        settings.og_description = request.form.get('og_description', '')
        settings.og_type = request.form.get('og_type', 'website')
        
        settings.twitter_card = request.form.get('twitter_card', 'summary_large_image')
        settings.twitter_site = request.form.get('twitter_site', '')
        
        if 'og_image' in request.files:
            og_image = request.files['og_image']
            if og_image and og_image.filename:
                branding_folder = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], 
                    'branding'
                )
                og_image_filename = save_uploaded_file(og_image, branding_folder)
                if og_image_filename:
                    settings.og_image_filename = og_image_filename
        
        db.session.commit()
        flash('Paramètres SEO mis à jour.', 'success')
        return redirect(url_for('admin_settings.settings'))
    
    return render_template('admin/settings/seo.html', settings=settings)


@bp.route('/settings/legal', methods=['GET', 'POST'])
@login_required
@admin_required
def settings_legal():
    """Gère les informations légales."""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        settings.company_name = request.form.get('company_name', '')
        settings.company_address = request.form.get('company_address', '')
        settings.company_email = request.form.get('company_email', '')
        settings.company_phone = request.form.get('company_phone', '')
        settings.company_registration = request.form.get('company_registration', '')
        settings.vat_number = request.form.get('vat_number', '')
        
        settings.legal_status = request.form.get('legal_status', '')
        settings.share_capital = request.form.get('share_capital', '')
        settings.rcs_number = request.form.get('rcs_number', '')
        settings.siret_number = request.form.get('siret_number', '')
        settings.ape_code = request.form.get('ape_code', '')
        
        settings.hosting_provider = request.form.get('hosting_provider', '')
        settings.hosting_address = request.form.get('hosting_address', '')
        settings.dpo_name = request.form.get('dpo_name', '')
        settings.dpo_email = request.form.get('dpo_email', '')
        
        db.session.commit()
        flash('Informations légales mises à jour.', 'success')
        return redirect(url_for('admin_settings.settings'))
    
    return render_template('admin/settings/legal.html', settings=settings)


@bp.route('/settings/advanced', methods=['GET', 'POST'])
@login_required
@admin_required
def settings_advanced():
    """Gère les paramètres avancés (scripts, analytics)."""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        settings.google_analytics_id = request.form.get('google_analytics_id', '')
        settings.google_tag_manager_id = request.form.get('google_tag_manager_id', '')
        settings.facebook_pixel_id = request.form.get('facebook_pixel_id', '')
        
        settings.robots_txt_content = request.form.get('robots_txt_content', '')
        settings.custom_head_scripts = request.form.get('custom_head_scripts', '')
        settings.custom_body_scripts = request.form.get('custom_body_scripts', '')
        
        settings.maintenance_mode = 'maintenance_mode' in request.form
        settings.maintenance_message = request.form.get('maintenance_message', '')
        
        db.session.commit()
        flash('Paramètres avancés mis à jour.', 'success')
        return redirect(url_for('admin_settings.settings'))
    
    return render_template('admin/settings/advanced.html', settings=settings)


@bp.route('/pages')
@login_required
@admin_required
def pages_list():
    """Liste toutes les pages dynamiques."""
    pages = Page.query.order_by(Page.order_index, Page.created_at.desc()).all()
    return render_template('admin/pages/list.html', pages=pages)


@bp.route('/pages/new', methods=['GET', 'POST'])
@login_required
@admin_required
def page_new():
    """Crée une nouvelle page."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip() or Page.generate_slug(title)
        
        existing = Page.query.filter_by(slug=slug).first()
        if existing:
            flash('Ce slug est déjà utilisé.', 'error')
            return render_template('admin/pages/edit.html', page=None)
        
        page = Page(
            title=title,
            slug=slug,
            content=request.form.get('content', ''),
            content_format=request.form.get('content_format', 'html'),
            meta_title=request.form.get('meta_title', ''),
            meta_description=request.form.get('meta_description', ''),
            is_published='is_published' in request.form,
            show_in_footer='show_in_footer' in request.form,
            show_in_navigation='show_in_navigation' in request.form,
            order_index=int(request.form.get('order_index', 0)),
            page_type=request.form.get('page_type', 'custom'),
            created_by=current_user.id
        )
        
        db.session.add(page)
        db.session.commit()
        
        flash('Page créée avec succès.', 'success')
        return redirect(url_for('admin_settings.pages_list'))
    
    return render_template('admin/pages/edit.html', page=None)


@bp.route('/pages/<int:page_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def page_edit(page_id):
    """Modifie une page existante."""
    page = Page.query.get_or_404(page_id)
    
    if request.method == 'POST':
        page.title = request.form.get('title', page.title).strip()
        
        new_slug = request.form.get('slug', '').strip() or Page.generate_slug(page.title)
        if new_slug != page.slug:
            existing = Page.query.filter_by(slug=new_slug).first()
            if existing and existing.id != page_id:
                flash('Ce slug est déjà utilisé.', 'error')
                return render_template('admin/pages/edit.html', page=page)
            page.slug = new_slug
        
        page.content = request.form.get('content', '')
        page.content_format = request.form.get('content_format', 'html')
        page.meta_title = request.form.get('meta_title', '')
        page.meta_description = request.form.get('meta_description', '')
        page.is_published = 'is_published' in request.form
        page.show_in_footer = 'show_in_footer' in request.form
        page.show_in_navigation = 'show_in_navigation' in request.form
        page.order_index = int(request.form.get('order_index', 0))
        page.page_type = request.form.get('page_type', 'custom')
        
        db.session.commit()
        
        flash('Page mise à jour.', 'success')
        return redirect(url_for('admin_settings.pages_list'))
    
    return render_template('admin/pages/edit.html', page=page)


@bp.route('/pages/<int:page_id>/delete', methods=['POST'])
@login_required
@admin_required
def page_delete(page_id):
    """Supprime une page."""
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    
    flash('Page supprimée.', 'success')
    return redirect(url_for('admin_settings.pages_list'))


@bp.route('/stats')
@login_required
@admin_required
def statistics():
    """Affiche la page de statistiques et traçabilité."""
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    
    total_requests = ServiceRequest.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    
    completed_requests = ServiceRequest.query.filter(
        ServiceRequest.status.in_(['completed', 'delivered'])
    ).all()
    
    on_time_deliveries = 0
    late_deliveries = 0
    delivery_times = []
    
    for req in completed_requests:
        if req.delivered_at and req.deadline:
            if req.delivered_at <= req.deadline:
                on_time_deliveries += 1
            else:
                late_deliveries += 1
            
            if req.created_at:
                delta = (req.delivered_at - req.created_at).days
                delivery_times.append(delta)
    
    avg_delivery_time = sum(delivery_times) / len(delivery_times) if delivery_times else 0
    
    requests_by_status = {}
    for status_code, status_label in ServiceRequest.STATUS_CHOICES:
        count = ServiceRequest.query.filter_by(status=status_code).count()
        requests_by_status[status_label] = count
    
    requests_by_service = {}
    for service_code, service_label in ServiceRequest.SERVICE_TYPES:
        count = ServiceRequest.query.filter_by(service_type=service_code).count()
        if count > 0:
            requests_by_service[service_label] = count
    
    recent_activities = ActivityLog.query.order_by(
        ActivityLog.created_at.desc()
    ).limit(50).all()
    
    stats = {
        'total_requests': total_requests,
        'total_users': total_users,
        'completed_requests': len(completed_requests),
        'on_time_deliveries': on_time_deliveries,
        'late_deliveries': late_deliveries,
        'on_time_rate': (on_time_deliveries / (on_time_deliveries + late_deliveries) * 100) if (on_time_deliveries + late_deliveries) > 0 else 0,
        'avg_delivery_time': round(avg_delivery_time, 1),
        'requests_by_status': requests_by_status,
        'requests_by_service': requests_by_service
    }
    
    return render_template(
        'admin/stats.html', 
        stats=stats,
        recent_activities=recent_activities
    )


# ==============================================================================
# GESTION DES PAIEMENTS
# ==============================================================================

@bp.route('/payments')
@login_required
@admin_required
def payments_list():
    """Liste tous les paiements avec filtrage par statut."""
    from models.payment import Payment
    
    status_filter = request.args.get('status', 'all')
    
    query = Payment.query
    if status_filter == 'pending':
        query = query.filter_by(status='pending')
    elif status_filter == 'verified':
        query = query.filter_by(status='verified')
    elif status_filter == 'rejected':
        query = query.filter_by(status='rejected')
    
    payments = query.order_by(Payment.created_at.desc()).all()
    
    pending_count = Payment.query.filter_by(status='pending').count()
    verified_count = Payment.query.filter_by(status='verified').count()
    rejected_count = Payment.query.filter_by(status='rejected').count()
    
    return render_template(
        'admin/payments/list.html',
        payments=payments,
        current_filter=status_filter,
        pending_count=pending_count,
        verified_count=verified_count,
        rejected_count=rejected_count
    )


# ==============================================================================
# GESTION DES LANGUES
# ==============================================================================

@bp.route('/languages')
@login_required
@admin_required
def languages_list():
    """Liste toutes les langues disponibles."""
    import json
    from pathlib import Path
    
    lang_dir = Path('lang')
    languages = []
    
    for lang_file in lang_dir.glob('*.json'):
        lang_code = lang_file.stem
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def count_keys(obj, count=0):
                for key, value in obj.items():
                    if isinstance(value, dict):
                        count = count_keys(value, count)
                    else:
                        count += 1
                return count
            
            keys_count = count_keys(data)
            mod_time = datetime.fromtimestamp(lang_file.stat().st_mtime)
            
            languages.append({
                'code': lang_code,
                'name': data.get('language', {}).get(lang_code, lang_code.upper()),
                'keys_count': keys_count,
                'last_modified': mod_time
            })
        except Exception as e:
            logger.error(f"Erreur lecture fichier langue {lang_code}: {e}")
    
    return render_template('admin/languages/list.html', languages=languages)


@bp.route('/languages/<lang_code>')
@login_required
@admin_required
def language_view(lang_code):
    """Affiche et permet d'éditer les traductions d'une langue."""
    import json
    from pathlib import Path
    
    lang_file = Path(f'lang/{lang_code}.json')
    if not lang_file.exists():
        flash('Fichier de langue introuvable.', 'error')
        return redirect(url_for('admin_settings.languages_list'))
    
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)
    except Exception as e:
        flash('Erreur lors de la lecture du fichier.', 'error')
        return redirect(url_for('admin_settings.languages_list'))
    
    return render_template(
        'admin/languages/edit.html',
        lang_code=lang_code,
        translations=translations,
        translations_json=json.dumps(translations, indent=2, ensure_ascii=False)
    )


@bp.route('/languages/<lang_code>/save', methods=['POST'])
@login_required
@admin_required
def language_save(lang_code):
    """Sauvegarde les modifications de traduction."""
    import json
    from pathlib import Path
    
    lang_file = Path(f'lang/{lang_code}.json')
    
    try:
        json_content = request.form.get('translations_json', '')
        translations = json.loads(json_content)
        
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)
        
        from utils.i18n import reload_translations
        reload_translations()
        
        flash('Traductions mises à jour avec succès.', 'success')
    except json.JSONDecodeError:
        flash('Le JSON est invalide.', 'error')
    except Exception as e:
        logger.error(f"Erreur sauvegarde langue {lang_code}: {e}")
        flash('Une erreur est survenue.', 'error')
    
    return redirect(url_for('admin_settings.language_view', lang_code=lang_code))


@bp.route('/languages/<lang_code>/download')
@login_required
@admin_required
def language_download(lang_code):
    """Télécharge le fichier JSON d'une langue."""
    from flask import send_file
    from pathlib import Path
    
    lang_file = Path(f'lang/{lang_code}.json')
    if not lang_file.exists():
        flash('Fichier introuvable.', 'error')
        return redirect(url_for('admin_settings.languages_list'))
    
    return send_file(
        lang_file,
        as_attachment=True,
        download_name=f'{lang_code}.json',
        mimetype='application/json'
    )


@bp.route('/languages/<lang_code>/upload', methods=['POST'])
@login_required
@admin_required
def language_upload(lang_code):
    """Importe un fichier JSON pour une langue."""
    import json
    from pathlib import Path
    
    if 'file' not in request.files:
        flash('Aucun fichier fourni.', 'error')
        return redirect(url_for('admin_settings.language_view', lang_code=lang_code))
    
    file = request.files['file']
    if not file.filename.endswith('.json'):
        flash('Le fichier doit être au format JSON.', 'error')
        return redirect(url_for('admin_settings.language_view', lang_code=lang_code))
    
    try:
        content = file.read().decode('utf-8')
        translations = json.loads(content)
        
        lang_file = Path(f'lang/{lang_code}.json')
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)
        
        from utils.i18n import reload_translations
        reload_translations()
        
        flash('Fichier importé avec succès.', 'success')
    except json.JSONDecodeError:
        flash('Le JSON est invalide.', 'error')
    except Exception as e:
        logger.error(f"Erreur import langue {lang_code}: {e}")
        flash('Une erreur est survenue.', 'error')
    
    return redirect(url_for('admin_settings.language_view', lang_code=lang_code))
