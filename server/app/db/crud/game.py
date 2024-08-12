from sqlalchemy.orm import scoped_session
from typing import Optional
from uuid import UUID

from ..model.game import Game, GameStatus

class GameCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        from dependancies import auth_manager
        self._auth_manager = auth_manager
        self._db_session = db_session

    def create_game(self, name: str, owner_id: UUID, public: bool, password: Optional[str] = None) -> Game:
        # Generate a join code, unique to the game
        join_code = self._auth_manager.generate_join_code()
        # Verify the join code is unique
        while self._db_session.query(Game).filter(Game.join_code == join_code).first():
            join_code = self._auth_manager.generate_join_code()
        
        hashed_password = None
        if password is not None:
            hashed_password = self._auth_manager.hash_password(password)
        new_game = Game(name = name, owner_id = owner_id, join_code = join_code, status = GameStatus.NEW, public = public, hashed_password = hashed_password)
        self._db_session.add(new_game)
        self._db_session.commit()
        return new_game
    
    def get_game_by_join_code(self, join_code: str) -> Game:
        return self._db_session.query(Game).filter(Game.join_code == join_code).first()
    
    def get_game_by_id(self, game_id: UUID) -> Game:
        return self._db_session.query(Game).filter(Game.id == game_id).first()
    
    def get_public_games(self) -> list[Game]:
        return self._db_session.query(Game).filter(Game.public == True).all()
    
    def get_games_by_owner_id(self, owner_id: UUID) -> list[Game]:
        return self._db_session.query(Game).filter(Game.owner_id == owner_id).all()