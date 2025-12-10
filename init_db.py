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

This will:
    - Create all database tables (users, service_requests, documents, payments)
    - Create a default admin user if ADMIN_EMAIL and ADMIN_PASSWORD are set
================================================================================
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.request import ServiceRequest
from app.models.document import Document
from app.models.payment import Payment


def init_database():
    """
    Initialize the database by creating all tables.
    
    This function creates the Flask application context and initializes
    all database tables defined in the models.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("=" * 60)
    print("TheDraftClinic - Database Initialization")
    print("By MOA Digital Agency LLC")
    print("=" * 60)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            print("[1/4] Dropping existing tables (if any)...")
            
            print("[2/4] Creating all database tables...")
            db.create_all()
            print("      - Table 'users' created")
            print("      - Table 'service_requests' created")
            print("      - Table 'documents' created")
            print("      - Table 'payments' created")
            
            print("[3/4] Checking for default admin user...")
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@thedraftclinic.com')
            admin_password = os.environ.get('ADMIN_PASSWORD')
            
            existing_admin = User.query.filter_by(email=admin_email).first()
            
            if existing_admin:
                print(f"      Admin user already exists: {admin_email}")
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
                print(f"      Created admin user: {admin_email}")
            else:
                print("      No ADMIN_PASSWORD set - skipping admin creation")
                print("      Set ADMIN_EMAIL and ADMIN_PASSWORD environment variables")
            
            print("[4/4] Verifying database tables...")
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
    
    app = create_app()
    
    with app.app_context():
        try:
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
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        init_database()
