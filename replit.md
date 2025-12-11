# TheDraftClinic - Plateforme de services de rédaction académique

**Par MOA Digital Agency LLC | Développé par : Aisance KALONJI | Contact : moa@myoneart.com**

## Vue d'ensemble

TheDraftClinic est une plateforme web permettant aux doctorants et chercheurs de soumettre des demandes de services de rédaction académique. La plateforme offre un système complet de gestion des demandes avec suivi de progression, gestion des devis et paiements.

## Architecture

### Backend (Python Flask)
```
/
├── app.py               # Configuration Flask, initialisation DB, logging
├── main.py              # Point d'entrée de l'application
├── models/              # Modèles SQLAlchemy
│   ├── __init__.py
│   ├── user.py          # Utilisateurs (clients et admins)
│   ├── request.py       # Demandes de services
│   ├── payment.py       # Paiements et justificatifs
│   ├── document.py      # Documents uploadés
│   ├── activity_log.py  # Historique des actions (traçabilité)
│   ├── site_settings.py # Paramètres du site (logo, SEO, etc.)
│   ├── page.py          # Pages dynamiques (CGU, CGV, etc.)
│   ├── deadline_extension.py # Extensions de délai
│   └── revision_request.py   # Demandes de révision
├── routes/              # Routes/endpoints Flask
│   ├── __init__.py
│   ├── main.py          # Pages publiques (landing, services, pages dynamiques)
│   ├── auth.py          # Authentification (login, register, logout)
│   ├── client.py        # Dashboard client, révisions, commentaires
│   ├── admin.py         # Dashboard admin, livraisons, révisions
│   └── admin_settings.py # Paramètres, pages, statistiques
├── services/            # Services métier
│   ├── __init__.py
│   ├── admin_service.py # Création admin par défaut
│   └── file_service.py  # Gestion fichiers uploadés
├── security/            # Modules de sécurité
│   ├── __init__.py
│   ├── decorators.py    # Décorateurs d'autorisation
│   ├── validators.py    # Validation des entrées
│   ├── rate_limiter.py  # Limitation de taux
│   └── error_handlers.py # Gestionnaires d'erreurs
├── utils/               # Utilitaires
│   ├── forms.py         # Formulaires WTForms
│   └── i18n.py          # Système de traduction (internationalisation)
├── lang/                # Fichiers de traduction
│   ├── fr.json          # Traductions françaises
│   └── en.json          # Traductions anglaises
├── templates/           # Templates Jinja2
│   ├── layouts/         # Template de base
│   ├── auth/            # Pages authentification
│   ├── client/          # Dashboard client
│   ├── admin/           # Dashboard admin
│   └── errors/          # Pages d'erreur (404, 500, etc.)
├── static/              # Fichiers statiques
│   ├── css/styles.css   # Styles personnalisés
│   ├── js/main.js       # JavaScript personnalisé
│   └── uploads/         # Documents uploadés
└── logs/                # Fichiers de log (générés)
```

### Frontend
- Tailwind CSS (via CDN) pour le style
- Design glassmorphisme moderne et professionnel
- Responsive pour mobile et desktop

## Services proposés
- Thèse de doctorat
- Mémoire de master
- Proposition de recherche
- Proposition académique
- Chapitre de livre
- Article de recherche
- Revue de littérature
- Relecture et correction
- Édition académique
- Mise en forme
- Consultation académique
- CV/Résumé académique
- Lettre de motivation
- Proposition de subvention
- Révision de poster

## Flux de travail

### Client
1. Inscription - Création de compte avec infos académiques
2. Soumission - Formulaire détaillé avec upload de documents
3. Devis - Réception et acceptation du devis
4. Paiement - Soumission de preuve d'acompte
5. Suivi - Visualisation de la progression en temps réel
6. Livraison - Téléchargement des livrables (traçabilité)
7. Révisions - Demande de modifications avec fichiers joints
8. Extensions - Réponse aux demandes d'extension de délai
9. Commentaires - Communication avec l'équipe

### Admin
1. Examen - Révision des demandes soumises
2. Devis - Envoi de devis personnalisés
3. Vérification - Validation des preuves de paiement
4. Traitement - Mise à jour de la progression
5. Livraison - Upload des livrables avec commentaires
6. Révisions - Gestion des demandes de révision
7. Extensions - Demandes d'extension de délai
8. Statistiques - Dashboard de traçabilité et stats
9. Paramètres - Logo, favicon, SEO, informations légales
10. Pages - Gestion des pages dynamiques (CGU, CGV, etc.)

### Super admin
- Tous les droits admin
- Gestion des autres administrateurs (ajouter, modifier rôles, désactiver)
- Premier compte créé automatiquement avec ce rôle

## Base de données
- PostgreSQL via Replit
- Tables : users, service_requests, payments, documents, activity_logs, site_settings, pages, deadline_extensions, revision_requests, revision_attachments

## Sécurité
- Mots de passe hashés avec Werkzeug (bcrypt)
- Protection CSRF sur tous les formulaires
- Décorateurs d'autorisation (admin_required, client_required, super_admin_required)
- Validation des entrées utilisateur
- Limitation de taux sur les connexions
- Logging complet des erreurs et actions
- Pages d'erreur personnalisées (400, 401, 403, 404, 500)

## Logging
L'application utilise un système de logging robuste :
- `logs/thedraftclinic.log` - Log général avec rotation
- `logs/errors.log` - Erreurs uniquement

## Variables d'environnement

### Requises
- `DATABASE_URL` - URL de connexion PostgreSQL
- `SESSION_SECRET` - Clé secrète Flask pour les sessions

### Admin (dans variables d'environnement)
- `ADMIN_EMAIL` - Email de l'admin (défaut : admin@thedraftclinic.com)
- `ADMIN_PASSWORD` - Mot de passe de l'admin (requis pour créer le compte)

## Développement

### Lancer le serveur
```bash
uv run gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### Structure des commentaires
Tous les fichiers sont commentés avec :
- En-tête d'identification (auteur, contact)
- Description du module/fichier
- Commentaires de section
- Docstrings pour les fonctions/classes

## Préférences utilisateur
- Interface en français
- Design moderne avec glassmorphisme
- Backend Python Flask bien structuré
- Frontend Tailwind CSS (pas de Node.js)
- Code entièrement commenté
- Système de logging robuste
