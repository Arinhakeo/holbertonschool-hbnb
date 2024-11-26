#!/usr/bin/python3
"""Tests for BaseModel class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.exceptions import ValidationError
from api.v1.app import app

class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test environment"""
        self.model = BaseModel()

    def test_init_no_args(self):
        """Test initialization without arguments"""
        self.assertTrue(hasattr(self.model, 'id'))
        self.assertTrue(hasattr(self.model, 'created_at'))
        self.assertTrue(hasattr(self.model, 'updated_at'))
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_init_with_dict(self):
        """Test initialization with dictionary"""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        model = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(model.id, "345")
        self.assertEqual(model.created_at, dt)
        self.assertEqual(model.updated_at, dt)

    def test_to_dict(self):
        """Test conversion to dictionary"""
        self.model.name = "Test"
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["name"], "Test")
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_str(self):
        """Test string representation"""
        string = str(self.model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.model.id, string)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)