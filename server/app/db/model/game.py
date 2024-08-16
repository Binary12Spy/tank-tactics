from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from enum import Enum as PyEnum
import uuid

from .base_model import BaseModel, UUID

from .user_account import TABLE_NAME as USER_TABLE_NAME

TABLE_NAME = 'games'

class GameStatus(PyEnum):
    NEW = 'NEW'
    RUNNING = 'RUNNING'
    COMPLETE = 'COMPLETE'

class Game(BaseModel):
    __tablename__ = TABLE_NAME
    
    id = Column(UUID(), primary_key = True, default = uuid.uuid4, unique = True, nullable = False)
    owner_id = Column(UUID(), ForeignKey(f'{USER_TABLE_NAME}.id'), nullable = False)
    name = Column(String, nullable = False, unique = False)
    join_code = Column(String, nullable = False, unique = True)
    status = Column(Enum(GameStatus), nullable = False, default = GameStatus.NEW)
    max_players = Column(Integer, nullable = False, default = 12)
    public = Column(Boolean, nullable = False, default = True)
    hashed_password = Column(String, nullable = True)