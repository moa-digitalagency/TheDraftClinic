# 📚 TheDraftClinic

> **Plateforme de Services de Rédaction Académique**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## 🏢 À Propos

**TheDraftClinic** est une plateforme web professionnelle destinée aux doctorants et chercheurs souhaitant confier leurs projets de rédaction académique. Que ce soit pour des thèses, mémoires, propositions de recherche, articles scientifiques ou chapitres d'ouvrage, notre plateforme offre une solution complète et sécurisée.

### 🎯 Fonctionnalités Principales

| Fonctionnalité | Description |
|----------------|-------------|
| 📝 **Soumission de Demandes** | Formulaire détaillé pour soumettre des projets académiques |
| 💰 **Système de Devis** | Réception et acceptation de devis personnalisés |
| 💳 **Gestion des Paiements** | Upload de preuves de paiement avec vérification admin |
| 📊 **Tableau de Bord** | Suivi en temps réel de l'avancement des projets |
| 👥 **Gestion Utilisateurs** | Inscription, connexion et gestion de profil |
| 🔐 **Panel Administrateur** | Interface complète pour la gestion des demandes |

---

## 🛠️ Technologies Utilisées

### Backend
- 🐍 **Python 3.11** - Langage de programmation principal
- 🌶️ **Flask** - Framework web léger et puissant
- 🗄️ **SQLAlchemy** - ORM pour la gestion de base de données
- 🔐 **Flask-Login** - Gestion de l'authentification
- 🛡️ **Flask-WTF** - Protection CSRF et validation de formulaires

### Frontend
- 🎨 **TailwindCSS** - Framework CSS utilitaire
- 🖼️ **Jinja2** - Moteur de templates
- ⚡ **JavaScript** - Interactions côté client

### Base de Données
- 🐘 **PostgreSQL** - Base de données relationnelle robuste

---

## 📁 Structure du Projet

```
TheDraftClinic/
├── 📂 app/
│   ├── 📂 models/           # Modèles de données
│   │   ├── user.py          # Modèle utilisateur
│   │   ├── request.py       # Modèle demande de service
│   │   ├── document.py      # Modèle document
│   │   └── payment.py       # Modèle paiement
│   ├── 📂 routes/           # Routes de l'application
│   │   ├── auth.py          # Authentification
│   │   ├── client.py        # Espace client
│   │   ├── admin.py         # Panel administrateur
│   │   └── main.py          # Pages publiques
│   ├── 📂 templates/        # Templates HTML
│   │   ├── 📂 admin/        # Templates admin
│   │   ├── 📂 auth/         # Templates authentification
│   │   ├── 📂 client/       # Templates client
│   │   └── 📂 layouts/      # Templates de base
│   ├── 📂 services/         # Services métier
│   ├── 📂 static/           # Fichiers statiques
│   └── __init__.py          # Configuration Flask
├── main.py                  # Point d'entrée
├── init_db.py              # Initialisation BDD
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

---

## 🚀 Installation

### Prérequis
- Python 3.11+
- PostgreSQL
- pip

### Étapes d'Installation

1️⃣ **Cloner le repository**
```bash
git clone https://github.com/votre-repo/thedraftclinic.git
cd thedraftclinic
```

2️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3️⃣ **Configurer les variables d'environnement**
```bash
# Créer un fichier .env
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=votre-clé-secrète
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=votre-mot-de-passe-admin
```

4️⃣ **Initialiser la base de données**
```bash
python init_db.py
```

5️⃣ **Lancer l'application**
```bash
python main.py
# ou en production:
gunicorn --bind 0.0.0.0:5000 main:app
```

---

## 📋 Types de Services

| Code | Service |
|------|---------|
| 🎓 `thesis` | Thèse de doctorat |
| 📖 `dissertation` | Mémoire de master |
| 📑 `research_proposal` | Proposition de recherche |
| 📰 `research_paper` | Article de recherche |
| 📚 `book_chapter` | Chapitre de livre |
| 📝 `literature_review` | Revue de littérature |
| ✏️ `proofreading` | Relecture et correction |
| 📋 `editing` | Édition académique |
| 🎨 `formatting` | Mise en forme |
| 💼 `consultation` | Consultation académique |

---

## 👤 Rôles Utilisateurs

### 🧑‍🎓 Client (Chercheur/Doctorant)
- Créer un compte et se connecter
- Soumettre des demandes de service
- Télécharger des documents de référence
- Recevoir et accepter des devis
- Uploader des preuves de paiement
- Suivre l'avancement des projets
- Télécharger les livrables

### 👨‍💼 Administrateur
- Voir toutes les demandes
- Envoyer des devis personnalisés
- Vérifier les paiements
- Mettre à jour le statut des demandes
- Uploader les livrables
- Gérer les utilisateurs

---

## 🔄 Workflow de Demande

```
┌─────────────────┐
│   1. Soumise    │ ← Client soumet une demande
└────────┬────────┘
         ▼
┌─────────────────┐
│  2. En examen   │ ← Admin examine la demande
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. Devis envoyé │ ← Admin envoie un devis
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. Devis accepté│ ← Client accepte le devis
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. Attente      │ ← Client upload preuve de paiement
│    acompte      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 6. En cours     │ ← Admin vérifie et lance le travail
└────────┬────────┘
         ▼
┌─────────────────┐
│  7. Terminée    │ ← Travail terminé
└────────┬────────┘
         ▼
┌─────────────────┐
│   8. Livrée     │ ← Client reçoit le livrable
└─────────────────┘
```

---

## 🔒 Sécurité

- 🔐 Mots de passe hashés avec Werkzeug
- 🛡️ Protection CSRF sur tous les formulaires
- 🔑 Authentification requise pour les espaces privés
- 👮 Décorateurs de contrôle d'accès admin
- 📁 Upload de fichiers sécurisé

---

## 📧 Contact

### 🏢 MOA Digital Agency LLC

| | |
|---|---|
| 👨‍💻 **Développeur** | Aisance KALONJI |
| 📧 **Email** | moa@myoneart.com |
| 🌐 **Site Web** | [www.myoneart.com](https://www.myoneart.com) |

---

## 📄 Licence

Copyright © 2024 MOA Digital Agency LLC. Tous droits réservés.

---

<div align="center">

**Développé avec ❤️ par MOA Digital Agency LLC**

</div>
