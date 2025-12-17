# Routes et API TheDraftClinic

Documentation des routes de l'application.

---

## Vue d'ensemble

L'application TheDraftClinic est une application web traditionnelle (pas une API REST). Les routes servent des pages HTML avec des formulaires. Cette documentation liste toutes les routes disponibles.

---

## Routes publiques

Blueprint : `main` (prefixe : `/`)

| Route | Methode | Description |
|-------|---------|-------------|
| `/` | GET | Page d'accueil (landing page) |
| `/services` | GET | Presentation des services |
| `/about` | GET | Page a propos |
| `/contact` | GET | Page de contact |
| `/page/<slug>` | GET | Page dynamique (CGU, CGV, etc.) |

---

## Routes d'authentification

Blueprint : `auth` (prefixe : `/auth`)

| Route | Methode | Description |
|-------|---------|-------------|
| `/auth/login` | GET, POST | Connexion utilisateur |
| `/auth/register` | GET, POST | Inscription |
| `/auth/logout` | GET | Deconnexion |

### Formulaire de connexion

Champs :
- `email` : Adresse email
- `password` : Mot de passe
- `remember` : Case a cocher "Se souvenir de moi"

### Formulaire d'inscription

Champs :
- `email` : Adresse email (unique)
- `password` : Mot de passe
- `confirm_password` : Confirmation
- `first_name` : Prenom
- `last_name` : Nom
- `phone` : Telephone (optionnel)
- `institution` : Etablissement (optionnel)
- `academic_level` : Niveau academique
- `field_of_study` : Domaine d'etude (optionnel)

---

## Routes client

Blueprint : `client` (prefixe : `/client`)

Toutes les routes necessitent une authentification et un compte client (non-admin).

| Route | Methode | Description |
|-------|---------|-------------|
| `/client/dashboard` | GET | Tableau de bord client |
| `/client/new-request` | GET, POST | Nouvelle demande |
| `/client/request/<id>` | GET | Detail d'une demande |
| `/client/request/<id>/accept-quote` | POST | Accepter un devis |
| `/client/request/<id>/submit-payment` | POST | Soumettre un paiement |
| `/client/request/<id>/download/<doc_id>` | GET | Telecharger un document |
| `/client/request/<id>/request-revision` | POST | Demander une revision |
| `/client/request/<id>/add-comment` | POST | Ajouter un commentaire |
| `/client/profile` | GET, POST | Profil utilisateur |
| `/client/deadline-extension/<id>/respond` | POST | Repondre a une extension |

### Formulaire nouvelle demande

Champs :
- `service_type` : Type de service (select)
- `title` : Titre du projet
- `description` : Description detaillee
- `word_count` : Nombre de mots
- `pages_count` : Nombre de pages
- `deadline` : Date limite
- `urgency_level` : Niveau d'urgence
- `additional_info` : Informations supplementaires
- `documents` : Fichiers a uploader (multiple)

### Formulaire de paiement

Champs :
- `amount` : Montant paye
- `payment_method` : Methode de paiement
- `transaction_reference` : Reference de transaction
- `proof_document` : Fichier de preuve
- `notes` : Notes (optionnel)

---

## Routes administration

Blueprint : `admin` (prefixe : `/admin`)

Toutes les routes necessitent un compte administrateur.

| Route | Methode | Description |
|-------|---------|-------------|
| `/admin/dashboard` | GET | Tableau de bord admin |
| `/admin/requests` | GET | Liste des demandes |
| `/admin/request/<id>` | GET | Detail d'une demande |
| `/admin/request/<id>/send-quote` | POST | Envoyer un devis |
| `/admin/request/<id>/update-status` | POST | Mettre a jour le statut |
| `/admin/request/<id>/upload-deliverable` | POST | Uploader un livrable |
| `/admin/request/<id>/add-comment` | POST | Ajouter un commentaire |
| `/admin/request/<id>/request-deadline-extension` | POST | Demander une extension |
| `/admin/payment/<id>/verify` | POST | Verifier un paiement |
| `/admin/users` | GET | Liste des utilisateurs |
| `/admin/user/<id>` | GET | Detail d'un utilisateur |

### Formulaire de devis

Champs :
- `quote_amount` : Montant total
- `deposit_required` : Acompte requis
- `quote_message` : Message d'accompagnement

### Formulaire de statut

Champs :
- `status` : Nouveau statut
- `progress` : Pourcentage de progression
- `admin_notes` : Notes internes

### Formulaire de livrable

Champs :
- `deliverable` : Fichier a uploader
- `delivery_comment` : Commentaire de livraison

### Verification de paiement

Champs :
- `action` : 'approve' ou 'reject'
- `rejection_reason` : Raison du rejet (si rejete)

---

## Routes parametres admin

Blueprint : `admin_settings` (prefixe : `/admin`)

| Route | Methode | Description |
|-------|---------|-------------|
| `/admin/settings` | GET | Index des parametres |
| `/admin/settings/general` | GET, POST | Parametres generaux |
| `/admin/settings/branding` | GET, POST | Logo et favicon |
| `/admin/settings/seo` | GET, POST | SEO et OpenGraph |
| `/admin/settings/legal` | GET, POST | Informations legales |
| `/admin/settings/advanced` | GET, POST | Parametres avances |
| `/admin/pages` | GET | Liste des pages |
| `/admin/pages/new` | GET, POST | Nouvelle page |
| `/admin/pages/<id>/edit` | GET, POST | Modifier une page |
| `/admin/pages/<id>/delete` | POST | Supprimer une page |
| `/admin/stats` | GET | Statistiques |
| `/admin/payments` | GET | Liste des paiements |
| `/admin/languages` | GET | Liste des langues |
| `/admin/languages/<code>` | GET | Voir/editer une langue |
| `/admin/languages/<code>/save` | POST | Sauvegarder les traductions |
| `/admin/languages/<code>/download` | GET | Telecharger le JSON |
| `/admin/languages/<code>/upload` | POST | Importer un JSON |

---

## Parametres de requete

### Filtrage des demandes

`/admin/requests?status=<status>`

Valeurs possibles :
- `all` : Toutes les demandes
- `submitted` : Soumises
- `under_review` : En examen
- `quote_sent` : Devis envoyes
- `in_progress` : En cours
- `completed` : Terminees
- `delivered` : Livrees

### Filtrage des paiements

`/admin/payments?status=<status>`

Valeurs possibles :
- `all` : Tous les paiements
- `pending` : En attente
- `verified` : Verifies
- `rejected` : Rejetes

### Changement de langue

`?lang=<code>`

Appliquable sur toutes les pages. Codes disponibles :
- `fr` : Francais
- `en` : Anglais

---

## Modeles de donnees

### User
```
id              : Integer (cle primaire)
email           : String (unique)
password_hash   : String
first_name      : String
last_name       : String
phone           : String (optionnel)
institution     : String (optionnel)
academic_level  : String (optionnel)
is_admin        : Boolean
admin_role      : String (super_admin, admin)
account_active  : Boolean
created_at      : DateTime
```

### ServiceRequest
```
id                  : Integer (cle primaire)
user_id             : Integer (FK -> users)
service_type        : String (thesis, dissertation, etc.)
title               : String
description         : Text
status              : String
progress_percentage : Integer (0-100)
quote_amount        : Float
deposit_required    : Float
deadline            : DateTime
created_at          : DateTime
delivered_at        : DateTime
```

### Payment
```
id                    : Integer (cle primaire)
request_id            : Integer (FK -> service_requests)
amount                : Float
payment_type          : String (deposit, final, full)
payment_method        : String
proof_document        : String
transaction_reference : String
status                : String (pending, verified, rejected)
verified_by           : Integer (FK -> users)
created_at            : DateTime
```

### Document
```
id                : Integer (cle primaire)
request_id        : Integer (FK -> service_requests)
filename          : String
original_filename : String
file_type         : String
document_type     : String (client_upload, deliverable, etc.)
uploaded_by       : Integer (FK -> users)
created_at        : DateTime
```

### ActivityLog
```
id                   : Integer (cle primaire)
request_id           : Integer (FK -> service_requests)
user_id              : Integer (FK -> users)
action_type          : String
title                : String
description          : Text
metadata_json        : Text (JSON)
is_visible_to_client : Boolean
created_at           : DateTime
```

---

## Codes de reponse

| Code | Signification |
|------|---------------|
| 200 | Succes |
| 302 | Redirection |
| 400 | Requete invalide |
| 403 | Acces interdit |
| 404 | Ressource non trouvee |
| 500 | Erreur serveur |

---

## Statuts des demandes

| Code | Libelle |
|------|---------|
| submitted | Soumise |
| under_review | En examen |
| quote_sent | Devis envoye |
| quote_accepted | Devis accepte |
| awaiting_deposit | Attente acompte |
| deposit_pending | Acompte en verification |
| in_progress | En cours |
| revision | En revision |
| completed | Terminee |
| delivered | Livree |
| cancelled | Annulee |
| rejected | Refusee |

---

## Types d'actions (ActivityLog)

| Code | Description |
|------|-------------|
| comment | Commentaire ajoute |
| delivery | Livrable uploade |
| revision_request | Demande de revision |
| revision_delivery | Revision livree |
| download | Document telecharge |
| status_change | Statut modifie |
| progress_update | Progression mise a jour |
| deadline_extension_request | Extension demandee |
| deadline_extension_approved | Extension approuvee |
| deadline_extension_rejected | Extension refusee |
| quote_sent | Devis envoye |
| quote_accepted | Devis accepte |
| payment_submitted | Paiement soumis |
| payment_verified | Paiement verifie |
| document_upload | Document uploade |

---

## Redirections

### Apres connexion

- Admin : `/admin/dashboard`
- Client : `/client/dashboard`
- Parametre `next` : URL de destination

### Acces non autorise

- Non connecte : `/auth/login`
- Client vers admin : `/`
- Admin vers client : `/admin/dashboard`

---

## Messages flash

Les messages flash sont affiches apres les actions :

| Categorie | Utilisation |
|-----------|-------------|
| `success` | Action reussie |
| `error` | Erreur ou echec |
| `warning` | Avertissement |
| `info` | Information |

---

## Protection CSRF

Tous les formulaires POST incluent un token CSRF obligatoire.

```html
<form method="POST">
    {{ form.csrf_token }}
    ...
</form>
```

---

## Fichiers statiques

| Chemin | Contenu |
|--------|---------|
| `/static/css/` | Feuilles de style |
| `/static/js/` | Scripts JavaScript |
| `/static/uploads/` | Fichiers uploades |
| `/static/uploads/branding/` | Logo, favicon, images OG |

---

## Notes techniques

### Uploads

- Taille max : 50 MB
- Extensions : pdf, doc, docx, txt, rtf, odt, png, jpg, jpeg, gif
- Stockage : `/static/uploads/`
- Nommage : UUID + nom original

### Sessions

- Gerees par Flask-Login
- Cle secrete via SESSION_SECRET
- Option "Se souvenir de moi" disponible

---

*TheDraftClinic - Documentation des routes v1.0*
