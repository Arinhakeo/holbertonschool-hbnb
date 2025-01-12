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
    function afficherPlaces() {
        const conteneurPlaces = document.getElementById('places-container');
        conteneurPlaces.innerHTML = ''; // Nettoie le contenu existant

        places.forEach(place => {
            const elementPlace = document.createElement('div');
            elementPlace.className = 'place';
            elementPlace.innerHTML = `
                <h3>${place.name}</h3>
                <p>Hôte : ${place.host}</p>
                <p>Prix : ${place.price}€ par nuit</p>
                <p>${place.description}</p>
                <button onclick="afficherDetails(${place.id})">Voir les détails</button>
            `;
            conteneurPlaces.appendChild(elementPlace);
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