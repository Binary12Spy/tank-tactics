from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from db.model.game import GameStatus

class GameDetails(BaseModel):
    id: Optional[UUID]
    name: str
    status: GameStatus
    join_code: str
    public: bool

    class Config:
        from_attributes = True
