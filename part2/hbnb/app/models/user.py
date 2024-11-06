"""User model module for the HBnB application."""
from datetime import datetime
from app.models.base_model import BaseModel
import uuid


class User(BaseModel):
    """User Model"""
    def __init__(self, *args, **kwargs):
        """Initialize user"""
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        self.validate()

    def validate(self):
        """Validate user data"""
        if not self.first_name or not self.first_name.strip():
            raise ValueError("first_name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("last_name cannot be empty")
        if not self.email or not self.email.strip():
            raise ValueError("email cannot be empty")
        if '@' not in self.email:
            raise ValueError("Invalid email format")