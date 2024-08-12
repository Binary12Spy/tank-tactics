from pydantic import EmailStr
from sqlalchemy import UUID
from sqlalchemy.orm import scoped_session

from ..model.game_user import GameUser

class GameUserCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    def create_game_user(self, user_id: UUID, game_id: UUID) -> GameUser:
        if self._is_user_in_game(user_id, game_id):
            return GameUser
        
        new_game_user = GameUser(user_id = user_id, game_id = game_id)
        self._db_session.add(new_game_user)
        self._db_session.commit()
        return new_game_user
    
    def get_games_by_user_id(self, user_id: UUID) -> list[GameUser]:
        return self._db_session.query(GameUser).filter(GameUser.user_id == user_id).all()

    def _is_user_in_game(self, user_id: UUID, game_id: UUID) -> bool:
        return self._db_session.query(GameUser).filter(GameUser.user_id == user_id, GameUser.game_id == game_id).first() is not None