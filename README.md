# TheDraftClinic

> Plateforme de services de redaction academique

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan?logo=tailwindcss)

---

## a propos

TheDraftClinic est une plateforme web professionnelle destinee aux doctorants et chercheurs souhaitant confier leurs projets de redaction academique. Que ce soit pour des theses, memoires, propositions de recherche, articles scientifiques ou chapitres d'ouvrage, notre plateforme offre une solution complete et securisee.

### fonctionnalites principales

| fonctionnalite | description |
|----------------|-------------|
| soumission de demandes | formulaire detaille pour soumettre des projets academiques |
| systeme de devis | reception et acceptation de devis personnalises |
| gestion des paiements | upload de preuves de paiement avec verification admin |
| tableau de bord | suivi en temps reel de l'avancement des projets |
| gestion utilisateurs | inscription, connexion et gestion de profil |
| panel administrateur | interface complete pour la gestion des demandes |
| tracabilite complete | historique de toutes les actions (livraisons, telechargements, revisions) |
| systeme de revisions | demandes de modifications avec fichiers joints |
| extensions de delai | demandes et validation des extensions de deadline |
| parametres du site | logo, favicon, seo, informations legales |
| pages dynamiques | cgu, cgv, politique de confidentialite personnalisables |
| statistiques | dashboard de stats avec metriques de performance |

---

## technologies utilisees

### backend
- Python 3.11 - langage de programmation principal
- Flask - framework web leger et puissant
- SQLAlchemy - orm pour la gestion de base de donnees
- Flask-Login - gestion de l'authentification
- Flask-WTF - protection csrf et validation de formulaires
- Gunicorn - serveur wsgi pour la production

### frontend
- TailwindCSS - framework css utilitaire (via cdn)
- Jinja2 - moteur de templates
- JavaScript - interactions cote client

### base de donnees
- PostgreSQL - base de donnees relationnelle robuste

---

## structure du projet

```
TheDraftClinic/
├── app.py                   # configuration flask et initialisation
├── main.py                  # point d'entree de l'application
├── models/                  # modeles de donnees sqlalchemy
│   ├── __init__.py
│   ├── user.py              # modele utilisateur
│   ├── request.py           # modele demande de service
│   ├── document.py          # modele document
│   ├── payment.py           # modele paiement
│   └── activity_log.py      # modele historique d'activites
├── routes/                  # routes/blueprints flask
│   ├── __init__.py
│   ├── auth.py              # authentification (login, register)
│   ├── client.py            # espace client
│   ├── admin.py             # panel administrateur
│   ├── admin_settings.py    # parametres admin
│   └── main.py              # pages publiques
├── templates/               # templates jinja2
│   ├── admin/               # templates admin
│   ├── auth/                # templates authentification
│   ├── client/              # templates client
│   ├── errors/              # pages d'erreur (404, 500, etc.)
│   └── layouts/             # templates de base
├── static/                  # fichiers statiques
│   ├── css/styles.css       # styles personnalises
│   ├── js/main.js           # javascript personnalise
│   └── uploads/             # documents uploades
├── services/                # services metier
├── security/                # modules de securite
├── utils/                   # utilitaires
├── docs/                    # documentation
└── README.md                # documentation principale
```

---

## installation

### prerequis
- Python 3.11+
- PostgreSQL
- uv (gestionnaire de paquets python)

### etapes d'installation

1. cloner le repository
```bash
git clone https://github.com/votre-repo/thedraftclinic.git
cd thedraftclinic
```

2. installer les dependances
```bash
uv sync
```

3. configurer les variables d'environnement
```bash
# variables requises
DATABASE_URL=postgresql://user:password@localhost/thedraftclinic
SESSION_SECRET=votre-cle-secrete-tres-longue-et-aleatoire

# variables admin (optionnelles mais recommandees)
ADMIN_EMAIL=admin@thedraftclinic.com
ADMIN_PASSWORD=MotDePasseAdmin123!
```

4. lancer l'application
```bash
# developpement
uv run python main.py

# production
uv run gunicorn --bind 0.0.0.0:5000 main:app
```

---

## variables d'environnement

| variable | description | requis | defaut |
|----------|-------------|--------|--------|
| `DATABASE_URL` | url de connexion postgresql | oui | - |
| `SESSION_SECRET` | cle secrete pour les sessions flask | oui | - |
| `ADMIN_EMAIL` | email du compte administrateur | non | admin@thedraftclinic.com |
| `ADMIN_PASSWORD` | mot de passe admin (creation auto) | non | - |

---

## types de services

| code | service |
|------|---------|
| `thesis` | these de doctorat |
| `dissertation` | memoire de master |
| `research_proposal` | proposition de recherche |
| `research_paper` | article de recherche |
| `book_chapter` | chapitre de livre |
| `literature_review` | revue de litterature |
| `proofreading` | relecture et correction |
| `editing` | edition academique |
| `formatting` | mise en forme |
| `consultation` | consultation academique |
| `cv_resume` | cv/resume academique |
| `personal_statement` | lettre de motivation |
| `grant_proposal` | proposition de subvention |
| `poster_review` | revision de poster |

---

## roles utilisateurs

### client (chercheur/doctorant)
- creer un compte et se connecter
- soumettre des demandes de service
- telecharger des documents de reference
- recevoir et accepter des devis
- uploader des preuves de paiement
- suivre l'avancement des projets
- telecharger les livrables

### administrateur
- voir toutes les demandes
- envoyer des devis personnalises
- verifier les paiements
- mettre a jour le statut des demandes
- uploader les livrables
- gerer les utilisateurs

### super administrateur
- tous les droits d'administrateur
- gerer les autres administrateurs (ajouter, modifier, supprimer)
- premier compte admin cree automatiquement

---

## workflow de demande

```
1. soumise          <- client soumet une demande
       |
2. en examen        <- admin examine la demande
       |
3. devis envoye     <- admin envoie un devis
       |
4. devis accepte    <- client accepte le devis
       |
5. attente acompte  <- client upload preuve de paiement
       |
6. en cours         <- admin verifie et lance le travail
       |
7. terminee         <- travail termine
       |
8. livree           <- client recoit le livrable
```

---

## securite

- mots de passe hashes avec werkzeug (bcrypt par defaut)
- protection csrf sur tous les formulaires
- authentification requise pour les espaces prives
- decorateurs d'autorisation pour controle d'acces admin/client
- upload de fichiers securise avec validation de type
- limitation de taux sur les formulaires de connexion
- logging complet des erreurs et actions sensibles
- pages d'erreur personnalisees (400, 401, 403, 404, 500)

---

## logging

L'application utilise un systeme de logging robuste:

- console: tous les logs en developpement
- logs/thedraftclinic.log: log general avec rotation (10mb)
- logs/errors.log: erreurs uniquement avec rotation

format: `YYYY-MM-DD HH:MM:SS - LEVEL - module - message`

---

## api endpoints

### pages publiques
- `GET /` - page d'accueil
- `GET /services` - liste des services
- `GET /about` - a propos
- `GET /contact` - contact

### authentification (`/auth`)
- `GET/POST /auth/login` - connexion
- `GET/POST /auth/register` - inscription
- `GET /auth/logout` - deconnexion

### espace client (`/client`)
- `GET /client/dashboard` - tableau de bord
- `GET/POST /client/new-request` - nouvelle demande
- `GET /client/request/<id>` - details d'une demande
- `POST /client/request/<id>/accept-quote` - accepter devis
- `POST /client/request/<id>/submit-payment` - soumettre paiement
- `GET/POST /client/profile` - profil utilisateur

### panel admin (`/admin`)
- `GET /admin/dashboard` - tableau de bord admin
- `GET /admin/requests` - liste des demandes
- `GET /admin/request/<id>` - details demande
- `POST /admin/request/<id>/send-quote` - envoyer devis
- `POST /admin/request/<id>/update-status` - modifier statut
- `POST /admin/request/<id>/upload-deliverable` - uploader livrable
- `GET /admin/users` - liste utilisateurs
- `GET /admin/user/<id>` - details utilisateur
- `POST /admin/payment/<id>/verify` - verifier paiement
- `GET /admin/admins` - gestion des administrateurs (super admin uniquement)

---

## documentation complete

- [readme english](README_EN.md)
- [guide de deploiement vps](docs/DEPLOYMENT_VPS.md)
- [guide de deploiement aws](docs/DEPLOYMENT_AWS.md)
- [documentation api](docs/API.md)
- [guide du panel admin](docs/ADMIN_GUIDE.md)

---

## contact

### MOA Digital Agency LLC

| | |
|---|---|
| developpeur | Aisance KALONJI |
| email | moa@myoneart.com |
| site web | [www.myoneart.com](https://www.myoneart.com) |

---

## licence

Copyright 2024 MOA Digital Agency LLC. Tous droits reserves.

---

<div align="center">

**developpe par MOA Digital Agency LLC**

*donnez vie a vos projets academiques*

</div>
