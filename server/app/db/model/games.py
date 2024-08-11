from sqlalchemy import Column, Enum, Integer, String
from enum import Enum as PyEnum
import uuid

from .base_model import BaseModel, UUID

class GameStatus(PyEnum):
    CREATED = 'CREATED'
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'

class Game(BaseModel):
    __tablename__ = 'games'
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False, unique=False)
    join_code = Column(String, nullable=False, unique=True)
    game_status = Column(Enum(GameStatus), nullable=False, default=GameStatus.CREATED)