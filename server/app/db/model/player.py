from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .base_model import BaseModel, UUID
from .user_account import TABLE_NAME as USER_TABLE_NAME
from .game import TABLE_NAME as GAME_TABLE_NAME

class Player(BaseModel):
    __tablename__ = 'players'
    
    user_id = Column(UUID(), ForeignKey(f'{USER_TABLE_NAME}.id'), primary_key = True)
    game_id = Column(UUID(), ForeignKey(f'{GAME_TABLE_NAME}.id'), primary_key = True)
    
    # Additional fields
    alive = Column(Boolean, default = True)
    action_points = Column(Integer, default = 3)
    health_points = Column(Integer, default = 3)
    cannon_range = Column(Integer, default = 1)
    
    position_x = Column(Integer, default = 0)
    position_y = Column(Integer, default = 0)