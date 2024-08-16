from pydantic import BaseModel
from typing import Optional

class GameCreate(BaseModel):
    name: str
    max_players: int
    public: bool
    password: Optional[str] = None

    class Config:
        from_attributes = True
