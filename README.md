# 📚 TheDraftClinic

> **🎓 Plateforme de Services de Redaction Academique**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## 📖 A Propos

**TheDraftClinic** est une plateforme web professionnelle destinee aux doctorants et chercheurs souhaitant confier leurs projets de redaction academique. Que ce soit pour des theses, memoires, propositions de recherche, articles scientifiques ou chapitres d'ouvrage, notre plateforme offre une solution complete et securisee.

### ✨ Fonctionnalites Principales

| Fonctionnalite | Description |
|----------------|-------------|
| 📝 **Soumission de Demandes** | Formulaire detaille pour soumettre des projets academiques |
| 💰 **Systeme de Devis** | Reception et acceptation de devis personnalises |
| 💳 **Gestion des Paiements** | Upload de preuves de paiement avec verification admin |
| 📊 **Tableau de Bord** | Suivi en temps reel de l'avancement des projets |
| 👤 **Gestion Utilisateurs** | Inscription, connexion et gestion de profil |
| ⚙️ **Panel Administrateur** | Interface complete pour la gestion des demandes |
| 📜 **Tracabilite Complete** | Historique de toutes les actions (livraisons, telechargements, revisions) |
| 🔄 **Systeme de Revisions** | Demandes de modifications avec fichiers joints |
| ⏰ **Extensions de Delai** | Demandes et validation des extensions de deadline |
| 🎨 **Parametres du Site** | Logo, favicon, SEO, informations legales |
| 📄 **Pages Dynamiques** | CGU, CGV, Politique de confidentialite personnalisables |
| 📈 **Statistiques** | Dashboard de stats avec metriques de performance |

---

## 🛠️ Technologies Utilisees

### Backend
- 🐍 **Python 3.11** - Langage de programmation principal
- 🌶️ **Flask** - Framework web leger et puissant
- 🗄️ **SQLAlchemy** - ORM pour la gestion de base de donnees
- 🔐 **Flask-Login** - Gestion de l'authentification
- 🛡️ **Flask-WTF** - Protection CSRF et validation de formulaires
- 🚀 **Gunicorn** - Serveur WSGI pour la production

### Frontend
- 🎨 **TailwindCSS** - Framework CSS utilitaire (via CDN)
- 📝 **Jinja2** - Moteur de templates
- ⚡ **JavaScript** - Interactions cote client

### Base de Donnees
- 🐘 **PostgreSQL** - Base de donnees relationnelle robuste

---

## 📁 Structure du Projet

```
TheDraftClinic/
├── 📄 app.py                   # Configuration Flask et initialisation
├── 📄 main.py                  # Point d'entree de l'application
├── 📁 models/                  # Modeles de donnees SQLAlchemy
│   ├── __init__.py
│   ├── user.py                 # Modele utilisateur
│   ├── request.py              # Modele demande de service
│   ├── document.py             # Modele document
│   ├── payment.py              # Modele paiement
│   └── activity_log.py         # Modele historique d'activites
├── 📁 routes/                  # Routes/Blueprints Flask
│   ├── __init__.py
│   ├── auth.py                 # Authentification (login, register)
│   ├── client.py               # Espace client
│   ├── admin.py                # Panel administrateur
│   ├── admin_settings.py       # Parametres admin
│   └── main.py                 # Pages publiques
├── 📁 templates/               # Templates Jinja2
│   ├── admin/                  # Templates admin
│   ├── auth/                   # Templates authentification
│   ├── client/                 # Templates client
│   ├── errors/                 # Pages d'erreur (404, 500, etc.)
│   └── layouts/                # Templates de base
├── 📁 static/                  # Fichiers statiques
│   ├── css/styles.css          # Styles personnalises
│   ├── js/main.js              # JavaScript personnalise
│   └── uploads/                # Documents uploades
├── 📁 services/                # Services metier
├── 📁 security/                # Modules de securite
├── 📁 utils/                   # Utilitaires
├── 📁 docs/                    # Documentation
└── 📄 README.md                # Documentation principale
```

---

## 🚀 Installation

### Prerequis
- 🐍 Python 3.11+
- 🐘 PostgreSQL
- 📦 uv (gestionnaire de paquets Python)

### Etapes d'Installation

1. **📥 Cloner le repository**
```bash
git clone https://github.com/votre-repo/thedraftclinic.git
cd thedraftclinic
```

2. **📦 Installer les dependances**
```bash
uv sync
```

3. **⚙️ Configurer les variables d'environnement**
```bash
# Variables requises
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=votre-cle-secrete-tres-longue-et-aleatoire

# Variables admin (optionnelles mais recommandees)
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=MotDePasseAdmin123!
```

4. **▶️ Lancer l'application**
```bash
# Developpement
uv run python main.py

# Production
uv run gunicorn --bind 0.0.0.0:5000 main:app
```

---

## 🔑 Variables d'Environnement

| Variable | Description | Requis | Defaut |
|----------|-------------|--------|--------|
| `DATABASE_URL` | URL de connexion PostgreSQL | ✅ Oui | - |
| `SESSION_SECRET` | Cle secrete pour les sessions Flask | ✅ Oui | - |
| `ADMIN_EMAIL` | Email du compte administrateur | ❌ Non | admin@thedraftclinic.com |
| `ADMIN_PASSWORD` | Mot de passe admin (creation auto) | ❌ Non | - |

---

## 📋 Types de Services

| Code | Service |
|------|---------|
| 📖 `thesis` | These de doctorat |
| 📕 `dissertation` | Memoire de master |
| 📑 `research_proposal` | Proposition de recherche |
| 📰 `research_paper` | Article de recherche |
| 📚 `book_chapter` | Chapitre de livre |
| 📊 `literature_review` | Revue de litterature |
| ✏️ `proofreading` | Relecture et correction |
| 📝 `editing` | Edition academique |
| 📐 `formatting` | Mise en forme |
| 💬 `consultation` | Consultation academique |
| 📄 `cv_resume` | CV/Resume academique |
| ✉️ `personal_statement` | Lettre de motivation |
| 💵 `grant_proposal` | Proposition de subvention |
| 🖼️ `poster_review` | Revision de poster |

---

## 👥 Roles Utilisateurs

### 🎓 Client (Chercheur/Doctorant)
- ✅ Creer un compte et se connecter
- ✅ Soumettre des demandes de service
- ✅ Telecharger des documents de reference
- ✅ Recevoir et accepter des devis
- ✅ Uploader des preuves de paiement
- ✅ Suivre l'avancement des projets
- ✅ Telecharger les livrables

### 👨‍💼 Administrateur
- ✅ Voir toutes les demandes
- ✅ Envoyer des devis personnalises
- ✅ Verifier les paiements
- ✅ Mettre a jour le statut des demandes
- ✅ Uploader les livrables
- ✅ Gerer les utilisateurs

---

## 🔄 Workflow de Demande

```
1️⃣ Soumise          ← Client soumet une demande
       ↓
2️⃣ En examen        ← Admin examine la demande
       ↓
3️⃣ Devis envoye     ← Admin envoie un devis
       ↓
4️⃣ Devis accepte    ← Client accepte le devis
       ↓
5️⃣ Attente acompte  ← Client upload preuve de paiement
       ↓
6️⃣ En cours         ← Admin verifie et lance le travail
       ↓
7️⃣ Terminee         ← Travail termine
       ↓
8️⃣ Livree           ← Client recoit le livrable
```

---

## 🔐 Securite

- 🔒 **Mots de passe hashes** avec Werkzeug (bcrypt par defaut)
- 🛡️ **Protection CSRF** sur tous les formulaires
- 🔑 **Authentification requise** pour les espaces prives
- 👮 **Decorateurs d'autorisation** pour controle d'acces admin/client
- 📁 **Upload de fichiers securise** avec validation de type
- ⏱️ **Limitation de taux** sur les formulaires de connexion
- 📋 **Logging complet** des erreurs et actions sensibles
- 🚫 **Pages d'erreur personnalisees** (400, 401, 403, 404, 500)

---

## 📝 Logging

L'application utilise un systeme de logging robuste:

- 🖥️ **Console**: Tous les logs en developpement
- 📄 **logs/thedraftclinic.log**: Log general avec rotation (10MB)
- ⚠️ **logs/errors.log**: Erreurs uniquement avec rotation

Format: `YYYY-MM-DD HH:MM:SS - LEVEL - module - message`

---

## 🌐 API Endpoints

### 🏠 Pages Publiques
- `GET /` - Page d'accueil
- `GET /services` - Liste des services
- `GET /about` - A propos
- `GET /contact` - Contact

### 🔐 Authentification (`/auth`)
- `GET/POST /auth/login` - Connexion
- `GET/POST /auth/register` - Inscription
- `GET /auth/logout` - Deconnexion

### 👤 Espace Client (`/client`)
- `GET /client/dashboard` - Tableau de bord
- `GET/POST /client/new-request` - Nouvelle demande
- `GET /client/request/<id>` - Details d'une demande
- `POST /client/request/<id>/accept-quote` - Accepter devis
- `POST /client/request/<id>/submit-payment` - Soumettre paiement
- `GET/POST /client/profile` - Profil utilisateur

### ⚙️ Panel Admin (`/admin`)
- `GET /admin/dashboard` - Tableau de bord admin
- `GET /admin/requests` - Liste des demandes
- `GET /admin/request/<id>` - Details demande
- `POST /admin/request/<id>/send-quote` - Envoyer devis
- `POST /admin/request/<id>/update-status` - Modifier statut
- `POST /admin/request/<id>/upload-deliverable` - Uploader livrable
- `GET /admin/users` - Liste utilisateurs
- `GET /admin/user/<id>` - Details utilisateur
- `POST /admin/payment/<id>/verify` - Verifier paiement

---

## 📚 Documentation Complete

- 🇬🇧 [README English](README_EN.md)
- 🚀 [Guide de deploiement VPS](docs/DEPLOYMENT_VPS.md)
- ☁️ [Guide de deploiement AWS](docs/DEPLOYMENT_AWS.md)
- 📡 [Documentation API](docs/API.md)
- 🎨 [Guide du Panel Admin](docs/ADMIN_GUIDE.md)

---

## 📞 Contact

### 🏢 MOA Digital Agency LLC

| | |
|---|---|
| 👨‍💻 **Developpeur** | Aisance KALONJI |
| 📧 **Email** | moa@myoneart.com |
| 🌐 **Site Web** | [www.myoneart.com](https://www.myoneart.com) |

---

## 📜 Licence

Copyright 2024 MOA Digital Agency LLC. Tous droits reserves.

---

<div align="center">

**🚀 Developpe par MOA Digital Agency LLC**

*Donnez vie a vos projets academiques*

</div>
