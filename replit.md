# TheDraftClinic - Plateforme de Services de Rédaction Académique

**By MOA Digital Agency LLC | Developed by: Aisance KALONJI | Contact: moa@myoneart.com**

## Vue d'ensemble
TheDraftClinic est une plateforme web permettant aux doctorants et chercheurs de soumettre des demandes de services de rédaction académique. La plateforme offre un système complet de gestion des demandes avec suivi de progression, gestion des devis et paiements.

## Architecture

### Backend (Python Flask)
```
/
├── app.py               # Configuration Flask, initialisation DB
├── main.py              # Point d'entrée de l'application
├── models/              # Modèles SQLAlchemy
│   ├── user.py          # Utilisateurs (clients et admins)
│   ├── request.py       # Demandes de services
│   ├── payment.py       # Paiements et justificatifs
│   └── document.py      # Documents uploadés
├── routes/              # Routes/Endpoints
│   ├── main.py          # Pages publiques (landing, services)
│   ├── auth.py          # Authentification (login, register, logout)
│   ├── client.py        # Dashboard client
│   └── admin.py         # Dashboard admin
├── services/            # Services métier
│   ├── admin_service.py # Création admin par défaut
│   └── file_service.py  # Gestion fichiers uploadés
├── utils/               # Utilitaires
│   └── forms.py         # Formulaires WTForms
├── security/            # Sécurité (à étendre)
├── templates/           # Templates Jinja2
│   ├── layouts/         # Template de base
│   ├── auth/            # Pages authentification
│   ├── client/          # Dashboard client
│   └── admin/           # Dashboard admin
└── static/              # Fichiers statiques
    ├── css/styles.css   # Styles personnalisés
    ├── js/main.js       # JavaScript personnalisé
    └── uploads/         # Documents uploadés
```

### Frontend
- **Tailwind CSS** (via CDN) pour le style
- **Design glassmorphisme** moderne et professionnel
- **Responsive** pour mobile et desktop

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
1. Inscription → Création de compte avec infos académiques
2. Soumission → Formulaire détaillé avec upload de documents
3. Devis → Réception et acceptation du devis
4. Paiement → Soumission de preuve d'acompte
5. Suivi → Visualisation de la progression en temps réel
6. Livraison → Téléchargement des livrables

### Admin
1. Examen → Révision des demandes soumises
2. Devis → Envoi de devis personnalisés
3. Vérification → Validation des preuves de paiement
4. Traitement → Mise à jour de la progression
5. Livraison → Upload des livrables

## Base de données
- **PostgreSQL** via Replit
- Tables: users, service_requests, payments, documents

## Compte administrateur
Le compte admin est créé automatiquement au démarrage si les variables d'environnement sont configurées.

## Développement

### Lancer le serveur
```bash
python main.py
```

### Variables d'environnement
- `DATABASE_URL` - URL de connexion PostgreSQL
- `SECRET_KEY` - Clé secrète Flask
- `ADMIN_EMAIL` - Email de l'admin (défaut: admin@thedraftclinic.com)
- `ADMIN_PASSWORD` - Mot de passe de l'admin (requis pour créer le compte)

## Préférences utilisateur
- Interface en français
- Design moderne avec glassmorphisme
- Backend Python Flask organisé
- Frontend Tailwind CSS (pas de Node.js)
