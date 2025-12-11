# architecture TheDraftClinic

> documentation technique de l'architecture

---

## vue d'ensemble

TheDraftClinic est une application web Flask suivant une architecture MVC (modele-vue-controleur) avec une separation claire des responsabilites.

---

## couches de l'application

```
┌─────────────────────────────────────────────────┐
│                   Templates                      │
│            (Jinja2 + TailwindCSS)               │
├─────────────────────────────────────────────────┤
│                    Routes                        │
│             (Blueprints Flask)                   │
├─────────────────────────────────────────────────┤
│                   Services                       │
│            (Logique metier)                     │
├─────────────────────────────────────────────────┤
│                   Modeles                        │
│              (SQLAlchemy ORM)                   │
├─────────────────────────────────────────────────┤
│                 Base de donnees                  │
│                 (PostgreSQL)                    │
└─────────────────────────────────────────────────┘
```

---

## structure des dossiers

### `/models` - modeles de donnees

| fichier | description |
|---------|-------------|
| `user.py` | modele utilisateur avec authentification et roles admin |
| `request.py` | modele demande de service |
| `document.py` | modele document/fichier |
| `payment.py` | modele paiement |
| `activity_log.py` | modele historique d'activites |
| `site_settings.py` | modele parametres du site |
| `page.py` | modele pages dynamiques |

### `/routes` - controleurs

| fichier | prefix | description |
|---------|--------|-------------|
| `main.py` | `/` | pages publiques |
| `auth.py` | `/auth` | authentification |
| `client.py` | `/client` | espace client |
| `admin.py` | `/admin` | administration |
| `admin_settings.py` | `/admin/settings` | parametres admin |

### `/templates` - vues

| dossier | description |
|---------|-------------|
| `layouts/` | templates de base |
| `admin/` | templates admin |
| `client/` | templates client |
| `auth/` | templates authentification |
| `errors/` | pages d'erreur |

### `/services` - services metier

| fichier | description |
|---------|-------------|
| `admin_service.py` | logique admin et creation super admin |
| `file_service.py` | gestion des fichiers |

### `/security` - securite

| fichier | description |
|---------|-------------|
| `decorators.py` | decorateurs d'autorisation |
| `validators.py` | validation des entrees |
| `rate_limiter.py` | limitation de taux |
| `error_handlers.py` | gestionnaires d'erreurs |

---

## authentification

### flask-login
l'authentification utilise flask-login avec:
- sessions securisees
- remember me (se souvenir de moi)
- protection des routes

### decorateurs
```python
@login_required          # connexion requise
@admin_required          # admin uniquement
@super_admin_required    # super admin uniquement
@client_required         # client uniquement
```

---

## systeme de roles admin

### roles disponibles
- `super_admin` - premier compte admin, tous les droits
- `admin` - administrateur standard

### permissions
| action | admin | super_admin |
|--------|-------|-------------|
| gerer demandes | oui | oui |
| gerer utilisateurs | oui | oui |
| parametres site | oui | oui |
| ajouter admin | non | oui |
| modifier role admin | non | oui |
| desactiver admin | non | oui |

---

## base de donnees

### schema relationnel

```
┌─────────────┐     ┌──────────────────┐
│    User     │────<│  ServiceRequest  │
└─────────────┘     └──────────────────┘
                           │
                           ├────<┌─────────────┐
                           │     │  Document   │
                           │     └─────────────┘
                           │
                           ├────<┌─────────────┐
                           │     │  Payment    │
                           │     └─────────────┘
                           │
                           └────<┌─────────────┐
                                 │ ActivityLog │
                                 └─────────────┘
```

### modeles principaux

#### user
- id, email, password_hash
- first_name, last_name
- phone, institution
- academic_level, field_of_study
- is_admin, admin_role
- account_active
- created_at, updated_at

#### servicerequest
- id, user_id, title
- service_type, description
- status, progress_percentage
- quote_amount, deposit_required
- deadline, created_at

#### payment
- id, request_id, amount
- payment_method, status
- proof_document, transaction_reference
- created_at

#### activitylog
- id, request_id, user_id
- action_type, title
- description, metadata
- created_at

---

## templates

### layouts
l'application utilise des templates de base:

| layout | description |
|--------|-------------|
| `base.html` | layout de base commun |
| `admin_base.html` | layout admin avec sidebar |

### heritage
```
base.html
├── layouts/auth_base.html
├── layouts/client_base.html
└── layouts/admin_base.html
    └── admin/*.html
```

---

## workflow des demandes

### statuts
1. `submitted` - soumise
2. `under_review` - en examen
3. `quote_sent` - devis envoye
4. `quote_accepted` - devis accepte
5. `awaiting_deposit` - attente acompte
6. `in_progress` - en cours
7. `revision` - en revision
8. `completed` - terminee
9. `delivered` - livree
10. `cancelled` - annulee

### transitions
```
submitted -> under_review -> quote_sent -> quote_accepted
    |                                        |
cancelled                             awaiting_deposit
                                            |
                                       in_progress
                                            |
                                      revision <-> completed
                                                    |
                                                delivered
```

---

## historique d'activites

### types d'actions
| type | description |
|------|-------------|
| `comment` | commentaire ajoute |
| `delivery` | livrable uploade |
| `status_change` | changement de statut |
| `payment` | paiement verifie |
| `download` | document telecharge |
| `revision` | demande de revision |

### couleurs
| type | couleur |
|------|---------|
| comment | blue |
| delivery | green |
| status_change | purple |
| payment | amber |
| download | gray |

---

## securite

### protection csrf
tous les formulaires utilisent flask-wtf pour la protection csrf.

### validation
- validation des entrees avec wtforms
- validation des types de fichiers
- limitation de taille des uploads

### sessions
- secret key obligatoire
- sessions securisees
- expiration configurable

---

## logging

### configuration
```python
logging.basicConfig(level=logging.DEBUG)
```

### fichiers
- `logs/thedraftclinic.log` - log general
- `logs/errors.log` - erreurs uniquement

### rotation
- taille max: 10mb
- backup count: 5

---

## deploiement

### variables d'environnement
| variable | description |
|----------|-------------|
| `DATABASE_URL` | url postgresql |
| `SESSION_SECRET` | cle secrete sessions |
| `ADMIN_EMAIL` | email admin |
| `ADMIN_PASSWORD` | mot de passe admin |

### production
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

---

<div align="center">

**TheDraftClinic - architecture**

*une base solide pour une application robuste*

</div>
