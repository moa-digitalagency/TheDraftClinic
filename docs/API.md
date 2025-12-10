# Documentation API TheDraftClinic

**Par MOA Digital Agency LLC**

## Introduction

Cette documentation décrit l'API interne de TheDraftClinic. L'application utilise principalement des routes web traditionnelles (form-based), mais cette documentation détaille les endpoints disponibles et leur fonctionnement.

This documentation describes TheDraftClinic's internal API. The application primarily uses traditional web routes (form-based), but this documentation details the available endpoints and their operation.

---

## Authentification / Authentication

### Session-Based Auth

TheDraftClinic utilise Flask-Login pour la gestion des sessions.

```
POST /auth/login
POST /auth/register
GET  /auth/logout
```

### Protection CSRF

Tous les formulaires POST incluent un token CSRF:
```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

---

## Endpoints Publics / Public Endpoints

### Pages

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Page d'accueil / Landing page |
| GET | `/services` | Liste des services |
| GET | `/about` | À propos |
| GET | `/contact` | Contact |
| GET | `/page/<slug>` | Page dynamique (CGU, CGV, etc.) |

---

## Endpoints Client / Client Endpoints

Tous les endpoints client nécessitent une authentification.
All client endpoints require authentication.

### Dashboard

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/client/dashboard` | Tableau de bord client |

### Demandes / Requests

| Méthode | URL | Description |
|---------|-----|-------------|
| GET, POST | `/client/new-request` | Créer une demande |
| GET | `/client/request/<id>` | Détail d'une demande |
| POST | `/client/request/<id>/accept-quote` | Accepter un devis |
| POST | `/client/request/<id>/submit-payment` | Soumettre un paiement |
| POST | `/client/request/<id>/request-revision` | Demander une révision |
| POST | `/client/request/<id>/add-comment` | Ajouter un commentaire |
| GET | `/client/request/<id>/download/<doc_id>` | Télécharger un document |

### Extension de Délai / Deadline Extension

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/client/deadline-extension/<id>/respond` | Répondre à une extension |

### Profil / Profile

| Méthode | URL | Description |
|---------|-----|-------------|
| GET, POST | `/client/profile` | Gérer le profil |

---

## Endpoints Administration / Admin Endpoints

Tous les endpoints admin nécessitent une authentification admin.
All admin endpoints require admin authentication.

### Dashboard

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/admin/dashboard` | Tableau de bord admin |
| GET | `/admin/stats` | Statistiques et traçabilité |

### Gestion des Demandes / Request Management

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/admin/requests` | Liste des demandes |
| GET | `/admin/request/<id>` | Détail d'une demande |
| POST | `/admin/request/<id>/create-quote` | Créer un devis |
| POST | `/admin/request/<id>/update-status` | Mettre à jour le statut |
| POST | `/admin/request/<id>/upload-deliverable` | Upload livrable |
| POST | `/admin/request/<id>/add-comment` | Ajouter un commentaire |
| POST | `/admin/request/<id>/request-deadline-extension` | Demander extension |

### Révisions / Revisions

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/admin/revision/<id>/handle` | Traiter une révision |

### Paiements / Payments

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/admin/payment/<id>/verify` | Vérifier un paiement |

### Utilisateurs / Users

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/admin/users` | Liste des utilisateurs |
| GET | `/admin/user/<id>` | Détail d'un utilisateur |

### Paramètres / Settings

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/admin/settings` | Menu paramètres |
| GET, POST | `/admin/settings/general` | Paramètres généraux |
| GET, POST | `/admin/settings/branding` | Logo et favicon |
| GET, POST | `/admin/settings/seo` | SEO et OpenGraph |
| GET, POST | `/admin/settings/legal` | Infos légales |
| GET, POST | `/admin/settings/advanced` | Analytics et scripts |

### Pages Dynamiques / Dynamic Pages

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/admin/pages` | Liste des pages |
| GET, POST | `/admin/pages/new` | Nouvelle page |
| GET, POST | `/admin/pages/<id>/edit` | Modifier une page |
| POST | `/admin/pages/<id>/delete` | Supprimer une page |

---

## Modèles de Données / Data Models

### User
```python
{
    "id": int,
    "email": str,
    "first_name": str,
    "last_name": str,
    "phone": str,
    "institution": str,
    "academic_level": str,
    "is_admin": bool,
    "created_at": datetime
}
```

### ServiceRequest
```python
{
    "id": int,
    "user_id": int,
    "service_type": str,  # "thesis", "dissertation", "article", etc.
    "title": str,
    "description": str,
    "status": str,  # "pending", "quoted", "in_progress", "delivered", etc.
    "deadline": datetime,
    "progress_percentage": int,
    "quoted_price": float,
    "quote_currency": str,
    "created_at": datetime,
    "delivered_at": datetime
}
```

### ActivityLog
```python
{
    "id": int,
    "request_id": int,
    "user_id": int,
    "action_type": str,  # "delivery", "download", "comment", etc.
    "title": str,
    "description": str,
    "metadata": json,
    "visible_to_client": bool,
    "created_at": datetime
}
```

### Page
```python
{
    "id": int,
    "title": str,
    "slug": str,
    "content": str,
    "content_format": str,  # "html" ou "markdown"
    "page_type": str,  # "cgu", "cgv", "privacy", "custom"
    "is_published": bool,
    "show_in_footer": bool,
    "show_in_navigation": bool,
    "meta_title": str,
    "meta_description": str,
    "created_at": datetime
}
```

---

## Codes de Statut / Status Codes

### Statuts de Demande / Request Status
| Code | Label FR | Label EN |
|------|----------|----------|
| `pending` | En attente | Pending |
| `quoted` | Devis envoyé | Quote sent |
| `quote_accepted` | Devis accepté | Quote accepted |
| `awaiting_deposit` | Attente acompte | Awaiting deposit |
| `deposit_pending` | Vérification acompte | Deposit pending |
| `in_progress` | En cours | In progress |
| `revision` | En révision | In revision |
| `awaiting_final` | Attente solde | Awaiting final |
| `delivered` | Livré | Delivered |
| `completed` | Terminé | Completed |
| `cancelled` | Annulé | Cancelled |

### Types d'Actions / Action Types
| Type | Description |
|------|-------------|
| `delivery` | Livraison d'un document |
| `download` | Téléchargement par le client |
| `comment` | Commentaire |
| `status_change` | Changement de statut |
| `progress_update` | Mise à jour progression |
| `revision_request` | Demande de révision |
| `revision_delivery` | Livraison révision |
| `deadline_extension_request` | Demande extension |
| `deadline_extension_approved` | Extension approuvée |

---

## Erreurs / Errors

### Codes HTTP
| Code | Description |
|------|-------------|
| 200 | Succès |
| 302 | Redirection |
| 400 | Mauvaise requête |
| 401 | Non authentifié |
| 403 | Accès refusé |
| 404 | Non trouvé |
| 500 | Erreur serveur |

### Messages Flash
Les messages sont affichés via le système flash de Flask:
```python
flash('Message de succès', 'success')
flash('Message d\'erreur', 'error')
flash('Message d\'avertissement', 'warning')
```

---

**MOA Digital Agency LLC** - www.myoneart.com
