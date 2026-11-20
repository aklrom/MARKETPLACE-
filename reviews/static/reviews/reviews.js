// static/reviews/reviews.js
document.addEventListener('DOMContentLoaded', function() {
    // Cible le champ textarea du formulaire d'avis
    const textarea = document.querySelector('textarea[name="text"]');
    
    if (textarea) {
        // Fonction pour ajuster la hauteur
        const autoResize = () => {
            textarea.style.height = 'auto'; // Réinitialise pour recalculer
            textarea.style.height = (textarea.scrollHeight) + 'px'; // Ajuste à la hauteur du contenu
        };

        // Écouteur d'événement à chaque frappe
        textarea.addEventListener('input', autoResize);
        
        // Déclenche une fois au chargement (utile pour la vue "Modifier" si le texte est déjà long)
        autoResize();
    }
});