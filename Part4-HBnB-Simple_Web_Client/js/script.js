/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/
  function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getCookie(name) {
    // Fonction pour obtenir la valeur d'un cookie par son nom
    // Votre code ici
}
function getPlaceIdFromURL() {
  // Extraire l'ID du lieu de window.location.search
  // Votre code ici
}
document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          // Obtenir le texte du commentaire à partir du formulaire
          // Effectuer une requête AJAX pour soumettre le commentaire
          // Gérer la réponse
      });
  }
});

async function submitReview(token, placeId, reviewText) {
  // Effectuer une requête POST pour soumettre les données du commentaire
  // Inclure le jeton dans l'en-tête d'autorisation
  // Envoyer placeId et reviewText dans le corps de la requête
  // Gérer la réponse
}

function handleResponse(response) {
  if (response.ok) {
      alert('Commentaire soumis avec succès !');
      // Effacer le formulaire
  } else {
      alert('Échec de la soumission du commentaire');
  }
}
