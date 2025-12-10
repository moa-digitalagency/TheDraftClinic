"""
================================================================================
TheDraftClinic - Database Initialization Script
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This script initializes the PostgreSQL database with all required tables
for the TheDraftClinic academic writing services platform.

Usage:
    python init_db.py
    python init_db.py --check    # Verify environment variables only
    python init_db.py --reset    # Reset database (DANGEROUS)

This will:
    - Verify all required environment variables
    - Create all database tables (users, service_requests, documents, payments)
    - Create a default admin user if ADMIN_EMAIL and ADMIN_PASSWORD are set
================================================================================
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def check_environment_variables():
    """
    Verify all required environment variables are set.
    
    Returns:
        tuple: (is_valid: bool, messages: list)
    """
    messages = []
    is_valid = True
    
    print("=" * 60)
    print("TheDraftClinic - Environment Variables Check")
    print("=" * 60)
    print()
    
    required_vars = {
        'DATABASE_URL': 'PostgreSQL connection URL',
        'SESSION_SECRET': 'Flask session secret key'
    }
    
    admin_vars = {
        'ADMIN_EMAIL': 'Administrator email address',
        'ADMIN_PASSWORD': 'Administrator password'
    }
    
    print("[1/3] Checking required environment variables...")
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            if var == 'DATABASE_URL':
                masked = value[:20] + '...' if len(value) > 20 else value
                print(f"      ✓ {var}: {masked}")
            else:
                print(f"      ✓ {var}: ***configured***")
            messages.append(f"✓ {var} is set")
        else:
            print(f"      ✗ {var}: NOT SET - {description}")
            messages.append(f"✗ {var} is MISSING - {description}")
            is_valid = False
    
    print()
    print("[2/3] Checking admin credentials...")
    admin_ready = True
    for var, description in admin_vars.items():
        value = os.environ.get(var)
        if value:
            if var == 'ADMIN_EMAIL':
                print(f"      ✓ {var}: {value}")
            else:
                print(f"      ✓ {var}: ***configured***")
            messages.append(f"✓ {var} is set")
        else:
            print(f"      ⚠ {var}: NOT SET - {description}")
            messages.append(f"⚠ {var} is not set (optional for admin creation)")
            admin_ready = False
    
    if admin_ready:
        print("      → Admin account will be created automatically")
    else:
        print("      → Admin account will NOT be created (set both ADMIN_EMAIL and ADMIN_PASSWORD)")
    
    print()
    print("[3/3] Validating admin credentials format...")
    
    admin_email = os.environ.get('ADMIN_EMAIL', '')
    admin_password = os.environ.get('ADMIN_PASSWORD', '')
    
    if admin_email:
        if '@' in admin_email and '.' in admin_email.split('@')[-1]:
            print(f"      ✓ ADMIN_EMAIL format is valid")
        else:
            print(f"      ⚠ ADMIN_EMAIL format may be invalid: {admin_email}")
            messages.append(f"⚠ ADMIN_EMAIL format may be invalid")
    
    if admin_password:
        if len(admin_password) >= 8:
            print(f"      ✓ ADMIN_PASSWORD length is sufficient ({len(admin_password)} chars)")
        else:
            print(f"      ⚠ ADMIN_PASSWORD is too short ({len(admin_password)} chars, minimum 8 recommended)")
            messages.append(f"⚠ ADMIN_PASSWORD is too short")
    
    print()
    return is_valid, messages


def init_database():
    """
    Initialize the database by creating all tables.
    
    This function creates the Flask application context and initializes
    all database tables defined in the models.
    
    Returns:
        bool: True if successful, False otherwise
    """
    is_valid, messages = check_environment_variables()
    
    if not is_valid:
        print("=" * 60)
        print("ERROR: Missing required environment variables!")
        print("Please set the following variables before running:")
        for msg in messages:
            if msg.startswith('✗'):
                print(f"  - {msg}")
        print("=" * 60)
        return False
    
    print("=" * 60)
    print("TheDraftClinic - Database Initialization")
    print("By MOA Digital Agency LLC")
    print("=" * 60)
    print()
    
    try:
        from app import create_app, db
        from models.user import User
        from models.request import ServiceRequest
        from models.document import Document
        from models.payment import Payment
        
        app = create_app()
        
        with app.app_context():
            print("[4/6] Creating all database tables...")
            db.create_all()
            print("      ✓ Table 'users' created")
            print("      ✓ Table 'service_requests' created")
            print("      ✓ Table 'documents' created")
            print("      ✓ Table 'payments' created")
            
            try:
                from models.activity_log import ActivityLog
                print("      ✓ Table 'activity_logs' created")
            except ImportError:
                pass
            
            try:
                from models.site_settings import SiteSettings
                print("      ✓ Table 'site_settings' created")
            except ImportError:
                pass
            
            try:
                from models.page import Page
                print("      ✓ Table 'pages' created")
            except ImportError:
                pass
            
            print()
            print("[5/6] Checking for default admin user...")
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@thedraftclinic.com')
            admin_password = os.environ.get('ADMIN_PASSWORD')
            
            existing_admin = User.query.filter_by(email=admin_email).first()
            
            if existing_admin:
                print(f"      ✓ Admin user already exists: {admin_email}")
            elif admin_password:
                admin = User(
                    email=admin_email,
                    first_name='Admin',
                    last_name='TheDraftClinic',
                    is_admin=True
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                print(f"      ✓ Created admin user: {admin_email}")
            else:
                print("      ⚠ No ADMIN_PASSWORD set - skipping admin creation")
                print("      → Set ADMIN_EMAIL and ADMIN_PASSWORD to create admin")
            
            print()
            print("[6/6] Verifying database tables...")
            tables_info = {
                'users': User.query.count(),
                'service_requests': ServiceRequest.query.count(),
                'documents': Document.query.count(),
                'payments': Payment.query.count()
            }
            
            for table, count in tables_info.items():
                print(f"      - {table}: {count} records")
            
            print()
            print("=" * 60)
            print("Database initialization completed successfully!")
            print("=" * 60)
            return True
            
    except Exception as e:
        print(f"ERROR: Database initialization failed!")
        print(f"Details: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    
    WARNING: This will delete all data in the database!
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("WARNING: This will delete all data in the database!")
    confirm = input("Are you sure? Type 'YES' to confirm: ")
    
    if confirm != 'YES':
        print("Operation cancelled.")
        return False
    
    try:
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            print("Dropping all tables...")
            db.drop_all()
            print("Creating all tables...")
            db.create_all()
            print("Database reset completed!")
            return True
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reset':
            reset_database()
        elif sys.argv[1] == '--check':
            is_valid, _ = check_environment_variables()
            sys.exit(0 if is_valid else 1)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python init_db.py [--check|--reset]")
            sys.exit(1)
    else:
        success = init_database()
        sys.exit(0 if success else 1)
