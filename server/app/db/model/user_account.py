from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import uuid

from .base_model import BaseModel, UUID

TABLE_NAME = 'user_accounts'

class UserAccount(BaseModel):
    __tablename__ = TABLE_NAME
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)