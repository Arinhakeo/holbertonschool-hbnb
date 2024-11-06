"""Amenity model module"""
from datetime import datetime
from app.models.base_model import BaseModel
import uuid

class Amenity(BaseModel):
    """Amenity Model"""
    def __init__(self, *args, **kwargs):
        """Initialize amenity"""
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', '')
        self.validate()

        def validate(self):
            """Validate amenity data"""
        if not self.name or not self.name.strip():
            raise ValueError("name cannot be empty")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
