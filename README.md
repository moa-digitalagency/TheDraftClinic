# TheDraftClinic

> Plateforme de services de rédaction académique

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## À propos

TheDraftClinic est une plateforme web professionnelle destinée aux doctorants et chercheurs souhaitant confier leurs projets de rédaction académique. Que ce soit pour des thèses, mémoires, propositions de recherche, articles scientifiques ou chapitres d'ouvrage, notre plateforme offre une solution complète et sécurisée.

### Fonctionnalités principales

| Fonctionnalité | Description |
|----------------|-------------|
| Soumission de demandes | Formulaire détaillé pour soumettre des projets académiques |
| Système de devis | Réception et acceptation de devis personnalisés |
| Gestion des paiements | Upload de preuves de paiement avec vérification admin |
| Tableau de bord | Suivi en temps réel de l'avancement des projets |
| Gestion utilisateurs | Inscription, connexion et gestion de profil |
| Panel administrateur | Interface complète pour la gestion des demandes |
| Traçabilité complète | Historique de toutes les actions (livraisons, téléchargements, révisions) |
| Système de révisions | Demandes de modifications avec fichiers joints |
| Extensions de délai | Demandes et validation des extensions de deadline |
| Paramètres du site | Logo, favicon, SEO, informations légales |
| Pages dynamiques | CGU, CGV, politique de confidentialité personnalisables |
| Statistiques | Dashboard de stats avec métriques de performance |

---

## Technologies utilisées

### Backend
- Python 3.11 - Langage de programmation principal
- Flask - Framework web léger et puissant
- SQLAlchemy - ORM pour la gestion de base de données
- Flask-Login - Gestion de l'authentification
- Flask-WTF - Protection CSRF et validation de formulaires
- Gunicorn - Serveur WSGI pour la production

### Frontend
- TailwindCSS - Framework CSS utilitaire (via CDN)
- Jinja2 - Moteur de templates
- JavaScript - Interactions côté client

### Base de données
- PostgreSQL - Base de données relationnelle robuste

---

## Structure du projet

```
TheDraftClinic/
├── app.py                   # Configuration Flask et initialisation
├── main.py                  # Point d'entrée de l'application
├── models/                  # Modèles de données SQLAlchemy
│   ├── __init__.py
│   ├── user.py              # Modèle utilisateur
│   ├── request.py           # Modèle demande de service
│   ├── document.py          # Modèle document
│   ├── payment.py           # Modèle paiement
│   └── activity_log.py      # Modèle historique d'activités
├── routes/                  # Routes/blueprints Flask
│   ├── __init__.py
│   ├── auth.py              # Authentification (login, register)
│   ├── client.py            # Espace client
│   ├── admin.py             # Panel administrateur
│   ├── admin_settings.py    # Paramètres admin
│   └── main.py              # Pages publiques
├── templates/               # Templates Jinja2
│   ├── admin/               # Templates admin
│   ├── auth/                # Templates authentification
│   ├── client/              # Templates client
│   ├── errors/              # Pages d'erreur (404, 500, etc.)
│   └── layouts/             # Templates de base
├── static/                  # Fichiers statiques
│   ├── css/styles.css       # Styles personnalisés
│   ├── js/main.js           # JavaScript personnalisé
│   └── uploads/             # Documents uploadés
├── services/                # Services métier
├── security/                # Modules de sécurité
├── utils/                   # Utilitaires
├── docs/                    # Documentation
└── README.md                # Documentation principale
```

---

## Installation

### Prérequis
- Python 3.11+
- PostgreSQL
- uv (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le repository
```bash
git clone https://github.com/votre-repo/thedraftclinic.git
cd thedraftclinic
```

2. Installer les dépendances
```bash
uv sync
```

3. Configurer les variables d'environnement
```bash
# Variables requises
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=votre-cle-secrete-tres-longue-et-aleatoire

# Variables admin (optionnelles mais recommandées)
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=MotDePasseAdmin123!
```

4. Lancer l'application
```bash
# Développement
uv run python main.py

# Production
uv run gunicorn --bind 0.0.0.0:5000 main:app
```

---

## Variables d'environnement

| Variable | Description | Requis | Défaut |
|----------|-------------|--------|--------|
| `DATABASE_URL` | URL de connexion PostgreSQL | Oui | - |
| `SESSION_SECRET` | Clé secrète pour les sessions Flask | Oui | - |
| `ADMIN_EMAIL` | Email du compte administrateur | Non | admin@thedraftclinic.com |
| `ADMIN_PASSWORD` | Mot de passe admin (création auto) | Non | - |

---

## Types de services

| Code | Service |
|------|---------|
| `thesis` | Thèse de doctorat |
| `dissertation` | Mémoire de master |
| `research_proposal` | Proposition de recherche |
| `research_paper` | Article de recherche |
| `book_chapter` | Chapitre de livre |
| `literature_review` | Revue de littérature |
| `proofreading` | Relecture et correction |
| `editing` | Édition académique |
| `formatting` | Mise en forme |
| `consultation` | Consultation académique |
| `cv_resume` | CV/Résumé académique |
| `personal_statement` | Lettre de motivation |
| `grant_proposal` | Proposition de subvention |
| `poster_review` | Révision de poster |

---

## Rôles utilisateurs

### Client (chercheur/doctorant)
- Créer un compte et se connecter
- Soumettre des demandes de service
- Télécharger des documents de référence
- Recevoir et accepter des devis
- Uploader des preuves de paiement
- Suivre l'avancement des projets
- Télécharger les livrables

### Administrateur
- Voir toutes les demandes
- Envoyer des devis personnalisés
- Vérifier les paiements
- Mettre à jour le statut des demandes
- Uploader les livrables
- Gérer les utilisateurs

### Super administrateur
- Tous les droits d'administrateur
- Gérer les autres administrateurs (ajouter, modifier, supprimer)
- Premier compte admin créé automatiquement

---

## Workflow de demande

```
1. Soumise          <- Client soumet une demande
       |
2. En examen        <- Admin examine la demande
       |
3. Devis envoyé     <- Admin envoie un devis
       |
4. Devis accepté    <- Client accepte le devis
       |
5. Attente acompte  <- Client upload preuve de paiement
       |
6. En cours         <- Admin vérifie et lance le travail
       |
7. Terminée         <- Travail terminé
       |
8. Livrée           <- Client reçoit le livrable
```

---

## Sécurité

- Mots de passe hashés avec Werkzeug (bcrypt par défaut)
- Protection CSRF sur tous les formulaires
- Authentification requise pour les espaces privés
- Décorateurs d'autorisation pour contrôle d'accès admin/client
- Upload de fichiers sécurisé avec validation de type
- Limitation de taux sur les formulaires de connexion
- Logging complet des erreurs et actions sensibles
- Pages d'erreur personnalisées (400, 401, 403, 404, 500)

---

## Logging

L'application utilise un système de logging robuste :

- Console : tous les logs en développement
- logs/thedraftclinic.log : log général avec rotation (10MB)
- logs/errors.log : erreurs uniquement avec rotation

Format : `YYYY-MM-DD HH:MM:SS - LEVEL - module - message`

---

## API endpoints

### Pages publiques
- `GET /` - Page d'accueil
- `GET /services` - Liste des services
- `GET /about` - À propos
- `GET /contact` - Contact

### Authentification (`/auth`)
- `GET/POST /auth/login` - Connexion
- `GET/POST /auth/register` - Inscription
- `GET /auth/logout` - Déconnexion

### Espace client (`/client`)
- `GET /client/dashboard` - Tableau de bord
- `GET/POST /client/new-request` - Nouvelle demande
- `GET /client/request/<id>` - Détails d'une demande
- `POST /client/request/<id>/accept-quote` - Accepter devis
- `POST /client/request/<id>/submit-payment` - Soumettre paiement
- `GET/POST /client/profile` - Profil utilisateur

### Panel admin (`/admin`)
- `GET /admin/dashboard` - Tableau de bord admin
- `GET /admin/requests` - Liste des demandes
- `GET /admin/request/<id>` - Détails demande
- `POST /admin/request/<id>/send-quote` - Envoyer devis
- `POST /admin/request/<id>/update-status` - Modifier statut
- `POST /admin/request/<id>/upload-deliverable` - Uploader livrable
- `GET /admin/users` - Liste utilisateurs
- `GET /admin/user/<id>` - Détails utilisateur
- `POST /admin/payment/<id>/verify` - Vérifier paiement
- `GET /admin/admins` - Gestion des administrateurs (super admin uniquement)

---

## Documentation complète

- [README English](README_EN.md)
- [Guide de déploiement VPS](docs/DEPLOYMENT_VPS.md)
- [Guide de déploiement AWS](docs/DEPLOYMENT_AWS.md)
- [Documentation API](docs/API.md)
- [Guide du panel admin](docs/ADMIN_GUIDE.md)

---

## Contact

### MOA Digital Agency LLC

| | |
|---|---|
| Développeur | Aisance KALONJI |
| Email | moa@myoneart.com |
| Site web | [www.myoneart.com](https://www.myoneart.com) |

---

## Licence

Copyright 2024 MOA Digital Agency LLC. Tous droits réservés.

---

<div align="center">

**Développé par MOA Digital Agency LLC**

*Donnez vie à vos projets académiques*

</div>
