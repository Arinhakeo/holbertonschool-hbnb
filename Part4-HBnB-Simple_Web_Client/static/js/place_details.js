// palce_details.js

function afficherDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    
    const detailsHTML = `
        <div class="modal">
            <div class="modal-content">
                <span class="close-button" onclick="fermerDetails()">&times;</span>
                <h2>${place.name}</h2>
                <div class="details-content">
                    <p class="price">Prix par nuit: €${place.price}</p>
                    <div class="amenities">
                        <p><strong>Hôte:</strong> ${place.host}</p>
                        
                        <div class="amenities-icons">
                            ${place.amenities.map(amenity => {
                                let iconName = '';
                                switch(amenity.toLowerCase()) {
                                    case 'wifi':
                                        iconName = 'icon_wifi.png';
                                        break;
                                    case 'tv':
                                    case 'smart tv':
                                        iconName = 'icon_tv.png';
                                        break;
                                    case 'pets':
                                    case 'animaux acceptés':
                                        iconName = 'icon_pets.png';
                                        break;
                                    default:
                                        return `<div class="amenity-item">${amenity}</div>`;
                                }
                                return `
                                    <div class="amenity-item">
                                        <img src="../static/images/${iconName}" alt="${amenity}">
                                        <span>${amenity}</span>
                                    </div>`;
                            }).join('')}
                        </div>

                        <div class="facilities">
                            <div class="facility">
                                <img src="../static/images/icon_bath.png" alt="Bathrooms">
                                <span>${place.bathrooms || 1} Salle${place.bathrooms > 1 ? 's' : ''} de bain</span>
                            </div>
                            <div class="facility">
                                <img src="../static/images/icon_bed.png" alt="Bedrooms">
                                <span>${place.rooms || 1} Chambre${place.rooms > 1 ? 's' : ''}</span>
                            </div>
                            <div class="facility">
                                <img src="../static/images/icon_group.png" alt="Guests">
                                <span>Max ${place.max_guests || 2} personne${place.max_guests > 1 ? 's' : ''}</span>
                            </div>
                        </div>

                        <div class="description">
                            <h3>Description</h3>
                            <p>${place.description}</p>
                        </div>
                        <div class="reviews">
                            <h3>Avis:</h3>
                            ${place.reviews.map(review => `
                                <div class="review">
                                    <p>${review.author} - Note : ${review.rating}/5</p>
                                    <p>${review.comment}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    detailsContainer.innerHTML = detailsHTML;
    detailsContainer.style.display = 'block';
}

function fermerDetails() {
    const detailsContainer = document.getElementById('place-details');
    detailsContainer.style.display = 'none';
}

window.onclick = function(event) {
    const detailsContainer = document.getElementById('place-details');
    if (event.target === detailsContainer) {
        detailsContainer.style.display = 'none';
    }
};