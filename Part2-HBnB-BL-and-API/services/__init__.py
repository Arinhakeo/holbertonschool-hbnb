class AmenityService:
    def __init__(self):
        self.amenities = []  # Liste pour stocker les amenities

    def create_amenity(self, data):
        # Assure-toi que l'ID est généré ou attribué correctement
        new_id = str(uuid.uuid4())  # Génère un nouvel ID
        amenity = Amenity(id=new_id, name=data.get('name'))
        self.amenities.append(amenity)  # Ajoute l'amenity à la liste
        return amenity

    def get_all_amenities(self):
        return [amenity.to_dict() for amenity in self.amenities]  # Convertit en dict
