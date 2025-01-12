#!/usr/bin/python3
"""User Model Module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
import re

class User(BaseModel, Base):
    """Representation of a User."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialize user"""
        super().__init__(*args, **kwargs)
        if 'email' in kwargs:
            if not self._validate_email(kwargs['email']):
                raise ValueError("Invalid email format")

    def _validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_attribute(self, attr_name):
        """Validate a specific attribute."""
        if attr_name == 'email':
            if not self.email or '@' not in self.email:
                raise ValueError("Invalid email format.")
        elif attr_name == 'password':
            if not self.password or len(self.password) < 6:
                raise ValueError("Password must be at least 6 characters.")
        elif attr_name == 'first_name':
            if self.first_name and not isinstance(self.first_name, str):
                raise ValueError("First name must be a string.")
        elif attr_name == 'last_name':
            if self.last_name and not isinstance(self.last_name, str):
                raise ValueError("Last name must be a string.")

    places = relationship("Place", backref="user", cascade="all, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")

    def __setattr__(self, name, value):
        """Hash password when setting"""
        if name == "password" and isinstance(value, str):
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)