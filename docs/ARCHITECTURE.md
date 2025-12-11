# 🏗️ Architecture TheDraftClinic

> **Documentation technique de l'architecture**

---

## 📖 Vue d'ensemble

TheDraftClinic est une application web Flask suivant une architecture MVC (Modele-Vue-Controleur) avec une separation claire des responsabilites.

---

## 🧱 Couches de l'Application

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

## 📁 Structure des Dossiers

### `/models` - Modeles de donnees

| Fichier | Description |
|---------|-------------|
| `user.py` | Modele utilisateur avec authentification |
| `request.py` | Modele demande de service |
| `document.py` | Modele document/fichier |
| `payment.py` | Modele paiement |
| `activity_log.py` | Modele historique d'activites |
| `site_settings.py` | Modele parametres du site |
| `page.py` | Modele pages dynamiques |

### `/routes` - Controleurs

| Fichier | Prefix | Description |
|---------|--------|-------------|
| `main.py` | `/` | Pages publiques |
| `auth.py` | `/auth` | Authentification |
| `client.py` | `/client` | Espace client |
| `admin.py` | `/admin` | Administration |
| `admin_settings.py` | `/admin/settings` | Parametres admin |

### `/templates` - Vues

| Dossier | Description |
|---------|-------------|
| `layouts/` | Templates de base |
| `admin/` | Templates admin |
| `client/` | Templates client |
| `auth/` | Templates authentification |
| `errors/` | Pages d'erreur |

### `/services` - Services metier

| Fichier | Description |
|---------|-------------|
| `admin_service.py` | Logique admin |
| `file_service.py` | Gestion des fichiers |

### `/security` - Securite

| Fichier | Description |
|---------|-------------|
| `decorators.py` | Decorateurs d'autorisation |
| `validators.py` | Validation des entrees |
| `rate_limiter.py` | Limitation de taux |
| `error_handlers.py` | Gestionnaires d'erreurs |

---

## 🔐 Authentification

### Flask-Login
L'authentification utilise Flask-Login avec:
- Sessions securisees
- Remember me (se souvenir de moi)
- Protection des routes

### Decorateurs
```python
@login_required          # Connexion requise
@admin_required          # Admin uniquement
@client_required         # Client uniquement
```

---

## 🗄️ Base de Donnees

### Schema Relationnel

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

### Modeles Principaux

#### User
- id, email, password_hash
- first_name, last_name
- phone, institution
- academic_level, field_of_study
- is_admin, is_active
- created_at, updated_at

#### ServiceRequest
- id, user_id, title
- service_type, description
- status, progress_percentage
- quote_amount, deposit_required
- deadline, created_at

#### Payment
- id, request_id, amount
- payment_method, status
- proof_document, transaction_reference
- created_at

#### ActivityLog
- id, request_id, user_id
- action_type, title
- description, metadata
- created_at

---

## 🎨 Templates

### Layouts
L'application utilise des templates de base:

| Layout | Description |
|--------|-------------|
| `base.html` | Layout de base commun |
| `admin_base.html` | Layout admin avec sidebar |

### Heritage
```
base.html
├── layouts/auth_base.html
├── layouts/client_base.html
└── layouts/admin_base.html
    └── admin/*.html
```

---

## 🔄 Workflow des Demandes

### Statuts
1. `submitted` - Soumise
2. `under_review` - En examen
3. `quote_sent` - Devis envoye
4. `quote_accepted` - Devis accepte
5. `awaiting_deposit` - Attente acompte
6. `in_progress` - En cours
7. `revision` - En revision
8. `completed` - Terminee
9. `delivered` - Livree
10. `cancelled` - Annulee

### Transitions
```
submitted → under_review → quote_sent → quote_accepted
    ↓                                        ↓
cancelled                             awaiting_deposit
                                            ↓
                                       in_progress
                                            ↓
                                      revision ←→ completed
                                                    ↓
                                                delivered
```

---

## 📊 Historique d'Activites

### Types d'Actions
| Type | Description |
|------|-------------|
| `comment` | Commentaire ajoute |
| `delivery` | Livrable uploade |
| `status_change` | Changement de statut |
| `payment` | Paiement verifie |
| `download` | Document telecharge |
| `revision` | Demande de revision |

### Couleurs
| Type | Couleur |
|------|---------|
| comment | blue |
| delivery | green |
| status_change | purple |
| payment | amber |
| download | gray |

---

## 🛡️ Securite

### Protection CSRF
Tous les formulaires utilisent Flask-WTF pour la protection CSRF.

### Validation
- Validation des entrees avec WTForms
- Validation des types de fichiers
- Limitation de taille des uploads

### Sessions
- Secret key obligatoire
- Sessions securisees
- Expiration configurable

---

## 📝 Logging

### Configuration
```python
logging.basicConfig(level=logging.DEBUG)
```

### Fichiers
- `logs/thedraftclinic.log` - Log general
- `logs/errors.log` - Erreurs uniquement

### Rotation
- Taille max: 10MB
- Backup count: 5

---

## 🚀 Deploiement

### Variables d'Environnement
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | URL PostgreSQL |
| `SESSION_SECRET` | Cle secrete sessions |
| `ADMIN_EMAIL` | Email admin |
| `ADMIN_PASSWORD` | Mot de passe admin |

### Production
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

---

<div align="center">

**🏗️ TheDraftClinic - Architecture**

*Une base solide pour une application robuste*

</div>
