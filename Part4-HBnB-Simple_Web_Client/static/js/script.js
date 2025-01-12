// script.js

document.addEventListener("DOMContentLoaded", () => {
    const priceFilter = document.getElementById('price-filter');
    const placesContainer = document.getElementById('places-container');
    const detailsContainer = document.getElementById('place-details');
    // Définition des données statiques pour les lieux
    const places = [
        {
            id: 1,
            name: "Beautiful Beach House",
            host: "John Doe",
            price: 150,
            description: "A beautiful beach house with amazing ocean views and direct beach access.",
            amenities: ["WiFi", "Pool", "Air Conditioning", "Beach Access"],
            reviews: [
                { author: "Jane Smith", comment: "Great place to stay! The view is breathtaking.", rating: 4 },
                { author: "Robert Brown", comment: "Amazing location and very comfortable. Will come back!", rating: 5 },
            ],
        },
        {
            id: 2,
            name: "Cozy Mountain Cabin",
            host: "Alice Johnson",
            price: 100,
            description: "A warm and inviting cabin nestled in the woods with stunning mountain views.",
            amenities: ["Fireplace", "Hiking Trails", "Mountain View", "Hot Tub"],
            reviews: [
                { author: "Emma Wilson", comment: "So cozy and quiet! Perfect for a weekend getaway.", rating: 5 },
            ],
        },
        {
            id: 3,
            name: "Modern City Apartment",
            host: "Chris Lee",
            price: 200,
            description: "A sleek and stylish city apartment with modern amenities in the heart of downtown.",
            amenities: ["Smart TV", "High-Speed WiFi", "Gym Access", "Rooftop Terrace"],
            reviews: [
                { author: "Liam Martinez", comment: "Perfect for business travel. Great location and amenities.", rating: 4 },
            ],
        },
        {
            id: 4,
            name: "Rustic Lakehouse Retreat",
            host: "Laura White",
            price: 180,
            description: "A charming lakehouse with a beautiful view of the sunset and private lake access.",
            amenities: ["Boat Dock", "Fireplace", "Private Garden", "Kayaks"],
            reviews: [
                { author: "Michael Scott", comment: "Absolutely stunning and relaxing! The lake view is incredible.", rating: 5 },
                { author: "Pam Beesly", comment: "Perfect place for a family getaway. Kids loved it!", rating: 4 },
            ],
        },
        {
            id: 5,
            name: "Luxury Penthouse Suite",
            host: "David Beckham",
            price: 350,
            description: "A luxurious penthouse with panoramic city views and world-class amenities.",
            amenities: ["Private Pool", "Rooftop Bar", "24/7 Butler Service", "Helipad"],
            reviews: [
                { author: "Victoria Beckham", comment: "Luxury at its finest! The service is impeccable.", rating: 5 },
                { author: "Elton John", comment: "Absolutely worth it! The views are unparalleled.", rating: 5 },
            ],
        },
    ];

    // Ajoutez ici le reste de votre code pour utiliser ces données
    function displayPlaces(places) {
        const placesContainer = document.getElementById('places-container');
        placesContainer.innerHTML = '';
    
        places.forEach(place => {
            const placeElement = document.createElement('article');
            placeElement.className = 'place';
            placeElement.innerHTML = `
                <h2>${place.name}</h2>
                <div class="price_by_night">€${place.price_by_night}</div>
                <div class="information">
                    <div class="max_guest">
                        <i class="fas fa-users"></i>
                        ${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}
                    </div>
                    <div class="number_rooms">
                        <i class="fas fa-bed"></i>
                        ${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}
                    </div>
                    <div class="number_bathrooms">
                        <i class="fas fa-bath"></i>
                        ${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}
                    </div>
                </div>
                <div class="description">${place.description}</div>
                <div class="actions">
                    <button onclick='afficherDetails(${JSON.stringify(place)})' class="view-details">
                        Voir les détails
                    </button>
                </div>
            `;
            placesContainer.appendChild(placeElement);
        });
    }
    // Fonction pour afficher les places
function afficherPlaces() {
    const conteneurPlaces = document.getElementById('places-container');
    conteneurPlaces.innerHTML = '';

    places.forEach(place => {
        const elementPlace = document.createElement('div');
        elementPlace.className = 'place';
        elementPlace.innerHTML = `
            <h3>${place.name}</h3>
            <p>Hôte : ${place.host}</p>
            <p>Prix : ${place.price}€ par nuit</p>
            <p>${place.description}</p>
            <button onclick='afficherDetails(${JSON.stringify(place)})'>Voir les détails</button>
        `;
        conteneurPlaces.appendChild(elementPlace);
    });
}

// Fonction pour afficher les places filtrées
function afficherPlacesFiltrees(placesFiltrees) {
    placesContainer.innerHTML = '';
    placesFiltrees.forEach(place => {
        const elementPlace = document.createElement('div');
        elementPlace.className = 'place';
        elementPlace.innerHTML = `
            <h3>${place.name}</h3>
            <p>Hôte : ${place.host}</p>
            <p>Prix : ${place.price}€ par nuit</p>
            <p>${place.description}</p>
            <button onclick='afficherDetails(${JSON.stringify(place)})'>Voir les détails</button>
        `;
        placesContainer.appendChild(elementPlace);
    });
}
    // Appel de la fonction pour afficher les places au chargement de la page
    afficherPlaces();

    // Gestion du filtre de prix
    priceFilter.addEventListener('change', () => {
        const selectedValue = priceFilter.value;
        let placesFiltrees;
        
        if (selectedValue === 'all') {
            placesFiltrees = places; // Affiche toutes les places
        } else {
            const prixMax = parseInt(selectedValue);
            placesFiltrees = places.filter(place => place.price <= prixMax);
        }
        
        afficherPlacesFiltrees(placesFiltrees);
    });

    // Fonction pour afficher les places filtrées
    function afficherPlacesFiltrees(placesFiltrees) {
        placesContainer.innerHTML = '';
        placesFiltrees.forEach(place => {
            const elementPlace = document.createElement('div');
            elementPlace.className = 'place';
            elementPlace.innerHTML = `
                <h3>${place.name}</h3>
                <p>Hôte : ${place.host}</p>
                <p>Prix : ${place.price}€ par nuit</p>
                <p>${place.description}</p>
                <button onclick='afficherDetails(${JSON.stringify(place)})'>Voir les détails</button>
            `;
            placesContainer.appendChild(elementPlace);
        });
    }
});
// Fonction pour afficher les détails d'une place
function afficherDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    
    const detailsHTML = `
        <div class="modal-content">
            <span class="close-button" onclick="fermerDetails()">&times;</span>
            <h2>${place.name}</h2>
            <div class="details-content">
                <div class="host-info">
                    <p><strong>Hôte:</strong> ${place.host}</p>
                </div>
                <div class="price">
                    <p><strong>Prix:</strong> ${place.price}€ par nuit</p>
                </div>
                <div class="description">
                    <h3>Description</h3>
                    <p>${place.description}</p>
                </div>
                <div class="amenities">
                    <h3>Équipements</h3>
                    <ul>
                        ${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
                    </ul>
                </div>
                <div class="reviews">
                    <h3>Avis</h3>
                    ${place.reviews.map(review => `
                        <div class="review">
                            <p><strong>${review.author}</strong> - Note: ${review.rating}/5</p>
                            <p>${review.comment}</p>
                        </div>
                    `).join('')}
                </div>
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

// Fermeture au clic en dehors de la modal
window.onclick = function(event) {
    const modal = document.getElementById('place-details');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}