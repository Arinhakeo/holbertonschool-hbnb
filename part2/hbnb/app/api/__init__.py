"""API package initialization"""
from app.api.v1 import blueprint as api_v1_blueprint

__all__ = ['api_v1_blueprint']