# TheDraftClinic - plateforme de services de redaction academique

**by MOA Digital Agency LLC | developed by: Aisance KALONJI | contact: moa@myoneart.com**

## vue d'ensemble
TheDraftClinic est une plateforme web permettant aux doctorants et chercheurs de soumettre des demandes de services de redaction academique. La plateforme offre un systeme complet de gestion des demandes avec suivi de progression, gestion des devis et paiements.

## architecture

### backend (python flask)
```
/
├── app.py               # configuration flask, initialisation db, logging
├── main.py              # point d'entree de l'application
├── models/              # modeles sqlalchemy
│   ├── __init__.py
│   ├── user.py          # utilisateurs (clients et admins)
│   ├── request.py       # demandes de services
│   ├── payment.py       # paiements et justificatifs
│   ├── document.py      # documents uploades
│   ├── activity_log.py  # historique des actions (tracabilite)
│   ├── site_settings.py # parametres du site (logo, seo, etc.)
│   ├── page.py          # pages dynamiques (cgu, cgv, etc.)
│   ├── deadline_extension.py # extensions de delai
│   └── revision_request.py   # demandes de revision
├── routes/              # routes/endpoints flask
│   ├── __init__.py
│   ├── main.py          # pages publiques (landing, services, pages dynamiques)
│   ├── auth.py          # authentification (login, register, logout)
│   ├── client.py        # dashboard client, revisions, commentaires
│   ├── admin.py         # dashboard admin, livraisons, revisions
│   └── admin_settings.py # parametres, pages, statistiques
├── services/            # services metier
│   ├── __init__.py
│   ├── admin_service.py # creation admin par defaut
│   └── file_service.py  # gestion fichiers uploades
├── security/            # modules de securite
│   ├── __init__.py
│   ├── decorators.py    # decorateurs d'autorisation
│   ├── validators.py    # validation des entrees
│   ├── rate_limiter.py  # limitation de taux
│   └── error_handlers.py # gestionnaires d'erreurs
├── utils/               # utilitaires
│   └── forms.py         # formulaires wtforms
├── templates/           # templates jinja2
│   ├── layouts/         # template de base
│   ├── auth/            # pages authentification
│   ├── client/          # dashboard client
│   ├── admin/           # dashboard admin
│   └── errors/          # pages d'erreur (404, 500, etc.)
├── static/              # fichiers statiques
│   ├── css/styles.css   # styles personnalises
│   ├── js/main.js       # javascript personnalise
│   └── uploads/         # documents uploades
└── logs/                # fichiers de log (generes)
```

### frontend
- Tailwind CSS (via cdn) pour le style
- design glassmorphisme moderne et professionnel
- responsive pour mobile et desktop

## services proposes
- these de doctorat
- memoire de master
- proposition de recherche
- proposition academique
- chapitre de livre
- article de recherche
- revue de litterature
- relecture et correction
- edition academique
- mise en forme
- consultation academique
- cv/resume academique
- lettre de motivation
- proposition de subvention
- revision de poster

## flux de travail

### client
1. inscription - creation de compte avec infos academiques
2. soumission - formulaire detaille avec upload de documents
3. devis - reception et acceptation du devis
4. paiement - soumission de preuve d'acompte
5. suivi - visualisation de la progression en temps reel
6. livraison - telechargement des livrables (tracabilite)
7. revisions - demande de modifications avec fichiers joints
8. extensions - reponse aux demandes d'extension de delai
9. commentaires - communication avec l'equipe

### admin
1. examen - revision des demandes soumises
2. devis - envoi de devis personnalises
3. verification - validation des preuves de paiement
4. traitement - mise a jour de la progression
5. livraison - upload des livrables avec commentaires
6. revisions - gestion des demandes de revision
7. extensions - demandes d'extension de delai
8. statistiques - dashboard de tracabilite et stats
9. parametres - logo, favicon, seo, informations legales
10. pages - gestion des pages dynamiques (cgu, cgv, etc.)

### super admin
- tous les droits admin
- gestion des autres administrateurs (ajouter, modifier roles, desactiver)
- premier compte cree automatiquement avec ce role

## base de donnees
- PostgreSQL via Replit
- tables: users, service_requests, payments, documents, activity_logs, site_settings, pages, deadline_extensions, revision_requests, revision_attachments

## securite
- mots de passe hashes avec werkzeug (bcrypt)
- protection csrf sur tous les formulaires
- decorateurs d'autorisation (admin_required, client_required, super_admin_required)
- validation des entrees utilisateur
- limitation de taux sur les connexions
- logging complet des erreurs et actions
- pages d'erreur personnalisees (400, 401, 403, 404, 500)

## logging
l'application utilise un systeme de logging robuste:
- `logs/thedraftclinic.log` - log general avec rotation
- `logs/errors.log` - erreurs uniquement

## variables d'environnement

### requises
- `DATABASE_URL` - url de connexion postgresql
- `SESSION_SECRET` - cle secrete flask pour les sessions

### admin (dans variables d'environnement)
- `ADMIN_EMAIL` - email de l'admin (defaut: admin@thedraftclinic.com)
- `ADMIN_PASSWORD` - mot de passe de l'admin (requis pour creer le compte)

## developpement

### lancer le serveur
```bash
uv run gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### structure des commentaires
tous les fichiers sont commentes avec:
- en-tete d'identification (auteur, contact)
- description du module/fichier
- commentaires de section
- docstrings pour les fonctions/classes

## preferences utilisateur
- interface en francais
- design moderne avec glassmorphisme
- backend python flask bien structure
- frontend tailwind css (pas de node.js)
- code entierement commente
- systeme de logging robuste
