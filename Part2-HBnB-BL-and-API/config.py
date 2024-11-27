import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SECRET_KEY = 'dev'
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
