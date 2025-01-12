// ==== VARIABLES GLOBALES ====
const API_BASE_URL = 'http://localhost:5000/api';  // URL de base de l'API
let currentPlaceId = null;                         // ID de la place en cours de modification

// ==== GESTIONNAIRES D'ÉVÉNEMENTS PRINCIPAUX ====
document.addEventListener('DOMContentLoaded', () => {
    // Initialisation des écouteurs d'événements
    initializeEventListeners();
    // Chargement initial des places
    loadPlaces();
});

// ==== GESTION DES ÉVÉNEMENTS ====
function initializeEventListeners() {
    // Gestion du formulaire de place
    const placeForm = document.getElementById('place-form');
    if (placeForm) {
        placeForm.addEventListener('submit', handlePlaceSubmit);
    }

    // Gestion des uploads de photos
    document.querySelectorAll('.photo-upload-box').forEach(box => {
        box.addEventListener('click', () => {
            box.querySelector('input[type="file"]').click();
        });

        const fileInput = box.querySelector('input[type="file"]');
        fileInput.addEventListener('change', (e) => handleFileSelect(e, box));
    });
}

// ==== GESTION DES PHOTOS ====
function handleFileSelect(event, uploadBox) {
    const file = event.target.files[0];
    if (!file) return;

    // Vérification du type de fichier
    if (!file.type.startsWith('image/')) {
        alert('Veuillez sélectionner une image');
        return;
    }

    // Création de la prévisualisation
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = uploadBox.querySelector('.preview');
        preview.style.backgroundImage = `url(${e.target.result})`;
        preview.style.display = 'block';
        uploadBox.querySelector('.upload-placeholder').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// ==== GESTION DU FORMULAIRE ====
async function handlePlaceSubmit(event) {
    event.preventDefault();

    // Récupération des données du formulaire
    const formData = new FormData();
    const placeData = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        price_by_night: parseInt(document.getElementById('price').value),
        max_guest: parseInt(document.getElementById('max_guests').value),
        number_rooms: parseInt(document.getElementById('bedrooms').value),
        number_bathrooms: parseInt(document.getElementById('bathrooms').value),
        amenities: getSelectedAmenities()
    };

    // Ajout des photos
    const photoInputs = document.querySelectorAll('.photo-input');
    photoInputs.forEach((input, index) => {
        if (input.files[0]) {
            formData.append(`photo${index + 1}`, input.files[0]);
        }
    });

    // Ajout des données de la place
    formData.append('placeData', JSON.stringify(placeData));

    try {
        await savePlace(formData);
        hideForm();
        loadPlaces();
    } catch (error) {
        alert('Erreur lors de la sauvegarde');
        console.error('Erreur:', error);
    }
}

// ==== SAUVEGARDE DES DONNÉES ====
async function savePlace(formData) {
    const url = currentPlaceId 
        ? `${API_BASE_URL}/places/${currentPlaceId}`
        : `${API_BASE_URL}/places`;

    const method = currentPlaceId ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            body: formData
        });

        if (!response.ok) throw new Error('Erreur réseau');

        const result = await response.json();
        return result;
    } catch (error) {
        throw error;
    }
}

// ==== CHARGEMENT DES PLACES ====
async function loadPlaces() {
    try {
        const response = await fetch(`${API_BASE_URL}/places`);
        if (!response.ok) throw new Error('Erreur chargement');

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Erreur chargement:', error);
        document.getElementById('places-list').innerHTML = 
            '<p class="error">Erreur de chargement des places</p>';
    }
}

// ==== AFFICHAGE DES PLACES ====
function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';

    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        container.appendChild(placeCard);
    });
}

// ==== CRÉATION D'UNE CARTE DE PLACE ====
// Fonction pour afficher les détails d'une place
function afficherDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    
    const detailsHTML = `
        <div class="modal-content">
            <span class="close-button" onclick="fermerDetails()">&times;</span>
            <h2>${place.name}</h2>
            <div class="details-content">
                <div class="price-section">
                    <h3>€${place.price_by_night} / nuit</h3>
                </div>
                <div class="info-section">
                    <div class="info-item">
                        <i class="fas fa-users"></i>
                        <span>${place.max_guest} personne${place.max_guest > 1 ? 's' : ''}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-bed"></i>
                        <span>${place.number_rooms} chambre${place.number_rooms > 1 ? 's' : ''}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-bath"></i>
                        <span>${place.number_bathrooms} salle${place.number_bathrooms > 1 ? 's' : ''} de bain</span>
                    </div>
                </div>
                <div class="description">
                    <h3>Description</h3>
                    <p>${place.description}</p>
                </div>
                ${place.amenities ? `
                    <div class="amenities">
                        <h3>Équipements</h3>
                        <ul>
                            ${place.amenities.map(amenity => `
                                <li><i class="fas fa-check"></i> ${amenity}</li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    detailsContainer.innerHTML = detailsHTML;
    detailsContainer.style.display = 'block';
}

// Fonction pour fermer la modal de détails
function fermerDetails() {
    document.getElementById('place-details').style.display = 'none';
}

// Fermer la modal en cliquant en dehors
window.onclick = function(event) {
    const modal = document.getElementById('place-details');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};
// Après les fonctions existantes, ajoutez :

// Gestion des uploads de photos
document.querySelectorAll('.photo-input').forEach(input => {
    input.addEventListener('change', function(e) {
        handlePhotoUpload(this);
    });
});

function handlePhotoUpload(input) {
    const file = input.files[0];
    if (!file) return;

    // Vérifier que c'est bien une image
    if (!file.type.startsWith('image/')) {
        alert('Veuillez sélectionner une image');
        input.value = '';
        return;
    }

    // Créer une prévisualisation
    const preview = input.closest('.photo-upload-box').querySelector('.preview');
    const placeholder = input.closest('.photo-upload-box').querySelector('.upload-placeholder');
    
    const reader = new FileReader();
    reader.onload = function(e) {
        preview.style.backgroundImage = `url(${e.target.result})`;
        preview.style.display = 'block';
        placeholder.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Modifier la fonction existante qui gère la soumission du formulaire
async function handlePlaceSubmit(event) {
    event.preventDefault();

    const formData = new FormData();
    
    // Ajouter les photos
    document.querySelectorAll('.photo-input').forEach((input, index) => {
        if (input.files[0]) {
            formData.append(`photo${index + 1}`, input.files[0]);
        }
    });

    // Ajouter les autres données
    const placeData = {
        // vos données existantes...
    };

    formData.append('data', JSON.stringify(placeData));

    try {
        // votre code d'envoi existant...
    } catch (error) {
        console.error('Erreur:', error);
    }
}