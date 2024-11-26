"""Review model module"""
from datetime import datetime
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review Model"""
    def __init__(self, *args, **kwargs):
        """Initialize review"""
        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')
        self.rating = int(kwargs.get('rating', 1))
        self.user_id = kwargs.get('user_id', '')
        self.place_id = kwargs.get('place_id', '')
        self.validate()

    def validate(self):
        """Validate review data"""
        if not self.text or not self.text.strip():
            raise ValueError("text cannot be empty")
        if not isinstance(self.rating, int) or self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if not self.place_id:
            raise ValueError("place_id cannot be empty")