# TheDraftClinic

> academic writing services platform

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## about

TheDraftClinic is a professional web platform designed for doctoral candidates and researchers who wish to entrust their academic writing projects. Whether it's theses, dissertations, research proposals, scientific articles, or book chapters, our platform offers a complete and secure solution.

### main features

| feature | description |
|---------|-------------|
| request submission | detailed form to submit academic projects |
| quote system | receive and accept personalized quotes |
| payment management | upload payment proofs with admin verification |
| dashboard | real-time tracking of project progress |
| user management | registration, login, and profile management |
| admin panel | complete interface for request management |
| full traceability | history of all actions (deliveries, downloads, revisions) |
| revision system | modification requests with attached files |
| deadline extensions | request and validate deadline extensions |
| site settings | logo, favicon, seo, legal information |
| dynamic pages | customizable terms of service, privacy policy |
| statistics | stats dashboard with performance metrics |

---

## technologies used

### backend
- Python 3.11 - main programming language
- Flask - lightweight and powerful web framework
- SQLAlchemy - orm for database management
- Flask-Login - authentication management
- Flask-WTF - csrf protection and form validation
- Gunicorn - wsgi server for production

### frontend
- TailwindCSS - utility-first css framework (via cdn)
- Jinja2 - template engine
- JavaScript - client-side interactions

### database
- PostgreSQL - robust relational database

---

## project structure

```
TheDraftClinic/
├── app.py                   # flask configuration and initialization
├── main.py                  # application entry point
├── init_db.py               # database initialization script
├── models/                  # sqlalchemy data models
│   ├── __init__.py
│   ├── user.py              # user model with admin roles
│   ├── request.py           # service request model
│   ├── document.py          # document model
│   ├── payment.py           # payment model
│   ├── activity_log.py      # activity log model
│   ├── site_settings.py     # site settings model
│   ├── page.py              # dynamic pages model
│   ├── revision_request.py  # revision request model
│   └── deadline_extension.py # deadline extension model
├── routes/                  # flask routes/blueprints
│   ├── __init__.py
│   ├── auth.py              # authentication (login, register)
│   ├── client.py            # client space
│   ├── admin.py             # admin panel
│   ├── admin_settings.py    # admin settings (stats, pages, settings)
│   └── main.py              # public pages
├── templates/               # jinja2 templates
│   ├── admin/               # admin templates
│   ├── auth/                # authentication templates
│   ├── client/              # client templates
│   ├── errors/              # error pages (404, 500, etc.)
│   └── layouts/             # base templates
├── static/                  # static files
│   ├── css/styles.css       # custom styles
│   ├── js/main.js           # custom javascript
│   └── uploads/             # uploaded documents
├── services/                # business services
│   ├── admin_service.py     # admin service
│   └── file_service.py      # file service
├── security/                # security modules
│   ├── decorators.py        # authorization decorators
│   ├── validators.py        # input validation
│   ├── rate_limiter.py      # rate limiting
│   └── error_handlers.py    # error handlers
├── utils/                   # utilities
│   └── forms.py             # wtforms forms
├── docs/                    # documentation
├── logs/                    # log files (generated)
├── pyproject.toml           # python dependencies (uv)
├── requirements.txt         # python dependencies (pip)
└── README.md                # french documentation
```

---

## installation

### prerequisites
- Python 3.11+
- PostgreSQL
- uv (python package manager) or pip

### installation steps

1. clone the repository
```bash
git clone https://github.com/your-repo/thedraftclinic.git
cd thedraftclinic
```

2. install dependencies
```bash
# using uv (recommended)
uv sync

# or using pip
pip install -r requirements.txt
```

3. configure environment variables
```bash
# required variables
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=your-very-long-and-random-secret-key

# admin variables (optional but recommended)
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=AdminPassword123!
```

4. initialize the database
```bash
# check environment variables
python init_db.py --check

# initialize database and create admin
python init_db.py
```

5. run the application
```bash
# development
uv run python main.py

# production
uv run gunicorn --bind 0.0.0.0:5000 main:app
```

---

## environment variables

| variable | description | required | default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | postgresql connection url | yes | - |
| `SESSION_SECRET` | flask session secret key | yes | - |
| `ADMIN_EMAIL` | admin account email | no | admin@thedraftclinic.com |
| `ADMIN_PASSWORD` | admin password (auto-creation) | no | - |

---

## service types

| code | service |
|------|---------|
| `thesis` | phd thesis |
| `dissertation` | master's dissertation |
| `research_proposal` | research proposal |
| `research_paper` | research paper |
| `book_chapter` | book chapter |
| `literature_review` | literature review |
| `proofreading` | proofreading & correction |
| `editing` | academic editing |
| `formatting` | formatting |
| `consultation` | academic consultation |
| `cv_resume` | academic cv/resume |
| `personal_statement` | personal statement |
| `grant_proposal` | grant proposal |
| `poster_review` | poster review |

---

## user roles

### client (researcher/doctoral candidate)
- create an account and log in
- submit service requests
- upload reference documents
- receive and accept quotes
- upload payment proofs
- track project progress
- download deliverables
- request revisions with attached files
- approve or reject deadline extensions

### administrator
- view all requests
- send personalized quotes
- verify payments
- update request status
- upload deliverables with comments
- manage users
- request deadline extensions
- handle revision requests
- configure site settings
- manage dynamic pages
- view statistics and activity logs

### super administrator
- all administrator rights
- manage other admins (add, modify roles, deactivate)
- first account created automatically with this role

---

## request workflow

```
1. submitted         <- client submits a request
       |
       v
2. under review      <- admin reviews the request
       |
       v
3. quote sent        <- admin sends a quote
       |
       v
4. quote accepted    <- client accepts the quote
       |
       v
5. awaiting deposit  <- client uploads payment proof
       |
       v
6. in progress       <- admin verifies and starts work
       |
       v
7. completed         <- work completed
       |
       v
8. delivered         <- client receives deliverable
       |
       └──> revision requested (optional)
            admin delivers revised version
```

---

## activity tracking

all actions are logged in the system:

| action type | description |
|-------------|-------------|
| `comment` | comment added |
| `delivery` | deliverable uploaded |
| `revision_request` | revision requested |
| `revision_delivery` | revised version delivered |
| `download` | document downloaded |
| `status_change` | status changed |
| `deadline_extension_request` | deadline extension requested |
| `deadline_extension_approved` | extension approved |
| `deadline_extension_rejected` | extension rejected |
| `quote_sent` | quote sent |
| `quote_accepted` | quote accepted |
| `payment_submitted` | payment submitted |
| `payment_verified` | payment verified |
| `document_upload` | document uploaded |
| `progress_update` | progress updated |

---

## security

- hashed passwords with werkzeug (bcrypt by default)
- csrf protection on all forms
- authentication required for private areas
- authorization decorators for admin/client access control
- secure file upload with type validation
- rate limiting on login forms
- complete logging of errors and sensitive actions
- custom error pages (400, 401, 403, 404, 500)

---

## logging

the application uses a robust logging system:

- console: all logs in development
- logs/thedraftclinic.log: general log with rotation (10mb)
- logs/errors.log: errors only with rotation

format: `YYYY-MM-DD HH:MM:SS - LEVEL - module - message`

---

## api endpoints

see [api documentation](API.md) for detailed endpoint information.

### public pages
- `GET /` - home page
- `GET /page/<slug>` - dynamic pages (terms, privacy, etc.)

### authentication (`/auth`)
- `GET/POST /auth/login` - login
- `GET/POST /auth/register` - registration
- `GET /auth/logout` - logout

### client space (`/client`)
- `GET /client/dashboard` - dashboard
- `GET/POST /client/new-request` - new request
- `GET /client/request/<id>` - request details
- `POST /client/request/<id>/accept-quote` - accept quote
- `POST /client/request/<id>/submit-payment` - submit payment
- `POST /client/request/<id>/add-comment` - add comment
- `POST /client/request/<id>/request-revision` - request revision
- `GET /client/request/<id>/download/<doc_id>` - download document
- `GET/POST /client/profile` - user profile

### admin panel (`/admin`)
- `GET /admin/dashboard` - admin dashboard
- `GET /admin/requests` - request list
- `GET /admin/request/<id>` - request details
- `POST /admin/request/<id>/send-quote` - send quote
- `POST /admin/request/<id>/update-status` - update status
- `POST /admin/request/<id>/upload-deliverable` - upload deliverable
- `POST /admin/request/<id>/add-comment` - add comment
- `POST /admin/request/<id>/request-deadline-extension` - request extension
- `GET /admin/users` - user list
- `GET /admin/user/<id>` - user details
- `POST /admin/payment/<id>/verify` - verify payment
- `GET /admin/stats` - statistics page
- `GET /admin/settings` - site settings
- `GET /admin/pages` - dynamic pages management
- `GET /admin/admins` - admin management (super admin only)

---

## deployment

- [vps deployment guide](DEPLOYMENT_VPS.md)
- [aws deployment guide](DEPLOYMENT_AWS.md)

---

## contact

### MOA Digital Agency LLC

| | |
|---|---|
| developer | Aisance KALONJI |
| email | moa@myoneart.com |
| website | [www.myoneart.com](https://www.myoneart.com) |

---

## license

Copyright 2024 MOA Digital Agency LLC. All rights reserved.

---

<div align="center">

**developed by MOA Digital Agency LLC**

</div>
