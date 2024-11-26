import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqldb://{}:{}@{}/{}'.format(
        os.getenv('HBNB_MYSQL_USER', 'hbnb_dev'),
        os.getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd'),
        os.getenv('HBNB_MYSQL_HOST', 'localhost'),
        os.getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')
    ))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False