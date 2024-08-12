from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .base_model import BaseModel, UUID
from .user_account import TABLE_NAME as USER_TABLE_NAME
from .game import TABLE_NAME as GAME_TABLE_NAME

class GameUser(BaseModel):
    __tablename__ = 'game_users'
    
    user_id = Column(UUID(), ForeignKey(f'{USER_TABLE_NAME}.id'), primary_key = True)
    game_id = Column(UUID(), ForeignKey(f'{GAME_TABLE_NAME}.id'), primary_key = True)
    
    # Additional fields
    joined_at = Column(DateTime, default = datetime.now(timezone.utc))