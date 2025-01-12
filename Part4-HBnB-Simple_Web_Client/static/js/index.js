// ==== GESTIONNAIRE DES PLACES ====
// Classe principale qui gère toute la logique des locations
class PlacesManager {
    // Constructeur : initialise les propriétés de base
    constructor(apiUrl) {
        // URL de l'API pour les requêtes
        this.apiUrl = apiUrl;
        // Éléments du DOM nécessaires
        this.placesList = document.getElementById('places-list');           // Conteneur des places
        this.priceFilter = document.getElementById('price-filter');         // Filtre de prix
        this.loginLink = document.getElementById('login-link');             // Lien de connexion
        // Tableau qui stockera toutes les places
        this.places = [];

        // Initialisation des écouteurs d'événements et vérification de l'authentification
        this.initEventListeners();
        this.checkAuthentication();
    }

    // ==== INITIALISATION DES ÉVÉNEMENTS ====
    initEventListeners() {
        // Ajoute un écouteur sur le changement du filtre de prix
        this.priceFilter.addEventListener('change', () => this.filterPlaces());
    }

    // ==== GESTION DE L'AUTHENTIFICATION ====
    // Vérifie si l'utilisateur est connecté
    async checkAuthentication() {
        const token = this.getToken();

        if (token) {
            // Si token présent, cache le lien de connexion et charge les places
            this.loginLink.style.display = 'none';
            await this.fetchPlaces(token);
        } else {
            // Sinon affiche le lien de connexion
            this.loginLink.style.display = 'block';
        }
    }

    // Récupère le token d'authentification
    getToken() {
        return this.getCookie('token');
    }

    // Récupère un cookie spécifique par son nom
    getCookie(name) {
        const cookieArr = document.cookie.split(";");
        for (let cookie of cookieArr) {
            let [cookieName, cookieValue] = cookie.trim().split("=");
            if (cookieName === name) {
                return cookieValue;
            }
        }
        return null;
    }

    // ==== RÉCUPÉRATION DES PLACES ====
    // Charge les places depuis l'API
    async fetchPlaces(token) {
        try {
            const response = await fetch(`${this.apiUrl}/places`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                this.places = await response.json();
                this.renderPlaces(this.places);
            } else {
                this.handleFetchError(response);
            }
        } catch (error) {
            console.error('Erreur de récupération des places:', error);
        }
    }

    // ==== AFFICHAGE DES PLACES ====
    // Affiche toutes les places dans la liste
    renderPlaces(places) {
        this.placesList.innerHTML = ''; // Vide la liste actuelle
        places.forEach(place => {
            const placeCard = this.createPlaceCard(place);
            this.placesList.appendChild(placeCard);
        });
    }

    // Crée une carte pour une place individuelle
    createPlaceCard(place) {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.dataset.price = place.price;

        // Structure HTML de la carte
        card.innerHTML = `
            <img src="${place.image || 'placeholder.jpg'}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p>Prix : ${place.price}€ / nuit</p>
            <p>${place.description.substring(0, 100)}...</p>
            <button class="details-button" data-id="${place.id}">
                Voir Détails
            </button>
        `;

        // Ajoute l'événement pour voir les détails
        const detailsButton = card.querySelector('.details-button');
        detailsButton.addEventListener('click', () => this.navigateToDetails(place.id));

        return card;
    }

    // ==== FILTRAGE DES PLACES ====
    // Filtre les places selon le prix sélectionné
    filterPlaces() {
        const selectedPrice = this.priceFilter.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            // Affiche ou cache selon le filtre
            if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // ==== NAVIGATION ====
    // Redirige vers la page de détails d'une place
    navigateToDetails(placeId) {
        window.location.href = `place.html?id=${placeId}`;
    }

    // ==== GESTION DES ERREURS ====
    // Gère les différentes erreurs possibles
    handleFetchError(response) {
        switch(response.status) {
            case 401:
                alert('Session expirée. Reconnectez-vous.');
                this.logout();
                break;
            case 403:
                alert('Accès non autorisé');
                break;
            case 404:
                alert('Aucune place trouvée');
                break;
            default:
                alert('Erreur de chargement des places');
        }
    }

    // ==== DÉCONNEXION ====
    // Déconnecte l'utilisateur
    logout() {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'login.html';
    }
}

// ==== CODE PRINCIPAL ====
// Charge les places au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    loadPlaces();
});

// Fonction de chargement des places
async function loadPlaces() {
    try {
        const response = await fetch(`${CONFIG.API_URL}/places`);
        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        utils.handleError(error);
    }
}

// Fonction d'affichage des places
function displayPlaces(places) {
    const container = document.getElementById('places-container');
    container.innerHTML = places.map(place => `
        <div class="place">
            <h2>${place.name}</h2>
            <p>${place.description}</p>
            <div class="price">${utils.formatPrice(place.price_by_night)}</div>
        </div>
    `).join('');
}

// Pour utiliser cette classe :
// const placesManager = new PlacesManager('http://votre-api-url');