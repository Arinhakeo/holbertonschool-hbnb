#!/usr/bin/python3
"""Amenity Model Module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import validates

class Amenity(BaseModel, Base):
    """Amenity Class"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty.")
        return value
    
    def to_dict(self):
        """Convert Amenity instance to dictionary"""
        obj_dict = super().to_dict()  # Appelle la méthode to_dict() de BaseModel
        return obj_dict