from pydantic import BaseModel

class GameCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True
