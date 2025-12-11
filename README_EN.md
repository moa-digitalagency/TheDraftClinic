# TheDraftClinic

> Academic writing services platform

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## About

TheDraftClinic is a professional web platform designed for doctoral candidates and researchers who wish to entrust their academic writing projects. Whether it's theses, dissertations, research proposals, scientific articles, or book chapters, our platform offers a complete and secure solution.

### Main features

| Feature | Description |
|---------|-------------|
| Request submission | Detailed form to submit academic projects |
| Quote system | Receive and accept personalized quotes |
| Payment management | Upload payment proofs with admin verification |
| Dashboard | Real-time tracking of project progress |
| User management | Registration, login, and profile management |
| Admin panel | Complete interface for request management |
| Full traceability | History of all actions (deliveries, downloads, revisions) |
| Revision system | Modification requests with attached files |
| Deadline extensions | Request and validate deadline extensions |
| Site settings | Logo, favicon, SEO, legal information |
| Dynamic pages | Customizable terms of service, privacy policy |
| Statistics | Stats dashboard with performance metrics |

---

## Technologies used

### Backend
- Python 3.11 - Main programming language
- Flask - Lightweight and powerful web framework
- SQLAlchemy - ORM for database management
- Flask-Login - Authentication management
- Flask-WTF - CSRF protection and form validation
- Gunicorn - WSGI server for production

### Frontend
- TailwindCSS - Utility-first CSS framework (via CDN)
- Jinja2 - Template engine
- JavaScript - Client-side interactions

### Database
- PostgreSQL - Robust relational database

---

## Project structure

```
TheDraftClinic/
├── app.py                   # Flask configuration and initialization
├── main.py                  # Application entry point
├── init_db.py               # Database initialization script
├── models/                  # SQLAlchemy data models
│   ├── __init__.py
│   ├── user.py              # User model with admin roles
│   ├── request.py           # Service request model
│   ├── document.py          # Document model
│   ├── payment.py           # Payment model
│   ├── activity_log.py      # Activity log model
│   ├── site_settings.py     # Site settings model
│   ├── page.py              # Dynamic pages model
│   ├── revision_request.py  # Revision request model
│   └── deadline_extension.py # Deadline extension model
├── routes/                  # Flask routes/blueprints
│   ├── __init__.py
│   ├── auth.py              # Authentication (login, register)
│   ├── client.py            # Client space
│   ├── admin.py             # Admin panel
│   ├── admin_settings.py    # Admin settings (stats, pages, settings)
│   └── main.py              # Public pages
├── templates/               # Jinja2 templates
│   ├── admin/               # Admin templates
│   ├── auth/                # Authentication templates
│   ├── client/              # Client templates
│   ├── errors/              # Error pages (404, 500, etc.)
│   └── layouts/             # Base templates
├── static/                  # Static files
│   ├── css/styles.css       # Custom styles
│   ├── js/main.js           # Custom JavaScript
│   └── uploads/             # Uploaded documents
├── services/                # Business services
│   ├── admin_service.py     # Admin service
│   └── file_service.py      # File service
├── security/                # Security modules
│   ├── decorators.py        # Authorization decorators
│   ├── validators.py        # Input validation
│   ├── rate_limiter.py      # Rate limiting
│   └── error_handlers.py    # Error handlers
├── utils/                   # Utilities
│   └── forms.py             # WTForms forms
├── docs/                    # Documentation
├── logs/                    # Log files (generated)
├── pyproject.toml           # Python dependencies (uv)
├── requirements.txt         # Python dependencies (pip)
└── README.md                # French documentation
```

---

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL
- uv (Python package manager) or pip

### Installation steps

1. Clone the repository
```bash
git clone https://github.com/your-repo/thedraftclinic.git
cd thedraftclinic
```

2. Install dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Configure environment variables
```bash
# Required variables
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=your-very-long-and-random-secret-key

# Admin variables (optional but recommended)
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=AdminPassword123!
```

4. Initialize the database
```bash
# Check environment variables
python init_db.py --check

# Initialize database and create admin
python init_db.py
```

5. Run the application
```bash
# Development
uv run python main.py

# Production
uv run gunicorn --bind 0.0.0.0:5000 main:app
```

---

## Environment variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | Yes | - |
| `SESSION_SECRET` | Flask session secret key | Yes | - |
| `ADMIN_EMAIL` | Admin account email | No | admin@thedraftclinic.com |
| `ADMIN_PASSWORD` | Admin password (auto-creation) | No | - |

---

## Service types

| Code | Service |
|------|---------|
| `thesis` | PhD thesis |
| `dissertation` | Master's dissertation |
| `research_proposal` | Research proposal |
| `research_paper` | Research paper |
| `book_chapter` | Book chapter |
| `literature_review` | Literature review |
| `proofreading` | Proofreading & correction |
| `editing` | Academic editing |
| `formatting` | Formatting |
| `consultation` | Academic consultation |
| `cv_resume` | Academic CV/resume |
| `personal_statement` | Personal statement |
| `grant_proposal` | Grant proposal |
| `poster_review` | Poster review |

---

## User roles

### Client (researcher/doctoral candidate)
- Create an account and log in
- Submit service requests
- Upload reference documents
- Receive and accept quotes
- Upload payment proofs
- Track project progress
- Download deliverables
- Request revisions with attached files
- Approve or reject deadline extensions

### Administrator
- View all requests
- Send personalized quotes
- Verify payments
- Update request status
- Upload deliverables with comments
- Manage users
- Request deadline extensions
- Handle revision requests
- Configure site settings
- Manage dynamic pages
- View statistics and activity logs

### Super administrator
- All administrator rights
- Manage other admins (add, modify roles, deactivate)
- First account created automatically with this role

---

## Request workflow

```
1. Submitted         <- Client submits a request
       |
       v
2. Under review      <- Admin reviews the request
       |
       v
3. Quote sent        <- Admin sends a quote
       |
       v
4. Quote accepted    <- Client accepts the quote
       |
       v
5. Awaiting deposit  <- Client uploads payment proof
       |
       v
6. In progress       <- Admin verifies and starts work
       |
       v
7. Completed         <- Work completed
       |
       v
8. Delivered         <- Client receives deliverable
       |
       └──> Revision requested (optional)
            Admin delivers revised version
```

---

## Activity tracking

All actions are logged in the system:

| Action type | Description |
|-------------|-------------|
| `comment` | Comment added |
| `delivery` | Deliverable uploaded |
| `revision_request` | Revision requested |
| `revision_delivery` | Revised version delivered |
| `download` | Document downloaded |
| `status_change` | Status changed |
| `deadline_extension_request` | Deadline extension requested |
| `deadline_extension_approved` | Extension approved |
| `deadline_extension_rejected` | Extension rejected |
| `quote_sent` | Quote sent |
| `quote_accepted` | Quote accepted |
| `payment_submitted` | Payment submitted |
| `payment_verified` | Payment verified |
| `document_upload` | Document uploaded |
| `progress_update` | Progress updated |

---

## Security

- Hashed passwords with Werkzeug (bcrypt by default)
- CSRF protection on all forms
- Authentication required for private areas
- Authorization decorators for admin/client access control
- Secure file upload with type validation
- Rate limiting on login forms
- Complete logging of errors and sensitive actions
- Custom error pages (400, 401, 403, 404, 500)

---

## Logging

The application uses a robust logging system:

- Console: all logs in development
- logs/thedraftclinic.log: general log with rotation (10MB)
- logs/errors.log: errors only with rotation

Format: `YYYY-MM-DD HH:MM:SS - LEVEL - module - message`

---

## API endpoints

See [API documentation](docs/API.md) for detailed endpoint information.

### Public pages
- `GET /` - Home page
- `GET /page/<slug>` - Dynamic pages (terms, privacy, etc.)

### Authentication (`/auth`)
- `GET/POST /auth/login` - Login
- `GET/POST /auth/register` - Registration
- `GET /auth/logout` - Logout

### Client space (`/client`)
- `GET /client/dashboard` - Dashboard
- `GET/POST /client/new-request` - New request
- `GET /client/request/<id>` - Request details
- `POST /client/request/<id>/accept-quote` - Accept quote
- `POST /client/request/<id>/submit-payment` - Submit payment
- `POST /client/request/<id>/add-comment` - Add comment
- `POST /client/request/<id>/request-revision` - Request revision
- `GET /client/request/<id>/download/<doc_id>` - Download document
- `GET/POST /client/profile` - User profile

### Admin panel (`/admin`)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/requests` - Request list
- `GET /admin/request/<id>` - Request details
- `POST /admin/request/<id>/send-quote` - Send quote
- `POST /admin/request/<id>/update-status` - Update status
- `POST /admin/request/<id>/upload-deliverable` - Upload deliverable
- `POST /admin/request/<id>/add-comment` - Add comment
- `POST /admin/request/<id>/request-deadline-extension` - Request extension
- `GET /admin/users` - User list
- `GET /admin/user/<id>` - User details
- `POST /admin/payment/<id>/verify` - Verify payment
- `GET /admin/stats` - Statistics page
- `GET /admin/settings` - Site settings
- `GET /admin/pages` - Dynamic pages management
- `GET /admin/admins` - Admin management (super admin only)

---

## Deployment

- [VPS deployment guide](docs/DEPLOYMENT_VPS.md)
- [AWS deployment guide](docs/DEPLOYMENT_AWS.md)

---

## Contact

### MOA Digital Agency LLC

| | |
|---|---|
| Developer | Aisance KALONJI |
| Email | moa@myoneart.com |
| Website | [www.myoneart.com](https://www.myoneart.com) |

---

## License

Copyright 2024 MOA Digital Agency LLC. All rights reserved.

---

<div align="center">

**Developed by MOA Digital Agency LLC**

</div>
