# Architecture TheDraftClinic

> Documentation technique de l'architecture

---

## Vue d'ensemble

TheDraftClinic est une application web Flask suivant une architecture MVC (Modèle-Vue-Contrôleur) avec une séparation claire des responsabilités.

---

## Couches de l'application

```
┌─────────────────────────────────────────────────┐
│                   Templates                      │
│            (Jinja2 + TailwindCSS)               │
├─────────────────────────────────────────────────┤
│                    Routes                        │
│             (Blueprints Flask)                   │
├─────────────────────────────────────────────────┤
│                   Services                       │
│            (Logique métier)                     │
├─────────────────────────────────────────────────┤
│                   Modèles                        │
│              (SQLAlchemy ORM)                   │
├─────────────────────────────────────────────────┤
│                 Base de données                  │
│                 (PostgreSQL)                    │
└─────────────────────────────────────────────────┘
```

---

## Structure des dossiers

### `/models` - Modèles de données

| Fichier | Description |
|---------|-------------|
| `user.py` | Modèle utilisateur avec authentification et rôles admin |
| `request.py` | Modèle demande de service |
| `document.py` | Modèle document/fichier |
| `payment.py` | Modèle paiement |
| `activity_log.py` | Modèle historique d'activités |
| `site_settings.py` | Modèle paramètres du site |
| `page.py` | Modèle pages dynamiques |

### `/routes` - Contrôleurs

| Fichier | Préfixe | Description |
|---------|--------|-------------|
| `main.py` | `/` | Pages publiques |
| `auth.py` | `/auth` | Authentification |
| `client.py` | `/client` | Espace client |
| `admin.py` | `/admin` | Administration |
| `admin_settings.py` | `/admin/settings` | Paramètres admin |

### `/templates` - Vues

| Dossier | Description |
|---------|-------------|
| `layouts/` | Templates de base |
| `admin/` | Templates admin |
| `client/` | Templates client |
| `auth/` | Templates authentification |
| `errors/` | Pages d'erreur |

### `/services` - Services métier

| Fichier | Description |
|---------|-------------|
| `admin_service.py` | Logique admin et création super admin |
| `file_service.py` | Gestion des fichiers |

### `/security` - Sécurité

| Fichier | Description |
|---------|-------------|
| `decorators.py` | Décorateurs d'autorisation |
| `validators.py` | Validation des entrées |
| `rate_limiter.py` | Limitation de taux |
| `error_handlers.py` | Gestionnaires d'erreurs |

---

## Authentification

### Flask-Login
L'authentification utilise Flask-Login avec :
- Sessions sécurisées
- Remember me (se souvenir de moi)
- Protection des routes

### Décorateurs
```python
@login_required          # Connexion requise
@admin_required          # Admin uniquement
@super_admin_required    # Super admin uniquement
@client_required         # Client uniquement
```

---

## Système de rôles admin

### Rôles disponibles
- `super_admin` - Premier compte admin, tous les droits
- `admin` - Administrateur standard

### Permissions
| Action | Admin | Super admin |
|--------|-------|-------------|
| Gérer demandes | Oui | Oui |
| Gérer utilisateurs | Oui | Oui |
| Paramètres site | Oui | Oui |
| Ajouter admin | Non | Oui |
| Modifier rôle admin | Non | Oui |
| Désactiver admin | Non | Oui |

---

## Base de données

### Schéma relationnel

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

### Modèles principaux

#### User
- id, email, password_hash
- first_name, last_name
- phone, institution
- academic_level, field_of_study
- is_admin, admin_role
- account_active
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

## Templates

### Layouts
L'application utilise des templates de base :

| Layout | Description |
|--------|-------------|
| `base.html` | Layout de base commun |
| `admin_base.html` | Layout admin avec sidebar |

### Héritage
```
base.html
├── layouts/auth_base.html
├── layouts/client_base.html
└── layouts/admin_base.html
    └── admin/*.html
```

---

## Workflow des demandes

### Statuts
1. `submitted` - Soumise
2. `under_review` - En examen
3. `quote_sent` - Devis envoyé
4. `quote_accepted` - Devis accepté
5. `awaiting_deposit` - Attente acompte
6. `in_progress` - En cours
7. `revision` - En révision
8. `completed` - Terminée
9. `delivered` - Livrée
10. `cancelled` - Annulée

### Transitions
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

## Historique d'activités

### Types d'actions
| Type | Description |
|------|-------------|
| `comment` | Commentaire ajouté |
| `delivery` | Livrable uploadé |
| `status_change` | Changement de statut |
| `payment` | Paiement vérifié |
| `download` | Document téléchargé |
| `revision` | Demande de révision |

### Couleurs
| Type | Couleur |
|------|---------|
| comment | Bleu |
| delivery | Vert |
| status_change | Violet |
| payment | Ambre |
| download | Gris |

---

## Sécurité

### Protection CSRF
Tous les formulaires utilisent Flask-WTF pour la protection CSRF.

### Validation
- Validation des entrées avec WTForms
- Validation des types de fichiers
- Limitation de taille des uploads

### Sessions
- Secret key obligatoire
- Sessions sécurisées
- Expiration configurable

---

## Logging

### Configuration
```python
logging.basicConfig(level=logging.DEBUG)
```

### Fichiers
- `logs/thedraftclinic.log` - Log général
- `logs/errors.log` - Erreurs uniquement

### Rotation
- Taille max : 10MB
- Backup count : 5

---

## Déploiement

### Variables d'environnement
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | URL PostgreSQL |
| `SESSION_SECRET` | Clé secrète sessions |
| `ADMIN_EMAIL` | Email admin |
| `ADMIN_PASSWORD` | Mot de passe admin |

### Production
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

---

<div align="center">

**TheDraftClinic - Architecture**

*Une base solide pour une application robuste*

</div>
