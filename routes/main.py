"""
================================================================================
TheDraftClinic - Main Routes Module
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This module handles public-facing routes including the landing page,
services page, about page, and contact page.
================================================================================
"""

from flask import Blueprint, render_template
from models.request import ServiceRequest

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    services = ServiceRequest.SERVICE_TYPES
    return render_template('landing.html', services=services)


@bp.route('/services')
def services():
    services = ServiceRequest.SERVICE_TYPES
    return render_template('services.html', services=services)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/contact')
def contact():
    return render_template('contact.html')


@bp.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
