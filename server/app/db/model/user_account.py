from sqlalchemy import Column, Integer, String
import uuid

from .base_model import BaseModel, UUID

class UserAccount(BaseModel):
    __tablename__ = 'user_accounts'
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)