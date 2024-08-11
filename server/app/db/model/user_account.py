from sqlalchemy import Column, Integer, String
from .base_model import BaseModel

class UserAccount(BaseModel):
    __tablename__ = 'user_accounts'
    
    id = BaseModel.id

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    
    created_at = BaseModel.created_at
    updated_at = BaseModel.updated_at