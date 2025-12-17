# Securite de TheDraftClinic

Documentation des mecanismes de securite de la plateforme.

---

## Vue d'ensemble

La securite est une priorite de TheDraftClinic. L'application implemente plusieurs couches de protection pour garantir la confidentialite des donnees et la securite des utilisateurs.

---

## Authentification

### Gestion des mots de passe

Les mots de passe sont hashes avec Werkzeug (algorithme pbkdf2:sha256) :
- Hash unidirectionnel (impossible de retrouver le mot de passe)
- Salt unique pour chaque utilisateur
- Verification securisee

```python
user.set_password("mot_de_passe")  # Hash et stocke
user.check_password("mot_de_passe")  # Verifie
```

### Sessions

Les sessions utilisateur sont gerees par Flask-Login :
- Stockage cote serveur
- Token de session securise
- Option "Se souvenir de moi"
- Expiration configurable

### Cle secrete

La cle de session (SECRET_KEY) doit etre :
- Stockee dans les variables d'environnement (SESSION_SECRET)
- Unique et aleatoire
- Jamais commitee dans le code

---

## Autorisation

### Controle d'acces

L'application utilise des decorateurs pour proteger les routes :

| Decorateur | Protection |
|------------|------------|
| `@login_required` | Connexion obligatoire |
| `@admin_required` | Administrateurs uniquement |
| `@super_admin_required` | Super admin uniquement |
| `@client_required` | Clients uniquement (exclut admins) |

### Verification de propriete

Pour les ressources utilisateur, la verification inclut :
- Authentification de l'utilisateur
- Verification que la ressource lui appartient

```python
ServiceRequest.query.filter_by(
    id=request_id,
    user_id=current_user.id
).first_or_404()
```

---

## Protection CSRF

### Fonctionnement

Flask-WTF protege contre les attaques Cross-Site Request Forgery :
- Token unique genere par formulaire
- Validation automatique a la soumission
- Rejet des requetes sans token valide

### Implementation

Tous les formulaires incluent le token CSRF :
```html
<form method="POST">
    {{ form.csrf_token }}
    ...
</form>
```

Pour les requetes AJAX, le token est inclus dans les en-tetes.

---

## Validation des entrees

### Formulaires WTForms

Les formulaires utilisent WTForms pour la validation :
- Types de champs stricts
- Validateurs integres (email, longueur, requis)
- Messages d'erreur personnalises

### Fichiers uploades

La validation des fichiers inclut :
- Verification de l'extension (liste blanche)
- Limite de taille (50 MB max)
- Renommage securise avec UUID

Extensions autorisees :
- Documents : pdf, doc, docx, txt, rtf, odt
- Images : png, jpg, jpeg, gif

```python
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'png', 'jpg', 'jpeg', 'gif'}
```

### Noms de fichiers

Les noms de fichiers sont securises avec :
- `secure_filename()` de Werkzeug
- Prefixe UUID unique
- Suppression des caracteres speciaux

---

## Protection des donnees

### Base de donnees

- Connexion via URL securisee (DATABASE_URL)
- Pool de connexions avec verification (pool_pre_ping)
- Pas de requetes SQL brutes (ORM uniquement)

### Mots de passe

- Jamais stockes en clair
- Jamais logges
- Hash irreversible

### Sessions

- Cle secrete obligatoire en production
- Donnees sensibles non exposees cote client

---

## Headers HTTP

### Cache-Control

Les en-tetes desactivent le cache pour eviter les fuites de donnees :
```
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
```

### Proxy Fix

Le middleware ProxyFix gere les en-tetes de proxy :
- X-Proto : protocole (HTTP/HTTPS)
- X-Host : nom d'hote original

Permet de generer les bonnes URLs meme derriere un reverse proxy.

---

## Logging

### Journalisation

Toutes les actions importantes sont loggees :
- Connexions (reussies et echouees)
- Tentatives d'acces non autorises
- Erreurs et exceptions
- Actions administratives

### Fichiers de log

| Fichier | Contenu |
|---------|---------|
| `logs/thedraftclinic.log` | Log general |
| `logs/errors.log` | Erreurs uniquement |

### Rotation

Les fichiers sont automatiquement rotatifs :
- Taille max : 10 MB
- Conservation : 10 fichiers

---

## Gestion des erreurs

### Pages d'erreur personnalisees

Les erreurs HTTP affichent des pages personnalisees :
- 404 : Page non trouvee
- 403 : Acces interdit
- 500 : Erreur serveur

### Masquage des details

En production, les messages d'erreur ne revelent pas :
- Chemins de fichiers
- Requetes SQL
- Stack traces detaillees

---

## Roles et permissions

### Hierarchie

| Role | Niveau | Acces |
|------|--------|-------|
| Visiteur | 0 | Pages publiques |
| Client | 1 | Espace client, ses demandes |
| Admin | 2 | Panel admin, toutes demandes |
| Super Admin | 3 | Gestion des admins |

### Separation

- Les admins ne peuvent pas acceder a l'espace client
- Les clients sont rediriges s'ils tentent d'acceder au panel admin
- Chaque route verifie les permissions appropriees

---

## Compte administrateur

### Creation automatique

Le compte admin par defaut est cree au demarrage si :
- ADMIN_EMAIL est configure
- ADMIN_PASSWORD est configure
- Aucun admin avec cet email n'existe

### Premier admin

Le premier compte admin cree recoit le role `super_admin` et peut :
- Creer d'autres administrateurs
- Modifier les roles admin
- Desactiver des comptes admin

---

## Recommandations de securite

### En production

1. Definir SESSION_SECRET avec une valeur aleatoire forte
2. Utiliser HTTPS obligatoire
3. Configurer un reverse proxy (Nginx)
4. Limiter les acces reseau a la base de donnees
5. Mettre a jour regulierement les dependances

### Mots de passe

1. Exiger des mots de passe forts (8+ caracteres)
2. Changer le mot de passe admin par defaut
3. Ne jamais reutiliser les mots de passe

### Fichiers

1. Stocker les uploads en dehors de la racine web si possible
2. Verifier les types MIME reels (pas seulement l'extension)
3. Scanner les fichiers pour les virus (recommande)

---

## Variables d'environnement sensibles

| Variable | Description | Securite |
|----------|-------------|----------|
| SESSION_SECRET | Cle de session | Obligatoire, aleatoire |
| DATABASE_URL | URL PostgreSQL | Proteger les credentials |
| ADMIN_EMAIL | Email admin | Utiliser un email securise |
| ADMIN_PASSWORD | Mot de passe admin | Fort, changer apres creation |

Ne jamais commiter ces valeurs dans le code source.

---

## Incidents de securite

### En cas de compromission

1. Desactiver les comptes compromis
2. Regenerer SESSION_SECRET (deconnecte tous les utilisateurs)
3. Changer les mots de passe admin
4. Analyser les logs
5. Corriger la vulnerabilite
6. Notifier les utilisateurs si necessaire

### Contact

Signaler les vulnerabilites de securite a l'equipe de developpement.

---

*TheDraftClinic - Documentation securite v1.0*
