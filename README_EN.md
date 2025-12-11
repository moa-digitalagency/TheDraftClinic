# 📚 TheDraftClinic

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/thedraftclinic)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

## 📖 Description

**TheDraftClinic** is a professional academic writing services platform. It supports doctoral students and researchers in writing theses, dissertations, articles, and all types of academic documents.

**🏢 Developed by MOA Digital Agency LLC**
- 👨‍💻 Developer: Aisance KALONJI
- 📧 Contact: moa@myoneart.com
- 🌐 Website: www.myoneart.com

---

## ✨ Features

### 👤 Client Area
- 🔐 Secure registration and login
- 📝 Service request submission
- 📁 Reference document uploads
- 📊 Real-time progress tracking
- ✅ Quote acceptance
- 💳 Payment proof submission
- 📥 Deliverable downloads
- 🔄 Revision requests with file attachments
- 📜 Complete activity history

### ⚙️ Admin Area
- 📊 Dashboard with statistics
- 📋 Request and quote management
- 💰 Payment verification
- 📤 Deliverable uploads with comments
- 🔄 Revision system
- ⏰ Deadline extension requests
- 👥 User management
- 🎨 Site settings (logo, favicon, SEO)
- 📄 Dynamic page management (Terms, Privacy, etc.)
- 📈 Statistics and traceability page

### 📜 Traceability System
- ✅ Complete history of all actions
- 📥 Download tracking
- ⏰ Delivery deadline tracking
- 📊 Performance statistics

---

## 🛠️ Technical Stack

| Category | Technology |
|----------|------------|
| 🔙 **Backend** | Python 3.11, Flask 3.x |
| 🗄️ **Database** | PostgreSQL (via SQLAlchemy) |
| 🔐 **Authentication** | Flask-Login |
| 🎨 **Frontend** | HTML5, Tailwind CSS, JavaScript |
| 🎯 **Icons** | Feather Icons |
| 🚀 **Server** | Gunicorn |

---

## 🚀 Installation

### Prerequisites
- 🐍 Python 3.11+
- 🐘 PostgreSQL
- 📦 pip or uv (Python package manager)

### 📥 Local Installation

```bash
# Clone the repository
git clone https://github.com/your-org/thedraftclinic.git
cd thedraftclinic

# Install dependencies
pip install -r requirements.txt
# or with uv
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env with your values

# Initialize the database
python init_db.py

# Start the development server
python -m flask run --host=0.0.0.0 --port=5000
```

### 🔑 Required Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/thedraftclinic
SESSION_SECRET=your-very-long-secret-key
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=secure-password
```

---

## 📚 Documentation

Complete documentation is available in the `/docs` folder:
- 🚀 [VPS Deployment Guide](docs/DEPLOYMENT_VPS.md)
- ☁️ [AWS Deployment Guide](docs/DEPLOYMENT_AWS.md)
- 📡 [API Documentation](docs/API.md)
- 🎨 [Admin Panel Guide](docs/ADMIN_GUIDE.md)
- 🇫🇷 [README Francais](README.md)

---

## 📁 Project Structure

```
thedraftclinic/
├── 📄 app.py              # Main Flask configuration
├── 📄 main.py             # Application entry point
├── 📄 init_db.py          # Database initialization script
├── 📁 models/             # SQLAlchemy models
│   ├── user.py
│   ├── request.py
│   ├── document.py
│   ├── payment.py
│   ├── activity_log.py
│   ├── site_settings.py
│   ├── page.py
│   └── ...
├── 📁 routes/             # Flask Blueprints
│   ├── main.py            # Public routes
│   ├── auth.py            # Authentication
│   ├── client.py          # Client area
│   ├── admin.py           # Administration
│   └── admin_settings.py
├── 📁 templates/          # Jinja2 templates
│   ├── layouts/
│   ├── admin/
│   ├── client/
│   └── ...
├── 📁 static/             # Static files
│   ├── css/
│   ├── js/
│   └── uploads/
├── 📁 services/           # Business services
├── 📁 security/           # Security and decorators
├── 📁 utils/              # Utilities and forms
└── 📁 docs/               # Documentation
```

---

## 🔐 Security

- 🔒 Password hashing with Werkzeug (pbkdf2:sha256)
- 🛡️ CSRF protection on all forms
- 🔑 Secure sessions with Flask-Login
- ✅ Input validation
- ⏱️ Rate limiting (configurable)

---

## 👥 User Roles

### 🎓 Client (Researcher/PhD Student)
- ✅ Create account and login
- ✅ Submit service requests
- ✅ Upload reference documents
- ✅ Receive and accept quotes
- ✅ Upload payment proofs
- ✅ Track project progress
- ✅ Download deliverables

### 👨‍💼 Administrator
- ✅ View all requests
- ✅ Send custom quotes
- ✅ Verify payments
- ✅ Update request status
- ✅ Upload deliverables
- ✅ Manage users
- ✅ Configure site settings

---

## 🔄 Request Workflow

```
1️⃣ Submitted        ← Client submits request
       ↓
2️⃣ Under Review     ← Admin reviews request
       ↓
3️⃣ Quote Sent       ← Admin sends quote
       ↓
4️⃣ Quote Accepted   ← Client accepts quote
       ↓
5️⃣ Awaiting Deposit ← Client uploads payment proof
       ↓
6️⃣ In Progress      ← Admin verifies and starts work
       ↓
7️⃣ Completed        ← Work completed
       ↓
8️⃣ Delivered        ← Client receives deliverable
```

---

## 📜 License

Proprietary - MOA Digital Agency LLC © 2024

---

<div align="center">

**🚀 Developed by MOA Digital Agency LLC**

*Bring your academic research to life*

</div>
