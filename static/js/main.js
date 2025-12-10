/**
 * ================================================================================
 * TheDraftClinic - JavaScript Principal
 * ================================================================================
 * By MOA Digital Agency LLC
 * Developed by: Aisance KALONJI
 * Contact: moa@myoneart.com
 * Website: www.myoneart.com
 * ================================================================================
 * 
 * Ce fichier contient le JavaScript côté client pour l'application:
 * - Gestion automatique des alertes flash (auto-dismiss)
 * - Validation des formulaires côté client
 * - Utilitaires d'interface utilisateur
 * 
 * Note: Ce fichier est chargé sur toutes les pages via le template de base.
 * ================================================================================
 */


// ==============================================================================
// ÉVÉNEMENT DE CHARGEMENT DU DOM
// ==============================================================================

/**
 * Attendre que le DOM soit entièrement chargé avant d'exécuter le code.
 * Cela garantit que tous les éléments HTML sont accessibles.
 */
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialisation des différents modules
    initAlertDismissal();
    initFormValidation();
    initMobileMenu();
    
});


// ==============================================================================
// GESTION DES ALERTES FLASH
// ==============================================================================

/**
 * Initialise le système de fermeture automatique des alertes.
 * 
 * Les alertes avec la classe 'alert-dismissible' disparaissent 
 * automatiquement après 5 secondes avec une animation de fondu.
 */
function initAlertDismissal() {
    // Sélection de toutes les alertes qui peuvent être fermées
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    // Pour chaque alerte trouvée
    alerts.forEach(function(alert) {
        // Programmer la disparition après 5 secondes
        setTimeout(function() {
            // Animation de fondu
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            
            // Suppression de l'élément après l'animation
            setTimeout(function() {
                alert.remove();
            }, 300);  // 300ms pour laisser l'animation se terminer
            
        }, 5000);  // 5 secondes avant de commencer la disparition
    });
}


// ==============================================================================
// VALIDATION DES FORMULAIRES
// ==============================================================================

/**
 * Initialise la validation des formulaires côté client.
 * 
 * Ajoute une validation en temps réel pour:
 * - Les champs email (format valide)
 * - Les champs mot de passe (longueur minimale)
 * - Les champs obligatoires
 */
function initFormValidation() {
    // Sélection de tous les formulaires avec validation
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(function(form) {
        // Écouteur sur la soumission du formulaire
        form.addEventListener('submit', function(event) {
            // Vérification de la validité du formulaire
            if (!validateForm(form)) {
                // Empêcher l'envoi si invalide
                event.preventDefault();
            }
        });
    });
}


/**
 * Valide un formulaire et affiche les erreurs.
 * 
 * @param {HTMLFormElement} form - Le formulaire à valider
 * @returns {boolean} - True si le formulaire est valide, false sinon
 */
function validateForm(form) {
    // Variable pour suivre la validité globale
    let isValid = true;
    
    // Réinitialisation des erreurs précédentes
    clearFormErrors(form);
    
    // Validation des champs email
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(function(field) {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Format d\'email invalide');
            isValid = false;
        }
    });
    
    // Validation des champs mot de passe (minimum 6 caractères)
    const passwordFields = form.querySelectorAll('input[type="password"]');
    passwordFields.forEach(function(field) {
        if (field.value && field.value.length < 6) {
            showFieldError(field, 'Le mot de passe doit contenir au moins 6 caractères');
            isValid = false;
        }
    });
    
    // Validation des champs obligatoires
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            showFieldError(field, 'Ce champ est obligatoire');
            isValid = false;
        }
    });
    
    return isValid;
}


/**
 * Vérifie si une adresse email a un format valide.
 * 
 * @param {string} email - L'adresse email à valider
 * @returns {boolean} - True si le format est valide
 */
function isValidEmail(email) {
    // Expression régulière pour la validation d'email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


/**
 * Affiche un message d'erreur sous un champ de formulaire.
 * 
 * @param {HTMLElement} field - Le champ avec l'erreur
 * @param {string} message - Le message d'erreur à afficher
 */
function showFieldError(field, message) {
    // Ajout d'une classe d'erreur au champ
    field.classList.add('border-red-500');
    
    // Création de l'élément d'erreur
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-red-500 text-sm mt-1 error-message';
    errorDiv.textContent = message;
    
    // Insertion après le champ
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}


/**
 * Efface tous les messages d'erreur d'un formulaire.
 * 
 * @param {HTMLFormElement} form - Le formulaire à nettoyer
 */
function clearFormErrors(form) {
    // Suppression des messages d'erreur
    const errorMessages = form.querySelectorAll('.error-message');
    errorMessages.forEach(function(msg) {
        msg.remove();
    });
    
    // Suppression des classes d'erreur sur les champs
    const errorFields = form.querySelectorAll('.border-red-500');
    errorFields.forEach(function(field) {
        field.classList.remove('border-red-500');
    });
}


// ==============================================================================
// MENU MOBILE
// ==============================================================================

/**
 * Initialise le comportement du menu mobile (hamburger).
 * 
 * Gère l'ouverture et la fermeture du menu sur les petits écrans.
 */
function initMobileMenu() {
    // Bouton du menu mobile
    const menuButton = document.querySelector('[data-mobile-menu-button]');
    // Contenu du menu mobile
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    
    // Si les éléments existent
    if (menuButton && mobileMenu) {
        // Écouteur sur le clic du bouton
        menuButton.addEventListener('click', function() {
            // Toggle de la visibilité du menu
            mobileMenu.classList.toggle('hidden');
        });
    }
}


// ==============================================================================
// UTILITAIRES
// ==============================================================================

/**
 * Formate un nombre en devise (EUR).
 * 
 * @param {number} amount - Le montant à formater
 * @returns {string} - Le montant formaté (ex: "1 234,56 €")
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}


/**
 * Formate une date en format français.
 * 
 * @param {string|Date} date - La date à formater
 * @returns {string} - La date formatée (ex: "10 décembre 2025")
 */
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(date).toLocaleDateString('fr-FR', options);
}


/**
 * Affiche une notification toast (message temporaire).
 * 
 * @param {string} message - Le message à afficher
 * @param {string} type - Le type de notification ('success', 'error', 'info')
 */
function showToast(message, type = 'info') {
    // Création de l'élément toast
    const toast = document.createElement('div');
    
    // Classes de base
    let bgClass = 'bg-blue-500';
    if (type === 'success') bgClass = 'bg-green-500';
    if (type === 'error') bgClass = 'bg-red-500';
    
    toast.className = `fixed top-4 right-4 ${bgClass} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300`;
    toast.textContent = message;
    
    // Ajout au DOM
    document.body.appendChild(toast);
    
    // Animation d'entrée
    setTimeout(function() {
        toast.classList.remove('translate-x-full');
    }, 10);
    
    // Animation de sortie et suppression
    setTimeout(function() {
        toast.classList.add('translate-x-full');
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 3000);
}
