from typing import Optional
from pydantic import EmailStr
from sqlalchemy import UUID
from sqlalchemy.orm import scoped_session

from ..model.game_user import GameUser
from ..model.game import Game, GameStatus

class GameUserCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        from dependancies import auth_manager
        self._auth_manager = auth_manager
        self._db_session = db_session

    def create_game_user(self, user_id: UUID, game_id: UUID, game_password: Optional[str] = None) -> Optional[GameUser]:
        if self._is_user_in_game(user_id, game_id):
            return GameUser
        
        game = self._db_session.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise Exception("Game not found")
        if game.hashed_password is not None:
            if game_password is None:
                raise Exception("Game requires a password")
            
            if not self._auth_manager.verify_password(game_password, game.hashed_password):
                raise Exception("Invalid password")
        
        if game.status != GameStatus.NEW:
            raise Exception("Game is not accepting new players")
        
        new_game_user = GameUser(user_id = user_id, game_id = game_id)
        self._db_session.add(new_game_user)
        self._db_session.commit()
        return new_game_user
    
    def get_games_by_user_id(self, user_id: UUID) -> list[GameUser]:
        return self._db_session.query(GameUser).filter(GameUser.user_id == user_id).all()

    def _is_user_in_game(self, user_id: UUID, game_id: UUID) -> bool:
        return self._db_session.query(GameUser).filter(GameUser.user_id == user_id, GameUser.game_id == game_id).first() is not None