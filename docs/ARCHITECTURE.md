# Architecture TheDraftClinic

Documentation technique de l'architecture de la plateforme.

---

## Presentation generale

TheDraftClinic est une plateforme de services de redaction academique developpee avec Flask. Elle suit une architecture MVC (Modele-Vue-Controleur) avec une separation claire des responsabilites.

L'application permet aux chercheurs et doctorants de soumettre des demandes de redaction academique (theses, memoires, articles), de recevoir des devis, de payer et de suivre l'avancement de leurs projets.

---

## Schema des couches

```
+---------------------------------------------------+
|                   PRESENTATION                     |
|    Templates Jinja2 + TailwindCSS + JavaScript    |
+---------------------------------------------------+
                        |
+---------------------------------------------------+
|                   CONTROLEURS                      |
|           Blueprints Flask (Routes)               |
+---------------------------------------------------+
                        |
+---------------------------------------------------+
|                    SERVICES                        |
|            Logique metier regroupe                |
+---------------------------------------------------+
                        |
+---------------------------------------------------+
|                    MODELES                         |
|              SQLAlchemy ORM                       |
+---------------------------------------------------+
                        |
+---------------------------------------------------+
|                BASE DE DONNEES                     |
|                 PostgreSQL                        |
+---------------------------------------------------+
```

---

## Organisation des dossiers

### Racine du projet

| Fichier | Role |
|---------|------|
| `app.py` | Point d'entree, configuration Flask, initialisation des extensions |
| `main.py` | Demarrage de l'application (import de app) |
| `pyproject.toml` | Configuration du projet Python et dependances |
| `requirements.txt` | Liste des packages Python |

### /models - Couche de donnees

Les modeles SQLAlchemy definissent la structure de la base de donnees.

| Fichier | Description |
|---------|-------------|
| `user.py` | Utilisateurs (clients et admins), authentification, hash mot de passe |
| `request.py` | Demandes de service avec cycle de vie complet |
| `document.py` | Documents uploades (client, admin, livrables) |
| `payment.py` | Paiements et preuves, verification par admin |
| `activity_log.py` | Historique des actions sur les projets |
| `site_settings.py` | Configuration globale du site |
| `page.py` | Pages dynamiques (CGU, CGV, mentions legales) |
| `deadline_extension.py` | Demandes d'extension de delai |
| `revision_request.py` | Demandes de revision sur livrables |

### /routes - Controleurs

Les blueprints Flask regroupent les routes par domaine fonctionnel.

| Fichier | Prefixe URL | Role |
|---------|-------------|------|
| `main.py` | `/` | Pages publiques (accueil, services, contact) |
| `auth.py` | `/auth` | Authentification (login, register, logout) |
| `client.py` | `/client` | Espace client (dashboard, demandes, profil) |
| `admin.py` | `/admin` | Administration (demandes, utilisateurs, paiements) |
| `admin_settings.py` | `/admin` | Parametres du site, pages, langues, stats |

### /templates - Vues

Templates Jinja2 organises par section.

| Dossier | Contenu |
|---------|---------|
| `layouts/` | Templates de base (base.html, admin_base.html) |
| `admin/` | Interface d'administration |
| `client/` | Espace client |
| `auth/` | Formulaires de connexion et inscription |
| `errors/` | Pages d'erreur (404, 500) |
| `landing.html` | Page d'accueil |
| `services.html` | Presentation des services |

### /services - Logique metier

| Fichier | Role |
|---------|------|
| `admin_service.py` | Creation automatique du compte admin au demarrage |
| `file_service.py` | Gestion des fichiers (upload, validation, suppression) |

### /security - Securite

| Fichier | Role |
|---------|------|
| `decorators.py` | Decorateurs de controle d'acces (admin_required, client_required) |
| `validators.py` | Validation des entrees utilisateur |
| `rate_limiter.py` | Limitation du nombre de requetes |
| `error_handlers.py` | Gestion centralisee des erreurs HTTP |

### /utils - Utilitaires

| Fichier | Role |
|---------|------|
| `forms.py` | Formulaires WTForms (login, register, demande, paiement) |
| `i18n.py` | Internationalisation, gestion des langues (FR/EN) |

### /lang - Traductions

| Fichier | Langue |
|---------|--------|
| `fr.json` | Francais |
| `en.json` | Anglais |

### /static - Ressources statiques

| Dossier | Contenu |
|---------|---------|
| `css/` | Feuilles de style personnalisees |
| `js/` | Scripts JavaScript |
| `uploads/` | Fichiers uploades par les utilisateurs |
| `uploads/branding/` | Logo, favicon, images OG |

---

## Schema relationnel de la base de donnees

```
                    +-------------+
                    |    User     |
                    +-------------+
                    | id          |
                    | email       |
                    | password_hash|
                    | is_admin    |
                    | admin_role  |
                    +------+------+
                           |
                           | 1:N
                           v
                 +-----------------+
                 | ServiceRequest  |
                 +-----------------+
                 | id              |
                 | user_id (FK)    |
                 | service_type    |
                 | status          |
                 | quote_amount    |
                 | progress_%      |
                 +--------+--------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
    +-----------+   +-----------+   +-------------+
    | Document  |   |  Payment  |   | ActivityLog |
    +-----------+   +-----------+   +-------------+
    | request_id|   | request_id|   | request_id  |
    | filename  |   | amount    |   | action_type |
    | doc_type  |   | status    |   | description |
    +-----------+   +-----------+   +-------------+
          |
          |               +-------------------+
          |               | DeadlineExtension |
          |               +-------------------+
          |               | request_id (FK)   |
          |               | new_deadline      |
          |               | status            |
          |               +-------------------+
          |
          |               +-------------------+
          |               | RevisionRequest   |
          |               +-------------------+
          |               | request_id (FK)   |
          |               | revision_details  |
          |               | status            |
          +-------------->+-------------------+

    +---------------+         +--------+
    | SiteSettings  |         |  Page  |
    +---------------+         +--------+
    | site_name     |         | title  |
    | logo          |         | slug   |
    | seo_*         |         | content|
    +---------------+         +--------+
```

---

## Systeme d'authentification

### Flask-Login

L'application utilise Flask-Login pour gerer les sessions utilisateur.

- `login_manager.user_loader` : charge l'utilisateur depuis la session
- `login_user()` : connecte un utilisateur
- `logout_user()` : deconnecte l'utilisateur
- `current_user` : acces a l'utilisateur connecte dans les templates et routes

### Hash des mots de passe

Les mots de passe sont hashes avec Werkzeug (pbkdf2:sha256) :
- `User.set_password(password)` : hash et stocke
- `User.check_password(password)` : verifie

### Decorateurs de controle d'acces

| Decorateur | Utilisation |
|------------|-------------|
| `@login_required` | Route accessible uniquement aux utilisateurs connectes |
| `@admin_required` | Route reservee aux administrateurs |
| `@super_admin_required` | Route reservee au super administrateur |
| `@client_required` | Route reservee aux clients (redirige les admins) |

---

## Systeme de roles

### Types de roles

| Role | Description |
|------|-------------|
| `None` | Utilisateur standard (client) |
| `admin` | Administrateur avec acces au panel admin |
| `super_admin` | Premier admin cree, peut gerer les autres admins |

### Permissions

| Action | Client | Admin | Super Admin |
|--------|--------|-------|-------------|
| Soumettre une demande | Oui | Non | Non |
| Voir ses demandes | Oui | Non | Non |
| Voir toutes les demandes | Non | Oui | Oui |
| Envoyer un devis | Non | Oui | Oui |
| Verifier un paiement | Non | Oui | Oui |
| Gerer les pages | Non | Oui | Oui |
| Creer un admin | Non | Non | Oui |
| Desactiver un admin | Non | Non | Oui |

---

## Cycle de vie des demandes

### Statuts possibles

| Code | Libelle | Description |
|------|---------|-------------|
| `submitted` | Soumise | Demande nouvellement creee |
| `under_review` | En examen | L'admin evalue la demande |
| `quote_sent` | Devis envoye | Un devis a ete propose au client |
| `quote_accepted` | Devis accepte | Le client a accepte le devis |
| `awaiting_deposit` | Attente acompte | En attente du paiement |
| `deposit_pending` | Acompte en verification | Paiement soumis, en cours de verification |
| `in_progress` | En cours | Travail en cours de realisation |
| `revision` | En revision | Modifications demandees par le client |
| `completed` | Terminee | Travail termine |
| `delivered` | Livree | Livrable transmis au client |
| `cancelled` | Annulee | Demande annulee |
| `rejected` | Refusee | Demande refusee par l'admin |

### Transitions

```
submitted --> under_review --> quote_sent --> quote_accepted
    |                                              |
    v                                              v
cancelled                                  awaiting_deposit
                                                   |
                                                   v
                                           deposit_pending
                                                   |
                                                   v
                                            in_progress
                                                   |
                                        +----------+----------+
                                        |                     |
                                        v                     v
                                    revision              completed
                                        |                     |
                                        +----------+----------+
                                                   |
                                                   v
                                               delivered
```

---

## Gestion des fichiers

### Types de documents

| Type | Description | Qui uploade |
|------|-------------|-------------|
| `client_upload` | Documents de reference | Client |
| `admin_upload` | Documents ajoutes par l'admin | Admin |
| `deliverable` | Travail final | Admin |
| `revision` | Version revisee | Admin |

### Extensions autorisees

- Documents : pdf, doc, docx, txt, rtf, odt
- Images : png, jpg, jpeg, gif

### Nommage des fichiers

Les fichiers sont renommes avec un prefixe UUID unique pour eviter les conflits :
`a1b2c3d4_document_original.pdf`

---

## Internationalisation (i18n)

### Langues supportees

- Francais (fr) - langue principale
- Anglais (en)

### Fonctionnement

1. Les traductions sont stockees dans `/lang/fr.json` et `/lang/en.json`
2. La fonction `t('cle.imbriquee')` recupere la traduction
3. La langue est determinee par : session > parametre URL > navigateur > defaut

### Utilisation dans les templates

```jinja
{{ t('auth.login.title') }}
{{ 'cle'|translate }}
```

---

## Logging

### Configuration

Le systeme de logging utilise des handlers rotatifs :
- Console : niveau DEBUG en developpement
- Fichier : `logs/thedraftclinic.log` (10 MB, 10 backups)
- Erreurs : `logs/errors.log` (10 MB, 10 backups)

### Format

```
2024-01-15 10:30:45 - INFO - routes.client - Nouvelle demande creee: 42
```

---

## Variables d'environnement requises

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `DATABASE_URL` | URL de connexion PostgreSQL | Oui |
| `SESSION_SECRET` | Cle secrete pour les sessions | Oui |
| `ADMIN_EMAIL` | Email du compte admin par defaut | Pour creation auto |
| `ADMIN_PASSWORD` | Mot de passe du compte admin | Pour creation auto |

---

## Configuration de production

### Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

### Pool de connexions

Le pool SQLAlchemy est configure pour la stabilite :
- `pool_recycle`: 300 secondes (recyclage des connexions)
- `pool_pre_ping`: True (verification avant utilisation)

---

## Securite

### Protection CSRF

Flask-WTF ajoute automatiquement des tokens CSRF aux formulaires.

### Proxy Fix

Le middleware `ProxyFix` est configure pour fonctionner derriere un reverse proxy (Nginx, Replit) et generer les bonnes URLs HTTPS.

### Taille des uploads

Limite a 50 MB par fichier (`MAX_CONTENT_LENGTH`).

### Cache control

Les en-tetes HTTP desactivent le cache pour eviter les problemes de mise a jour :
```
Cache-Control: no-cache, no-store, must-revalidate
```

---

*TheDraftClinic - Documentation technique v1.0*
