from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class GameDetails(BaseModel):
    id: Optional[UUID]
    name: str
    join_code: str

    class Config:
        from_attributes = True
