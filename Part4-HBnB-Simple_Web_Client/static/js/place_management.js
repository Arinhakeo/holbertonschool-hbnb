// ==== CONSTANTES ET VARIABLES GLOBALES ====
const API_BASE_URL = 'http://localhost:5000/api';
let editingPlaceId = null; // Pour suivre si on est en mode édition

// ==== GESTION DE LA MODAL ====
function showAddPlaceForm() {
    document.getElementById('place-modal').style.display = 'block';
    document.getElementById('place-form').reset(); // Réinitialise le formulaire
    editingPlaceId = null; // Mode création
}

function hideModal() {
    document.getElementById('place-modal').style.display = 'none';
}

// Ferme la modal si on clique en dehors
window.onclick = function(event) {
    const modal = document.getElementById('place-modal');
    if (event.target === modal) {
        hideModal();
    }
}

// ==== GESTION DU FORMULAIRE ====
document.addEventListener('DOMContentLoaded', () => {
    // Charge les places au démarrage
    loadPlaces();

    // Gestion de la soumission du formulaire
    document.getElementById('place-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        // Récupère les données du formulaire
        const formData = {
            name: document.getElementById('name').value,
            price_by_night: parseInt(document.getElementById('price').value),
            description: document.getElementById('description').value,
            max_guest: parseInt(document.getElementById('max_guests').value),
            number_rooms: parseInt(document.getElementById('rooms').value),
            number_bathrooms: parseInt(document.getElementById('bathrooms').value),
            amenities: Array.from(document.querySelectorAll('.amenities-grid input:checked'))
                           .map(checkbox => checkbox.value)
        };

        try {
            if (editingPlaceId) {
                // Mode édition
                await updatePlace(editingPlaceId, formData);
            } else {
                // Mode création
                await createPlace(formData);
            }
            hideModal();
            loadPlaces(); // Recharge la liste
        } catch (error) {
            console.error('Erreur:', error);
            alert('Une erreur est survenue');
        }
    });
});

// ==== FONCTIONS CRUD ====
// Création d'une place
async function createPlace(placeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(placeData)
        });

        if (!response.ok) throw new Error('Erreur création');
        alert('Place créée avec succès !');
    } catch (error) {
        console.error('Erreur création:', error);
        throw error;
    }
}

// Mise à jour d'une place
async function updatePlace(id, placeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(placeData)
        });

        if (!response.ok) throw new Error('Erreur mise à jour');
        alert('Place mise à jour avec succès !');
    } catch (error) {
        console.error('Erreur mise à jour:', error);
        throw error;
    }
}

// Suppression d'une place
async function deletePlace(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette place ?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/places/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Erreur suppression');
        loadPlaces(); // Recharge la liste
        alert('Place supprimée avec succès !');
    } catch (error) {
        console.error('Erreur suppression:', error);
        alert('Erreur lors de la suppression');
    }
}

// ==== AFFICHAGE DES PLACES ====
async function loadPlaces() {
    const container = document.getElementById('places-container');
    try {
        const response = await fetch(`${API_BASE_URL}/places`);
        if (!response.ok) throw new Error('Erreur chargement');

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Erreur chargement:', error);
        container.innerHTML = '<p class="error">Erreur de chargement des places</p>';
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-container');
    container.innerHTML = ''; // Vide le conteneur

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <div class="price">${place.price_by_night}€ / nuit</div>
            <div class="info">
                <p><i class="fas fa-users"></i> ${place.max_guest} personnes</p>
                <p><i class="fas fa-bed"></i> ${place.number_rooms} chambres</p>
                <p><i class="fas fa-bath"></i> ${place.number_bathrooms} sdb</p>
            </div>
            <p class="description">${place.description}</p>
            <div class="amenities">
                ${place.amenities.map(amenity => `
                    <span class="amenity"><i class="fas fa-check"></i> ${amenity}</span>
                `).join('')}
            </div>
            <div class="actions">
                <button onclick="editPlace(${place.id})" class="edit-btn">
                    <i class="fas fa-edit"></i> Modifier
                </button>
                <button onclick="deletePlace(${place.id})" class="delete-btn">
                    <i class="fas fa-trash"></i> Supprimer
                </button>
            </div>
        `;
        container.appendChild(placeCard);
    });
}

// ==== ÉDITION D'UNE PLACE ====
function editPlace(id) {
    // Cherche la place dans les données
    const place = places.find(p => p.id === id);
    if (!place) return;

    // Remplit le formulaire
    document.getElementById('name').value = place.name;
    document.getElementById('price').value = place.price_by_night;
    document.getElementById('description').value = place.description;
    document.getElementById('max_guests').value = place.max_guest;
    document.getElementById('rooms').value = place.number_rooms;
    document.getElementById('bathrooms').value = place.number_bathrooms;

    // Coche les équipements
    document.querySelectorAll('.amenities-grid input').forEach(checkbox => {
        checkbox.checked = place.amenities.includes(checkbox.value);
    });

    // Passe en mode édition
    editingPlaceId = id;
    showAddPlaceForm();
}