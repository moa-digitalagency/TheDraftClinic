"""
================================================================================
TheDraftClinic - Demo Data Initialization Script
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This script creates demo data to showcase all platform features.

Usage:
    python init_db_demo.py

This will create:
    - Demo users (clients)
    - Demo service requests with various statuses
    - Demo payments
    - Demo documents
================================================================================
"""

import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

def create_demo_data():
    """Create demo data for all platform features."""
    
    print("=" * 60)
    print("TheDraftClinic - Demo Data Creation")
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
            db.create_all()
            
            print("[1/5] Creating demo users...")
            demo_users = []
            
            users_data = [
                {
                    "email": "marie.dupont@university.fr",
                    "first_name": "Marie",
                    "last_name": "Dupont",
                    "phone": "+33 6 12 34 56 78",
                    "institution": "Université Paris-Saclay",
                    "academic_level": "Doctorat",
                    "field_of_study": "Sciences de l'éducation"
                },
                {
                    "email": "jean.martin@sorbonne.fr",
                    "first_name": "Jean",
                    "last_name": "Martin",
                    "phone": "+33 6 98 76 54 32",
                    "institution": "Sorbonne Université",
                    "academic_level": "Master 2",
                    "field_of_study": "Droit international"
                },
                {
                    "email": "sophie.bernard@lyon.fr",
                    "first_name": "Sophie",
                    "last_name": "Bernard",
                    "phone": "+33 6 45 67 89 01",
                    "institution": "Université Lyon 3",
                    "academic_level": "Master 1",
                    "field_of_study": "Sciences politiques"
                },
                {
                    "email": "pierre.leroy@grenoble.fr",
                    "first_name": "Pierre",
                    "last_name": "Leroy",
                    "phone": "+33 6 23 45 67 89",
                    "institution": "Université Grenoble Alpes",
                    "academic_level": "Licence 3",
                    "field_of_study": "Économie"
                },
                {
                    "email": "claire.moreau@toulouse.fr",
                    "first_name": "Claire",
                    "last_name": "Moreau",
                    "phone": "+33 6 34 56 78 90",
                    "institution": "Université Toulouse",
                    "academic_level": "Doctorat",
                    "field_of_study": "Psychologie cognitive"
                }
            ]
            
            for user_data in users_data:
                existing = User.query.filter_by(email=user_data["email"]).first()
                if existing:
                    demo_users.append(existing)
                    print(f"      ✓ User exists: {user_data['email']}")
                else:
                    user = User(
                        email=user_data["email"],
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        phone=user_data["phone"],
                        institution=user_data["institution"],
                        academic_level=user_data["academic_level"],
                        field_of_study=user_data["field_of_study"],
                        is_admin=False,
                        account_active=True
                    )
                    user.set_password("demo123")
                    db.session.add(user)
                    demo_users.append(user)
                    print(f"      ✓ Created: {user_data['first_name']} {user_data['last_name']}")
            
            db.session.commit()
            
            print()
            print("[2/5] Creating demo service requests...")
            
            requests_data = [
                {
                    "user_idx": 0,
                    "service_type": "thesis",
                    "title": "Thèse sur l'impact du numérique dans l'éducation",
                    "description": "Étude comparative des méthodes pédagogiques traditionnelles vs numériques dans l'enseignement supérieur français.",
                    "deadline": datetime.now() + timedelta(days=90),
                    "word_count": 80000,
                    "status": "in_progress",
                    "progress": 45,
                    "quote_amount": Decimal("2500.00"),
                    "deposit_required": Decimal("750.00")
                },
                {
                    "user_idx": 1,
                    "service_type": "memoir",
                    "title": "Mémoire sur le droit européen de la concurrence",
                    "description": "Analyse des récentes réformes du droit de la concurrence dans l'Union Européenne et leurs impacts sur les GAFAM.",
                    "deadline": datetime.now() + timedelta(days=45),
                    "word_count": 25000,
                    "status": "quote_sent",
                    "quote_amount": Decimal("800.00"),
                    "deposit_required": Decimal("240.00")
                },
                {
                    "user_idx": 2,
                    "service_type": "article",
                    "title": "Article scientifique sur la démocratie participative",
                    "description": "Publication pour revue internationale sur les nouvelles formes de participation citoyenne en Europe.",
                    "deadline": datetime.now() + timedelta(days=30),
                    "word_count": 8000,
                    "status": "submitted",
                    "quote_amount": None,
                    "deposit_required": None
                },
                {
                    "user_idx": 3,
                    "service_type": "correction",
                    "title": "Correction et mise en forme mémoire économie",
                    "description": "Relecture complète, correction orthographique et mise en page selon normes APA.",
                    "deadline": datetime.now() + timedelta(days=7),
                    "word_count": 15000,
                    "status": "deposit_paid",
                    "progress": 20,
                    "quote_amount": Decimal("350.00"),
                    "deposit_required": Decimal("100.00")
                },
                {
                    "user_idx": 4,
                    "service_type": "thesis",
                    "title": "Thèse en psychologie cognitive sur la mémoire de travail",
                    "description": "Recherche expérimentale sur les capacités de la mémoire de travail chez les adultes.",
                    "deadline": datetime.now() + timedelta(days=120),
                    "word_count": 100000,
                    "status": "completed",
                    "progress": 100,
                    "quote_amount": Decimal("3200.00"),
                    "deposit_required": Decimal("960.00")
                },
                {
                    "user_idx": 0,
                    "service_type": "article",
                    "title": "Article sur les MOOCs et l'apprentissage en ligne",
                    "description": "Étude de l'efficacité des cours en ligne ouverts et massifs.",
                    "deadline": datetime.now() + timedelta(days=21),
                    "word_count": 6000,
                    "status": "under_review",
                    "quote_amount": None,
                    "deposit_required": None
                }
            ]
            
            demo_requests = []
            for req_data in requests_data:
                user = demo_users[req_data["user_idx"]]
                
                existing = ServiceRequest.query.filter_by(
                    user_id=user.id,
                    title=req_data["title"]
                ).first()
                
                if existing:
                    demo_requests.append(existing)
                    print(f"      ✓ Request exists: {req_data['title'][:40]}...")
                else:
                    request = ServiceRequest(
                        user_id=user.id,
                        service_type=req_data["service_type"],
                        title=req_data["title"],
                        description=req_data["description"],
                        deadline=req_data["deadline"],
                        word_count=req_data["word_count"],
                        status=req_data["status"],
                        progress_percentage=req_data.get("progress", 0),
                        quote_amount=req_data["quote_amount"],
                        deposit_required=req_data["deposit_required"]
                    )
                    db.session.add(request)
                    demo_requests.append(request)
                    print(f"      ✓ Created: {req_data['title'][:40]}...")
            
            db.session.commit()
            
            print()
            print("[3/5] Creating demo payments...")
            
            payments_data = [
                {
                    "request_idx": 0,
                    "amount": Decimal("750.00"),
                    "payment_type": "deposit",
                    "status": "verified",
                    "reference": "PAY-2024-001"
                },
                {
                    "request_idx": 3,
                    "amount": Decimal("100.00"),
                    "payment_type": "deposit",
                    "status": "verified",
                    "reference": "PAY-2024-002"
                },
                {
                    "request_idx": 4,
                    "amount": Decimal("960.00"),
                    "payment_type": "deposit",
                    "status": "verified",
                    "reference": "PAY-2024-003"
                },
                {
                    "request_idx": 4,
                    "amount": Decimal("2240.00"),
                    "payment_type": "final",
                    "status": "verified",
                    "reference": "PAY-2024-004"
                },
                {
                    "request_idx": 1,
                    "amount": Decimal("240.00"),
                    "payment_type": "deposit",
                    "status": "pending",
                    "reference": "PAY-2024-005"
                }
            ]
            
            for pay_data in payments_data:
                request = demo_requests[pay_data["request_idx"]]
                
                existing = Payment.query.filter_by(
                    request_id=request.id,
                    transaction_reference=pay_data["reference"]
                ).first()
                
                if existing:
                    print(f"      ✓ Payment exists: {pay_data['reference']}")
                else:
                    payment = Payment(
                        request_id=request.id,
                        amount=pay_data["amount"],
                        payment_type=pay_data["payment_type"],
                        status=pay_data["status"],
                        transaction_reference=pay_data["reference"]
                    )
                    db.session.add(payment)
                    print(f"      ✓ Created: {pay_data['reference']} - {pay_data['amount']}€")
            
            db.session.commit()
            
            print()
            print("[4/5] Creating demo documents...")
            
            documents_data = [
                {
                    "request_idx": 0,
                    "filename": "plan_these_numerique.pdf",
                    "document_type": "deliverable",
                    "description": "Plan détaillé de la thèse - Version 1"
                },
                {
                    "request_idx": 0,
                    "filename": "chapitre_1_introduction.pdf",
                    "document_type": "deliverable",
                    "description": "Chapitre 1 - Introduction et cadre théorique"
                },
                {
                    "request_idx": 4,
                    "filename": "these_complete_finale.pdf",
                    "document_type": "deliverable",
                    "description": "Version finale de la thèse"
                },
                {
                    "request_idx": 3,
                    "filename": "memoire_original.docx",
                    "document_type": "client_upload",
                    "description": "Document original à corriger"
                }
            ]
            
            for doc_data in documents_data:
                request = demo_requests[doc_data["request_idx"]]
                
                existing = Document.query.filter_by(
                    request_id=request.id,
                    filename=doc_data["filename"]
                ).first()
                
                if existing:
                    print(f"      ✓ Document exists: {doc_data['filename']}")
                else:
                    document = Document(
                        request_id=request.id,
                        filename=doc_data["filename"],
                        original_filename=doc_data["filename"],
                        document_type=doc_data["document_type"],
                        description=doc_data.get("description"),
                        file_size=1024 * 100
                    )
                    db.session.add(document)
                    print(f"      ✓ Created: {doc_data['filename']}")
            
            db.session.commit()
            
            print()
            print("[5/5] Summary of demo data...")
            print(f"      - Users: {User.query.filter_by(is_admin=False).count()}")
            print(f"      - Service Requests: {ServiceRequest.query.count()}")
            print(f"      - Payments: {Payment.query.count()}")
            print(f"      - Documents: {Document.query.count()}")
            
            print()
            print("=" * 60)
            print("Demo data creation completed successfully!")
            print()
            print("Demo user credentials (password: demo123):")
            for user in demo_users:
                print(f"  - {user.email}")
            print("=" * 60)
            return True
            
    except Exception as e:
        print(f"ERROR: Demo data creation failed!")
        print(f"Details: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = create_demo_data()
    sys.exit(0 if success else 1)
