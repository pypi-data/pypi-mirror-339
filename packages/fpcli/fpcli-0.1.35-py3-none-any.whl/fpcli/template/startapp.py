def get_init_content():
    return """
from core.config import settings
from core.security.models.base_model import BaseModel
from core.security.schemas.base_schema import APIResponseSchema
from core.dependencies import get_db

__all__ = ["get_db", "settings", "BaseModel","APIResponseSchema"]
"""
