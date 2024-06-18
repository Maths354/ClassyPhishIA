
// Script pour afficher l'animation de la page si bouton 'loading' est clické
document.getElementById('loading').addEventListener('click', function() {
    var overlay = document.getElementById('overlay');
    overlay.style.display = 'flex';
    setTimeout(function() {
        overlay.style.display = 'none';
    }, 5000);
});
