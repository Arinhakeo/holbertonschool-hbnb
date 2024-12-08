class PlacesManager {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
        this.placesList = document.getElementById('places-list');
        this.priceFilter = document.getElementById('price-filter');
        this.loginLink = document.getElementById('login-link');
        this.places = [];

        this.initEventListeners();
        this.checkAuthentication();
    }

    initEventListeners() {
        this.priceFilter.addEventListener('change', this.filterPlaces.bind(this));
    }

    async checkAuthentication() {
        const token = this.getToken();

        if (token) {
            this.loginLink.style.display = 'none';
            await this.fetchPlaces(token);
        } else {
            this.loginLink.style.display = 'block';
        }
    }

    getToken() {
        return this.getCookie('token');
    }

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

    renderPlaces(places) {
        this.placesList.innerHTML = ''; // Vider la liste actuelle

        places.forEach(place => {
            const placeCard = this.createPlaceCard(place);
            this.placesList.appendChild(placeCard);
        });
    }

    createPlaceCard(place) {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.dataset.price = place.price;

        card.innerHTML = `
            <img src="${place.image || 'placeholder.jpg'}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p>Prix : ${place.price}€ / nuit</p>
            <p>${place.description.substring(0, 100)}...</p>
            <button class="details-button" data-id="${place.id}">
                Voir Détails
            </button>
        `;

        const detailsButton = card.querySelector('.details-button');
        detailsButton.addEventListener('click', () => this.navigateToDetails(place.id));

        return card;
    }

    filterPlaces() {
        const selectedPrice = this.priceFilter.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const price = parseFloat(card.dataset.price);

            if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    navigateToDetails(placeId) {
        window.location.href = `place.html?id=${placeId}`;
    }

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

    logout() {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = 'login.html';
    }
}

// Initialisation du gestionnaire de places
document.addEventListener('DOMContentLoaded', () => {
    const placesManager = new PlacesManager('<https://votre-api.com>');
});
