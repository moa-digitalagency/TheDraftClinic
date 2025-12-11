# Guide du panel administrateur

> TheDraftClinic - Documentation admin

---

## Introduction

Ce guide détaille l'utilisation du panel administrateur de TheDraftClinic. L'interface a été redesignée avec une navigation latérale intuitive pour une meilleure ergonomie.

---

## Navigation

### Sidebar (barre latérale)

La sidebar gauche offre un accès rapide à toutes les sections :

| Section | Description |
|---------|-------------|
| Tableau de bord | Vue d'ensemble avec statistiques |
| Demandes | Liste et gestion des demandes clients |
| Utilisateurs | Gestion des comptes utilisateurs |
| Administrateurs | Gestion des admins (super admin uniquement) |
| Pages | CGU, CGV, pages personnalisées |
| Statistiques | Métriques de performance |
| Paramètres | Configuration du site |

---

## Tableau de bord

Le tableau de bord affiche :

### Cartes de statistiques
- Total demandes - Nombre total de demandes reçues
- En attente - Demandes en attente de traitement
- En cours - Demandes en cours de traitement
- Paiements - Paiements en attente de vérification
- Utilisateurs - Nombre total d'utilisateurs inscrits

### Sections
- Demandes récentes - Les 6 dernières demandes avec progression
- Paiements à vérifier - Paiements en attente d'approbation
- Activité récente - Historique des 10 dernières actions

---

## Gestion des demandes

### Liste des demandes

La page affiche toutes les demandes avec :
- ID - Numéro unique de la demande
- Titre - Titre du projet
- Client - Nom et email du client
- Statut - État actuel de la demande
- Progression - Barre de progression visuelle
- Date - Date de création

### Filtres
Utilisez le filtre par statut pour afficher :
- Tous les statuts
- Soumises
- En examen
- Devis envoyés
- En cours
- Terminées
- Livrées

### Actions sur une demande

#### Envoyer un devis
1. Ouvrir la demande
2. Remplir le montant total
3. Indiquer l'acompte requis
4. Ajouter un message (optionnel)
5. Cliquer sur "Envoyer le devis"

#### Mettre à jour le statut
1. Sélectionner le nouveau statut
2. Ajuster la progression (%)
3. Ajouter des notes admin
4. Cliquer sur "Mettre à jour"

#### Uploader un livrable
1. Sélectionner le fichier
2. Ajouter un commentaire de livraison
3. Cliquer sur "Uploader le livrable"

#### Vérifier un paiement
1. Consulter le justificatif
2. Cliquer sur "Approuver" ou "Rejeter"

---

## Gestion des utilisateurs

### Liste des utilisateurs
- Nom et email
- Établissement
- Niveau académique
- Nombre de demandes
- Date d'inscription

### Profil utilisateur
Vue détaillée avec :
- Informations personnelles
- Historique des demandes

---

## Gestion des administrateurs (super admin)

Accessible uniquement au super administrateur (premier compte créé).

### Ajouter un admin
1. Aller dans "Administrateurs"
2. Cliquer sur "Nouvel administrateur"
3. Remplir email, nom, prénom, mot de passe
4. Valider

### Modifier un admin
- Changer le rôle (admin/super_admin)
- Activer/désactiver le compte
- Réinitialiser le mot de passe

### Désactiver un admin
- Le compte reste en base mais ne peut plus se connecter
- Les actions passées restent tracées

---

## Gestion des pages

### Types de pages
- CGU - Conditions générales d'utilisation
- CGV - Conditions générales de vente
- Politique de confidentialité
- Mentions légales
- FAQ
- Pages personnalisées

### Créer une page
1. Cliquer sur "Nouvelle page"
2. Remplir le titre
3. Sélectionner le type de page
4. Choisir le format (HTML ou Markdown)
5. Écrire le contenu
6. Configurer les métadonnées SEO
7. Définir les options d'affichage
8. Publier la page

---

## Paramètres

### Paramètres généraux
- Nom du site
- Description
- Fuseau horaire
- Pays
- Langue par défaut
- Devise

### Branding
- Logo du site
- Favicon

### SEO et OpenGraph
- Titre SEO
- Description SEO
- Mots-clés
- Image OG
- Twitter Card

### Informations légales
- Raison sociale
- Adresse
- Email / Téléphone
- SIRET, RCS, TVA
- Hébergeur
- DPO

### Paramètres avancés
- Google Analytics
- Google Tag Manager
- Facebook Pixel
- Scripts personnalisés
- Mode maintenance

---

## Historique des activités

Le système enregistre automatiquement :
- Commentaires - Messages ajoutés aux demandes
- Livraisons - Fichiers uploadés
- Changements de statut - Modifications d'état
- Paiements - Vérifications de paiement
- Téléchargements - Documents téléchargés

Chaque activité inclut :
- Titre de l'action
- Description
- Auteur
- Date et heure
- Lien vers la demande

---

## Interface

### Design
- Thème sombre moderne
- Responsive (mobile-friendly)
- Navigation intuitive
- Chargement rapide

### Codes couleurs des statuts
- Jaune - En attente
- Bleu - En cours
- Vert - Complète/livrée
- Rouge - Rejetée/annulée

---

## Conseils

1. Consultez le tableau de bord régulièrement pour voir les nouvelles demandes
2. Vérifiez les paiements rapidement pour éviter les retards
3. Utilisez les commentaires pour communiquer avec les clients
4. Mettez à jour la progression pour que les clients suivent l'avancement
5. Consultez l'historique pour retracer les actions

---

<div align="center">

**TheDraftClinic - Panel administrateur**

*Interface redesignée pour une meilleure productivité*

</div>
