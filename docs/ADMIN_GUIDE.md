# Guide Administrateur TheDraftClinic

Documentation complete pour l'administration de la plateforme.

---

## Acces au panel administrateur

### Connexion

1. Rendez-vous sur `/auth/login`
2. Connectez-vous avec un compte administrateur
3. Vous etes automatiquement redirige vers le tableau de bord admin

### Types de comptes admin

| Role | Description |
|------|-------------|
| Super administrateur | Premier compte cree, tous les droits incluant la gestion des admins |
| Administrateur | Acces complet sauf gestion des autres admins |

---

## Tableau de bord

Le tableau de bord offre une vue d'ensemble :

### Cartes de statistiques

- Total demandes : Nombre total de demandes recues
- En attente : Demandes necessitant une action
- En cours : Demandes en traitement
- Paiements a verifier : Paiements en attente de validation
- Utilisateurs : Nombre de clients inscrits

### Sections

- Demandes recentes : Les 10 dernieres demandes
- Paiements en attente : Liste des paiements a verifier
- Activite recente : Dernieres actions sur la plateforme

---

## Gestion des demandes

### Liste des demandes

Accessible via le menu "Demandes".

Colonnes affichees :
- ID de la demande
- Titre du projet
- Client (nom et email)
- Type de service
- Statut actuel
- Progression
- Date de creation

### Filtrage

Utilisez le menu deroulant pour filtrer par statut :
- Toutes les demandes
- Soumises (nouvelles)
- En examen
- Devis envoyes
- En cours
- Terminees
- Livrees

### Detail d'une demande

Cliquez sur une demande pour voir :

#### Informations du projet
- Type de service demande
- Titre et description
- Nombre de mots/pages souhaite
- Date limite
- Niveau d'urgence
- Notes additionnelles

#### Informations du client
- Nom complet
- Email
- Telephone
- Etablissement
- Niveau academique

#### Documents
- Documents uploades par le client
- Documents ajoutes par l'admin
- Livrables

#### Paiements
- Historique des paiements
- Statut de chaque paiement
- Preuves de paiement

---

## Actions sur les demandes

### Envoyer un devis

1. Ouvrez la demande
2. Remplissez le formulaire de devis :
   - Montant total en euros
   - Montant de l'acompte (generalement 50%)
   - Message d'accompagnement
3. Cliquez sur "Envoyer le devis"

Le client recevra la notification et pourra accepter ou refuser.

### Mettre a jour le statut

1. Selectionnez le nouveau statut dans la liste
2. Ajustez le pourcentage de progression
3. Ajoutez des notes internes si necessaire
4. Cliquez sur "Mettre a jour"

Les changements de statut sont visibles par le client.

### Uploader un livrable

1. Selectionnez le fichier a uploader
2. Ajoutez un commentaire de livraison
3. Cliquez sur "Uploader le livrable"

Le client pourra telecharger le fichier.

### Ajouter un commentaire

Les commentaires permettent de communiquer avec le client :
1. Ecrivez votre message
2. Cliquez sur "Ajouter"

Le message apparait dans l'historique d'activite.

### Demander une extension de delai

Si plus de temps est necessaire :
1. Indiquez la nouvelle date limite
2. Expliquez la raison
3. Soumettez la demande

Le client devra approuver ou refuser.

---

## Verification des paiements

### Acces

Les paiements a verifier apparaissent :
- Sur le tableau de bord
- Dans la section "Paiements" du menu

### Processus de verification

1. Ouvrez le paiement en question
2. Consultez :
   - Montant declare
   - Methode de paiement
   - Reference de transaction
   - Preuve de paiement (image/document)
3. Verifiez sur votre compte bancaire
4. Choisissez :
   - "Approuver" si le paiement est confirme
   - "Rejeter" avec une explication si non valide

### Apres approbation

- Le statut de la demande passe a "En cours"
- Le client est notifie
- Le travail peut commencer

### Apres rejet

- Le statut revient a "Attente acompte"
- Le client peut soumettre une nouvelle preuve

---

## Gestion des utilisateurs

### Liste des utilisateurs

Affiche tous les clients inscrits :
- Nom et email
- Etablissement
- Niveau academique
- Nombre de demandes
- Date d'inscription

### Detail d'un utilisateur

Voir le profil complet et l'historique des demandes du client.

---

## Gestion des administrateurs (super admin)

Accessible uniquement au super administrateur.

### Ajouter un administrateur

1. Allez dans "Administrateurs"
2. Cliquez sur "Nouvel administrateur"
3. Remplissez :
   - Email
   - Mot de passe
   - Prenom et nom
4. Validez

### Modifier un administrateur

- Changer le role (admin / super_admin)
- Activer ou desactiver le compte
- Reinitialiser le mot de passe

### Desactiver un compte admin

Le compte reste en base mais ne peut plus se connecter. Les actions passees restent tracees.

---

## Gestion des pages

### Types de pages

| Type | Description |
|------|-------------|
| CGU | Conditions generales d'utilisation |
| CGV | Conditions generales de vente |
| Politique de confidentialite | Protection des donnees |
| Mentions legales | Informations legales |
| FAQ | Questions frequentes |
| A propos | Presentation de l'entreprise |
| Page personnalisee | Contenu libre |

### Creer une page

1. Allez dans "Pages"
2. Cliquez sur "Nouvelle page"
3. Remplissez :
   - Titre
   - Slug (URL de la page)
   - Type de page
   - Format (HTML ou Markdown)
   - Contenu
4. Configurez les metadonnees SEO
5. Choisissez les options d'affichage :
   - Publier la page
   - Afficher dans le footer
   - Afficher dans la navigation
6. Enregistrez

### Modifier une page

1. Cliquez sur la page a modifier
2. Effectuez vos changements
3. Enregistrez

### Supprimer une page

Attention, cette action est irreversible.

---

## Parametres du site

### Parametres generaux

- Nom du site
- Description
- Fuseau horaire
- Pays
- Langue par defaut
- Devise

### Branding

- Logo du site (recommande : PNG transparent)
- Favicon (icone navigateur)

### SEO et OpenGraph

- Titre SEO (balise title)
- Description SEO (balise meta description)
- Mots-cles
- Image OpenGraph (partage reseaux sociaux)
- Twitter Card

### Informations legales

- Raison sociale
- Adresse du siege
- Email et telephone
- SIRET, RCS, numero TVA
- Code APE
- Capital social
- Nom et email du DPO
- Hebergeur

### Parametres avances

- Google Analytics ID
- Google Tag Manager ID
- Facebook Pixel ID
- Scripts personnalises (head/body)
- Mode maintenance

---

## Gestion des langues

### Langues disponibles

La plateforme supporte plusieurs langues (FR, EN).

### Modifier les traductions

1. Allez dans "Langues"
2. Selectionnez la langue a modifier
3. Editez le fichier JSON
4. Enregistrez

### Telecharger/Importer

- Telecharger le fichier JSON pour modification externe
- Importer un fichier JSON modifie

---

## Statistiques

La page de statistiques affiche :

### Metriques globales

- Nombre total de demandes
- Nombre d'utilisateurs
- Demandes terminees
- Taux de livraison dans les delais
- Temps moyen de livraison

### Repartition

- Demandes par statut
- Demandes par type de service

### Historique d'activite

Les 50 dernieres actions sur la plateforme.

---

## Historique des activites

Le systeme enregistre automatiquement :

| Action | Description |
|--------|-------------|
| Commentaire | Message ajoute |
| Livraison | Fichier uploade |
| Changement de statut | Modification du statut |
| Paiement verifie | Approbation de paiement |
| Telechargement | Document telecharge |
| Demande de revision | Revision demandee |
| Extension de delai | Demande d'extension |

Chaque entree inclut :
- Type d'action
- Titre et description
- Auteur
- Date et heure

---

## Codes couleur des statuts

| Couleur | Statuts |
|---------|---------|
| Jaune/Orange | Soumise, En attente |
| Bleu | En examen, En cours |
| Vert | Termine, Livre, Verifie |
| Rouge | Annule, Rejete |

---

## Bonnes pratiques

1. Verifiez le tableau de bord quotidiennement
2. Traitez les paiements en attente rapidement
3. Mettez a jour la progression regulierement
4. Utilisez les commentaires pour communiquer
5. Documentez les notes internes
6. Consultez l'historique en cas de litige

---

## Securite

### Acces au panel

- Connexion obligatoire
- Session securisee
- Protection CSRF sur tous les formulaires

### Bonnes pratiques

- Utilisez un mot de passe fort
- Ne partagez pas vos identifiants
- Deconnectez-vous sur les appareils partages
- Verifiez les paiements avec attention

---

*TheDraftClinic - Guide administrateur v1.0*
