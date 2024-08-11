from pydantic import EmailStr
from sqlalchemy import UUID
from sqlalchemy.orm import scoped_session

from ..model.user_account import UserAccount

class UserCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        from dependancies import auth_manager
        self._auth_manager = auth_manager
        self._db_session = db_session

    def create_user(self, username: str, email: EmailStr, password: str) -> UserAccount:
        user = self.get_user_by_email(email)
        if user:
            return user
        
        hashed_password = self._auth_manager.hash_password(password)
        new_user = UserAccount(username=username, email=email, hashed_password=hashed_password)
        self._db_session.add(new_user)
        self._db_session.commit()
        return new_user

    def get_user_by_id(self, user_id: UUID) -> UserAccount:
        return self._db_session.query(UserAccount).filter(UserAccount.id == user_id).first()
    
    def get_user_by_email(self, email: EmailStr) -> UserAccount:
        return self._db_session.query(UserAccount).filter(UserAccount.email == email).first()

    def update_user_email(self, user_id: UUID, new_email: EmailStr) -> UserAccount:
        user = self.get_user_by_id(user_id)
        if user:
            user.email = new_email
            self._db_session.commit()
        return user

    def delete_user(self, user_id: UUID) -> UserAccount:
        user = self.get_user_by_id(user_id)
        if user:
            self._db_session.delete(user)
            self._db_session.commit()
        return user