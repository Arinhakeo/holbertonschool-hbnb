#!/usr/bin/python3
"""Module de stockage de base de données"""
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
    """Classe de stockage de base de données utilisant SQLAlchemy."""
    __engine = None  # Moteur SQLAlchemy
    __session = None  # Session SQLAlchemy

    def __init__(self):
        """Initialise le moteur SQLAlchemy et crée la session."""
        user = getenv('HBNB_MYSQL_USER', 'hbnb_dev')  # Utilisateur MySQL
        pwd = getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')  # Mot de passe MySQL
        host = getenv('HBNB_MYSQL_HOST', 'localhost')  # Hôte MySQL
        db = getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')  # Nom de la base de données
        env = getenv('HBNB_ENV', 'test')  # Environnement

        # Vérification des variables d'environnement
        if not all([user, pwd, host, db]):
            raise Exception("Variables d'environnement MySQL manquantes.")

        # Création du moteur SQLAlchemy
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        # Supprime toutes les tables si en environnement de test
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Interroge tous les objets ou les objets d'une classe spécifique."""
        classes = {
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }  # Dictionnaire des classes disponibles
        objects = {}

        # Si une classe est spécifiée
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)  # Obtient la classe à partir du nom
            if cls:
                query = self.__session.query(cls)  # Interroge tous les objets de la classe spécifiée
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        else:
            # Interroge tous les objets de toutes les classes
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Ajoute un nouvel objet à la session."""
        if obj:
            self.__session.add(obj)  # Ajoute l'objet à la session SQLAlchemy

    def save(self):
        """Valide la session en enregistrant les modifications."""
        self.__session.commit()  # Enregistre les modifications dans la base de données

    def delete(self, obj=None):
        """Supprime un objet de la session."""
        if obj:
            self.__session.delete(obj)  # Supprime l'objet de la session SQLAlchemy

    def reload(self):
        """Crée toutes les tables et initialise la session."""
        Base.metadata.create_all(self.__engine)  # Crée toutes les tables définies dans les modèles
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()  # Crée une nouvelle session SQLAlchemy

    def close(self):
        """Ferme la session SQLAlchemy."""
        if self.__session:
            self.__session.close()  # Ferme la session

    def get(self, cls, id):
        """Récupère un objet par sa classe et son id."""
        if cls and id:
            # Récupère la classe à partir de son nom si c'est une chaîne
            classes = {
                'User': User,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Place': Place,
                'Review': Review
            }
            cls = classes.get(cls) if isinstance(cls, str) else cls
            return self.__session.get(cls, id)  # Récupère l'objet par son id
        return None

    def count(self, cls=None):
        """Compte le nombre d'objets d'une classe spécifique ou tous les objets."""
        return len(self.all(cls))  # Utilise la méthode all() pour obtenir tous les objets et les compte

    def delete_all(self):
        """Supprime tous les objets dans l'ordre correct."""
        try:
            # Supprime d'abord les objets enfants
            self.__session.query(Review).delete()  # Supprime toutes les reviews
            self.__session.query(Place).delete()   # Supprime tous les lieux
            self.__session.query(City).delete()    # Supprime toutes les villes
            self.__session.query(State).delete()   # Supprime tous les états
            self.__session.query(User).delete()    # Supprime tous les utilisateurs
            self.__session.commit()  # Valide les suppressions
        except Exception as e:
            print(f"Erreur lors de la suppression de tous les objets: {e}")
            self.__session.rollback()  # Annule les changements en cas d'erreur
