# TheDraftClinic

> **Academic Writing Services Platform**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## About

**TheDraftClinic** is a professional web platform designed for doctoral candidates and researchers who wish to entrust their academic writing projects. Whether it's theses, dissertations, research proposals, scientific articles, or book chapters, our platform offers a complete and secure solution.

### Main Features

| Feature | Description |
|---------|-------------|
| **Request Submission** | Detailed form to submit academic projects |
| **Quote System** | Receive and accept personalized quotes |
| **Payment Management** | Upload payment proofs with admin verification |
| **Dashboard** | Real-time tracking of project progress |
| **User Management** | Registration, login, and profile management |
| **Admin Panel** | Complete interface for request management |
| **Full Traceability** | History of all actions (deliveries, downloads, revisions) |
| **Revision System** | Modification requests with attached files |
| **Deadline Extensions** | Request and validate deadline extensions |
| **Site Settings** | Logo, favicon, SEO, legal information |
| **Dynamic Pages** | Customizable Terms of Service, Privacy Policy |
| **Statistics** | Stats dashboard with performance metrics |

---

## Technologies Used

### Backend
- **Python 3.11** - Main programming language
- **Flask** - Lightweight and powerful web framework
- **SQLAlchemy** - ORM for database management
- **Flask-Login** - Authentication management
- **Flask-WTF** - CSRF protection and form validation
- **Gunicorn** - WSGI server for production

### Frontend
- **TailwindCSS** - Utility-first CSS framework (via CDN)
- **Jinja2** - Template engine
- **JavaScript** - Client-side interactions

### Database
- **PostgreSQL** - Robust relational database

---

## Project Structure

```
TheDraftClinic/
├── app.py                   # Flask configuration and initialization
├── main.py                  # Application entry point
├── init_db.py               # Database initialization script
├── models/                  # SQLAlchemy data models
│   ├── __init__.py
│   ├── user.py              # User model
│   ├── request.py           # Service request model
│   ├── document.py          # Document model
│   ├── payment.py           # Payment model
│   ├── activity_log.py      # Activity log model
│   ├── site_settings.py     # Site settings model
│   ├── page.py              # Dynamic pages model
│   ├── revision_request.py  # Revision request model
│   └── deadline_extension.py # Deadline extension model
├── routes/                  # Flask Routes/Blueprints
│   ├── __init__.py
│   ├── auth.py              # Authentication (login, register)
│   ├── client.py            # Client space
│   ├── admin.py             # Admin panel
│   ├── admin_settings.py    # Admin settings (stats, pages, settings)
│   └── main.py              # Public pages
├── templates/               # Jinja2 Templates
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
│   ├── README_EN.md         # English documentation
│   ├── DEPLOYMENT_VPS.md    # VPS deployment guide
│   ├── DEPLOYMENT_AWS.md    # AWS deployment guide
│   └── API.md               # API documentation
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

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/thedraftclinic.git
cd thedraftclinic
```

2. **Install dependencies**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Required variables
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=your-very-long-and-random-secret-key

# Admin variables (optional but recommended)
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=AdminPassword123!
```

4. **Initialize the database**
```bash
# Check environment variables
python init_db.py --check

# Initialize database and create admin
python init_db.py
```

5. **Run the application**
```bash
# Development
uv run python main.py

# Production
uv run gunicorn --bind 0.0.0.0:5000 main:app
```

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | Yes | - |
| `SESSION_SECRET` | Flask session secret key | Yes | - |
| `ADMIN_EMAIL` | Admin account email | No | admin@thedraftclinic.com |
| `ADMIN_PASSWORD` | Admin password (auto-creation) | No | - |

---

## Service Types

| Code | Service |
|------|---------|
| `thesis` | PhD Thesis |
| `dissertation` | Master's Dissertation |
| `research_proposal` | Research Proposal |
| `research_paper` | Research Paper |
| `book_chapter` | Book Chapter |
| `literature_review` | Literature Review |
| `proofreading` | Proofreading & Correction |
| `editing` | Academic Editing |
| `formatting` | Formatting |
| `consultation` | Academic Consultation |
| `cv_resume` | Academic CV/Resume |
| `personal_statement` | Personal Statement |
| `grant_proposal` | Grant Proposal |
| `poster_review` | Poster Review |

---

## User Roles

### Client (Researcher/Doctoral Candidate)
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

---

## Request Workflow

```
1. Submitted         <- Client submits a request
       |
       v
2. Under Review      <- Admin reviews the request
       |
       v
3. Quote Sent        <- Admin sends a quote
       |
       v
4. Quote Accepted    <- Client accepts the quote
       |
       v
5. Awaiting Deposit  <- Client uploads payment proof
       |
       v
6. In Progress       <- Admin verifies and starts work
       |
       v
7. Completed         <- Work completed
       |
       v
8. Delivered         <- Client receives deliverable
       |
       └──> Revision Requested (optional)
            Admin delivers revised version
```

---

## Activity Tracking

All actions are logged in the system:

| Action Type | Description |
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

- **Hashed passwords** with Werkzeug (bcrypt by default)
- **CSRF protection** on all forms
- **Authentication required** for private areas
- **Authorization decorators** for admin/client access control
- **Secure file upload** with type validation
- **Rate limiting** on login forms
- **Complete logging** of errors and sensitive actions
- **Custom error pages** (400, 401, 403, 404, 500)

---

## Logging

The application uses a robust logging system:

- **Console**: All logs in development
- **logs/thedraftclinic.log**: General log with rotation (10MB)
- **logs/errors.log**: Errors only with rotation

Format: `YYYY-MM-DD HH:MM:SS - LEVEL - module - message`

---

## API Endpoints

See [API Documentation](API.md) for detailed endpoint information.

### Public Pages
- `GET /` - Home page
- `GET /page/<slug>` - Dynamic pages (Terms, Privacy, etc.)

### Authentication (`/auth`)
- `GET/POST /auth/login` - Login
- `GET/POST /auth/register` - Registration
- `GET /auth/logout` - Logout

### Client Space (`/client`)
- `GET /client/dashboard` - Dashboard
- `GET/POST /client/new-request` - New request
- `GET /client/request/<id>` - Request details
- `POST /client/request/<id>/accept-quote` - Accept quote
- `POST /client/request/<id>/submit-payment` - Submit payment
- `POST /client/request/<id>/add-comment` - Add comment
- `POST /client/request/<id>/request-revision` - Request revision
- `GET /client/request/<id>/download/<doc_id>` - Download document
- `GET/POST /client/profile` - User profile

### Admin Panel (`/admin`)
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

---

## Deployment

- [VPS Deployment Guide](DEPLOYMENT_VPS.md)
- [AWS Deployment Guide](DEPLOYMENT_AWS.md)

---

## Contact

### MOA Digital Agency LLC

| | |
|---|---|
| **Developer** | Aisance KALONJI |
| **Email** | moa@myoneart.com |
| **Website** | [www.myoneart.com](https://www.myoneart.com) |

---

## License

Copyright 2024 MOA Digital Agency LLC. All rights reserved.

---

<div align="center">

**Developed by MOA Digital Agency LLC**

</div>
