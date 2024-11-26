#!/usr/bin/python3
"""Database Storage Module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    """Database Storage Class"""
    __engine = None
    __session = None

    def rollback(self):
        """Rollback session"""
        self.__session.rollback()

    def get_by_name(self, cls, name):
        """
    Retrieve an object by its name.
    Args:
        cls (class): The class of the object to query.
        name (str): The name of the object to retrieve.
    Returns:
        The first object that matches the given name, or None if not found.
    """
        if cls and name:
            query = self.__session.query(cls).filter(cls.name == name).first()
            return query
        return None

    def __init__(self):
        """Initialize SQLAlchemy engine."""
        user = getenv('HBNB_MYSQL_USER') or 'hbnb_dev'
        pwd = getenv('HBNB_MYSQL_PWD') or 'hbnb_dev_pwd'
        host = getenv('HBNB_MYSQL_HOST') or 'localhost'
        db = getenv('HBNB_MYSQL_DB') or 'hbnb_dev_db'
        env = getenv('HBNB_ENV') or 'test'

        if not all([user, pwd, host, db]):
            print(f"USER: {user}, PWD: {pwd}, HOST: {host}, DB: {db}, ENV: {env}")
            raise Exception("Missing MySQL environment variables.")
        
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        

    def all(self, cls=None):
        """Query objects"""
        classes = {
            'User': User, 'State': State, 'City': City,
            'Amenity': Amenity, 'Place': Place, 'Review': Review
        }
        objects = {}
        
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls:
                query = self.__session.query(cls)
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add object to session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close session"""
        if self.__session:
            self.__session.close()

    def get(self, cls, id):
        """Get object by class and id"""
        if cls and id:
            if isinstance(cls, str):
                cls = eval(cls)
            obj = self.__session.get(cls, id)
            return obj
        return None

    def count(self, cls=None):
        """Count objects"""
        return len(self.all(cls))
    
    def delete_all(self):
        """Delete all objects in the correct order"""
        try:
            # Supprimer d'abord les objets enfants
            self.__session.query(Review).delete()
            self.__session.query(Place).delete()
            self.__session.query(City).delete()
            self.__session.query(State).delete()
            self.__session.query(User).delete()
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e