from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserAccount(BaseModel):
    id: Optional[UUID]
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
