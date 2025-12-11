# guide du panel administrateur

> TheDraftClinic - documentation admin

---

## introduction

Ce guide detaille l'utilisation du panel administrateur de TheDraftClinic. L'interface a ete redesignee avec une navigation laterale intuitive pour une meilleure ergonomie.

---

## navigation

### sidebar (barre laterale)

La sidebar gauche offre un acces rapide a toutes les sections:

| section | description |
|---------|-------------|
| tableau de bord | vue d'ensemble avec statistiques |
| demandes | liste et gestion des demandes clients |
| utilisateurs | gestion des comptes utilisateurs |
| administrateurs | gestion des admins (super admin uniquement) |
| pages | cgu, cgv, pages personnalisees |
| statistiques | metriques de performance |
| parametres | configuration du site |

---

## tableau de bord

Le tableau de bord affiche:

### cartes de statistiques
- total demandes - nombre total de demandes recues
- en attente - demandes en attente de traitement
- en cours - demandes en cours de traitement
- paiements - paiements en attente de verification
- utilisateurs - nombre total d'utilisateurs inscrits

### sections
- demandes recentes - les 6 dernieres demandes avec progression
- paiements a verifier - paiements en attente d'approbation
- activite recente - historique des 10 dernieres actions

---

## gestion des demandes

### liste des demandes

La page affiche toutes les demandes avec:
- id - numero unique de la demande
- titre - titre du projet
- client - nom et email du client
- statut - etat actuel de la demande
- progression - barre de progression visuelle
- date - date de creation

### filtres
utilisez le filtre par statut pour afficher:
- tous les statuts
- soumises
- en examen
- devis envoyes
- en cours
- terminees
- livrees

### actions sur une demande

#### envoyer un devis
1. ouvrir la demande
2. remplir le montant total
3. indiquer l'acompte requis
4. ajouter un message (optionnel)
5. cliquer sur "envoyer le devis"

#### mettre a jour le statut
1. selectionner le nouveau statut
2. ajuster la progression (%)
3. ajouter des notes admin
4. cliquer sur "mettre a jour"

#### uploader un livrable
1. selectionner le fichier
2. ajouter un commentaire de livraison
3. cliquer sur "uploader le livrable"

#### verifier un paiement
1. consulter le justificatif
2. cliquer sur "approuver" ou "rejeter"

---

## gestion des utilisateurs

### liste des utilisateurs
- nom et email
- etablissement
- niveau academique
- nombre de demandes
- date d'inscription

### profil utilisateur
vue detaillee avec:
- informations personnelles
- historique des demandes

---

## gestion des administrateurs (super admin)

Accessible uniquement au super administrateur (premier compte cree).

### ajouter un admin
1. aller dans "administrateurs"
2. cliquer sur "nouvel administrateur"
3. remplir email, nom, prenom, mot de passe
4. valider

### modifier un admin
- changer le role (admin/super_admin)
- activer/desactiver le compte
- reinitialiser le mot de passe

### desactiver un admin
- le compte reste en base mais ne peut plus se connecter
- les actions passees restent tracees

---

## gestion des pages

### types de pages
- cgu - conditions generales d'utilisation
- cgv - conditions generales de vente
- politique de confidentialite
- mentions legales
- faq
- pages personnalisees

### creer une page
1. cliquer sur "nouvelle page"
2. remplir le titre
3. selectionner le type de page
4. choisir le format (html ou markdown)
5. ecrire le contenu
6. configurer les metadonnees seo
7. definir les options d'affichage
8. publier la page

---

## parametres

### parametres generaux
- nom du site
- description
- fuseau horaire
- pays
- langue par defaut
- devise

### branding
- logo du site
- favicon

### seo et opengraph
- titre seo
- description seo
- mots-cles
- image og
- twitter card

### informations legales
- raison sociale
- adresse
- email / telephone
- siret, rcs, tva
- hebergeur
- dpo

### parametres avances
- google analytics
- google tag manager
- facebook pixel
- scripts personnalises
- mode maintenance

---

## historique des activites

Le systeme enregistre automatiquement:
- commentaires - messages ajoutes aux demandes
- livraisons - fichiers uploades
- changements de statut - modifications d'etat
- paiements - verifications de paiement
- telechargements - documents telecharges

Chaque activite inclut:
- titre de l'action
- description
- auteur
- date et heure
- lien vers la demande

---

## interface

### design
- theme sombre moderne
- responsive (mobile-friendly)
- navigation intuitive
- chargement rapide

### codes couleurs des statuts
- jaune - en attente
- bleu - en cours
- vert - complete/livree
- rouge - rejetee/annulee

---

## conseils

1. consultez le tableau de bord regulierement pour voir les nouvelles demandes
2. verifiez les paiements rapidement pour eviter les retards
3. utilisez les commentaires pour communiquer avec les clients
4. mettez a jour la progression pour que les clients suivent l'avancement
5. consultez l'historique pour retracer les actions

---

<div align="center">

**TheDraftClinic - panel administrateur**

*interface redesignee pour une meilleure productivite*

</div>
