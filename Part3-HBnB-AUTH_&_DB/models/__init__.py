"""Initialize models package"""
from dotenv import load_dotenv
import os
from models.base_model import Base
from models.engine.db_storage import DBStorage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

storage = DBStorage()
storage.reload()