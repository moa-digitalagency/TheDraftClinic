# Modeles de donnees TheDraftClinic

Documentation technique des modeles de la base de donnees.

---

## Vue d'ensemble

L'application utilise PostgreSQL avec SQLAlchemy comme ORM. Les modeles sont definis dans le dossier `/models`.

---

## User (Utilisateur)

Table : `users`

Represente un utilisateur de la plateforme (client ou administrateur).

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| email | String(120) | Email unique, utilise pour la connexion |
| password_hash | String(256) | Hash du mot de passe (pbkdf2:sha256) |
| first_name | String(50) | Prenom |
| last_name | String(50) | Nom de famille |
| phone | String(20) | Telephone (optionnel) |
| institution | String(200) | Etablissement academique |
| academic_level | String(50) | Niveau d'etudes |
| field_of_study | String(100) | Domaine de recherche |
| is_admin | Boolean | True si administrateur |
| admin_role | String(20) | 'super_admin' ou 'admin' |
| account_active | Boolean | True si compte actif |
| created_at | DateTime | Date de creation |
| updated_at | DateTime | Derniere modification |

### Relations

- `requests` : Demandes de service soumises par l'utilisateur (1:N)

### Methodes

| Methode | Description |
|---------|-------------|
| `set_password(password)` | Hash et stocke le mot de passe |
| `check_password(password)` | Verifie le mot de passe |
| `full_name` | Retourne prenom + nom |
| `is_active` | Propriete Flask-Login |
| `is_super_admin` | Verifie si super admin |
| `can_manage_admins()` | Verifie les droits de gestion admin |

---

## ServiceRequest (Demande de service)

Table : `service_requests`

Represente une demande de service de redaction academique.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| user_id | Integer | FK vers users |
| service_type | String(100) | Code du type de service |
| title | String(300) | Titre du projet |
| description | Text | Description detaillee |
| additional_info | Text | Notes supplementaires |
| word_count | Integer | Nombre de mots |
| pages_count | Integer | Nombre de pages |
| deadline | DateTime | Date limite |
| urgency_level | String(20) | standard, express_24h, express_5h |
| status | String(30) | Statut actuel |
| progress_percentage | Integer | Progression (0-100) |
| quote_amount | Float | Montant du devis |
| quote_message | Text | Message du devis |
| quote_sent_at | DateTime | Date d'envoi du devis |
| quote_accepted | Boolean | Devis accepte |
| deposit_required | Float | Montant de l'acompte |
| deposit_paid | Boolean | Acompte paye |
| admin_notes | Text | Notes internes |
| rejection_reason | Text | Raison de rejet |
| created_at | DateTime | Date de creation |
| updated_at | DateTime | Derniere modification |
| delivered_at | DateTime | Date de livraison |

### Relations

- `user` : Utilisateur ayant soumis la demande
- `documents` : Documents associes (1:N)
- `payments` : Paiements effectues (1:N)
- `activity_logs` : Historique d'activite
- `deadline_extensions` : Extensions de delai
- `revision_requests` : Demandes de revision

### Constantes

#### STATUS_CHOICES

| Code | Libelle |
|------|---------|
| submitted | Soumise |
| under_review | En examen |
| quote_sent | Devis envoye |
| quote_accepted | Devis accepte |
| awaiting_deposit | En attente d'acompte |
| deposit_pending | Acompte en verification |
| in_progress | En cours de traitement |
| revision | En revision |
| completed | Terminee |
| delivered | Livree |
| cancelled | Annulee |
| rejected | Refusee |

#### SERVICE_TYPES

| Code | Libelle |
|------|---------|
| thesis | These de doctorat |
| dissertation | Memoire de master |
| research_proposal | Proposition de recherche |
| academic_proposal | Proposition academique |
| book_chapter | Chapitre de livre |
| research_paper | Article de recherche |
| literature_review | Revue de litterature |
| proofreading | Relecture et correction |
| editing | Edition academique |
| formatting | Mise en forme |
| consultation | Consultation academique |
| cv_resume | CV academique |
| personal_statement | Lettre de motivation |
| grant_proposal | Proposition de subvention |
| poster_review | Revision de poster |
| other | Autre service |

---

## Payment (Paiement)

Table : `payments`

Represente un paiement effectue par un client.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| request_id | Integer | FK vers service_requests |
| amount | Float | Montant paye |
| payment_type | String(30) | deposit, final, full |
| payment_method | String(50) | Methode utilisee |
| proof_document | String(255) | Nom du fichier de preuve |
| transaction_reference | String(100) | Reference de transaction |
| status | String(20) | pending, verified, rejected |
| verified_by | Integer | FK vers users (admin) |
| verified_at | DateTime | Date de verification |
| rejection_reason | Text | Raison du rejet |
| notes | Text | Notes du client |
| created_at | DateTime | Date de creation |
| updated_at | DateTime | Derniere modification |

### Relations

- `request` : Demande de service associee

### Constantes

| Code status | Libelle |
|-------------|---------|
| pending | En attente |
| verified | Verifie |
| rejected | Rejete |

---

## Document

Table : `documents`

Represente un fichier uploade dans le systeme.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| request_id | Integer | FK vers service_requests |
| filename | String(255) | Nom unique sur le serveur |
| original_filename | String(255) | Nom original du fichier |
| file_type | String(50) | Type MIME |
| file_size | Integer | Taille en octets |
| document_type | String(30) | Categorie du document |
| description | Text | Description |
| uploaded_by | Integer | FK vers users |
| created_at | DateTime | Date d'upload |

### Relations

- `request` : Demande de service associee

### Types de documents

| Code | Libelle | Description |
|------|---------|-------------|
| client_upload | Document client | Uploade par le client |
| admin_upload | Document admin | Ajoute par l'admin |
| deliverable | Livrable | Travail final |
| revision | Revision | Version revisee |

---

## ActivityLog (Journal d'activite)

Table : `activity_logs`

Enregistre toutes les actions sur les projets.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| request_id | Integer | FK vers service_requests |
| user_id | Integer | FK vers users |
| action_type | String(50) | Type d'action |
| title | String(200) | Titre de l'action |
| description | Text | Description detaillee |
| metadata_json | Text | Donnees supplementaires (JSON) |
| is_visible_to_client | Boolean | Visible par le client |
| created_at | DateTime | Date de l'action |

### Relations

- `user` : Utilisateur ayant effectue l'action
- `service_request` : Demande concernee

### Types d'action

| Code | Libelle | Icone | Couleur |
|------|---------|-------|---------|
| comment | Commentaire | message-circle | blue |
| delivery | Livraison | package | green |
| revision_request | Demande de revision | edit-3 | orange |
| revision_delivery | Livraison revision | check-circle | green |
| download | Telechargement | download | gray |
| status_change | Changement de statut | refresh-cw | purple |
| deadline_extension_request | Demande extension | clock | yellow |
| deadline_extension_approved | Extension approuvee | check | green |
| deadline_extension_rejected | Extension refusee | x | red |
| quote_sent | Devis envoye | file-text | blue |
| quote_accepted | Devis accepte | thumbs-up | green |
| payment_submitted | Paiement soumis | credit-card | yellow |
| payment_verified | Paiement verifie | check-square | green |
| document_upload | Document uploade | upload | blue |
| progress_update | Mise a jour progression | trending-up | indigo |

### Methode statique

`log_action(request_id, user_id, action_type, title, description, metadata, visible_to_client)` : Cree une entree de log.

---

## SiteSettings (Parametres du site)

Table : `site_settings`

Stocke les parametres globaux de configuration.

### Colonnes principales

| Groupe | Colonnes |
|--------|----------|
| General | site_name, site_description, timezone, country, default_language, currency |
| Branding | logo_filename, favicon_filename |
| SEO | seo_title, seo_description, seo_keywords |
| OpenGraph | og_title, og_description, og_image_filename, og_type |
| Twitter | twitter_card, twitter_site |
| Legal | company_name, company_address, company_email, company_phone, company_registration, vat_number, legal_status, share_capital, rcs_number, siret_number, ape_code |
| Hebergement | hosting_provider, hosting_address, dpo_name, dpo_email |
| Analytics | google_analytics_id, google_tag_manager_id, facebook_pixel_id |
| Avance | robots_txt_content, custom_head_scripts, custom_body_scripts, maintenance_mode, maintenance_message |

### Methode statique

`get_settings()` : Recupere l'instance unique (la cree si inexistante).

---

## Page (Page dynamique)

Table : `pages`

Gere les pages de contenu (CGU, CGV, mentions legales, etc.).

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| title | String(200) | Titre de la page |
| slug | String(200) | URL unique |
| content | Text | Contenu HTML ou Markdown |
| content_format | String(20) | html ou markdown |
| meta_title | String(70) | Titre SEO |
| meta_description | String(160) | Description SEO |
| is_published | Boolean | Page publiee |
| show_in_footer | Boolean | Afficher dans le footer |
| show_in_navigation | Boolean | Afficher dans la nav |
| order_index | Integer | Ordre d'affichage |
| page_type | String(50) | Type de page |
| created_by | Integer | FK vers users |
| created_at | DateTime | Date de creation |
| updated_at | DateTime | Derniere modification |

### Types de pages

| Code | Libelle |
|------|---------|
| cgu | Conditions Generales d'Utilisation |
| cgv | Conditions Generales de Vente |
| privacy | Politique de Confidentialite |
| legal | Mentions Legales |
| faq | Foire Aux Questions |
| about | A Propos |
| contact | Contact |
| custom | Page Personnalisee |

### Methodes statiques

- `generate_slug(title)` : Genere un slug a partir du titre
- `get_footer_pages()` : Pages a afficher dans le footer
- `get_navigation_pages()` : Pages a afficher dans la navigation

---

## DeadlineExtension (Extension de delai)

Table : `deadline_extensions`

Gere les demandes d'extension de delai.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| request_id | Integer | FK vers service_requests |
| requested_by | Integer | FK vers users (admin) |
| original_deadline | DateTime | Date limite originale |
| new_deadline | DateTime | Nouvelle date proposee |
| reason | Text | Raison de la demande |
| status | String(20) | pending, approved, rejected |
| responded_by | Integer | FK vers users (client) |
| response_message | Text | Message de reponse |
| responded_at | DateTime | Date de reponse |
| created_at | DateTime | Date de creation |

### Methodes

- `get_status_display()` : Libelle du statut
- `get_extension_days()` : Nombre de jours d'extension

---

## RevisionRequest (Demande de revision)

Table : `revision_requests`

Gere les demandes de revision sur les livrables.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| request_id | Integer | FK vers service_requests |
| delivery_document_id | Integer | FK vers documents |
| requested_by | Integer | FK vers users (client) |
| revision_details | Text | Details des modifications |
| status | String(20) | pending, in_progress, completed, rejected |
| admin_response | Text | Reponse de l'admin |
| responded_by | Integer | FK vers users (admin) |
| responded_at | DateTime | Date de reponse |
| created_at | DateTime | Date de creation |
| updated_at | DateTime | Derniere modification |

### Relations

- `attachments` : Fichiers joints a la demande de revision

---

## RevisionAttachment (Piece jointe revision)

Table : `revision_attachments`

Fichiers joints aux demandes de revision.

### Colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Cle primaire |
| revision_request_id | Integer | FK vers revision_requests |
| filename | String(255) | Nom sur le serveur |
| original_filename | String(255) | Nom original |
| file_type | String(50) | Type MIME |
| file_size | Integer | Taille en octets |
| uploaded_by | Integer | FK vers users |
| created_at | DateTime | Date d'upload |

---

*TheDraftClinic - Documentation des modeles v1.0*
