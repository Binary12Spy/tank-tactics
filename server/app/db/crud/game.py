from sqlalchemy.orm import scoped_session
from typing import Optional
from uuid import UUID

from config import settings
from ..model.game import Game, GameStatus

class GameCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        from dependancies import auth_manager
        self._auth_manager = auth_manager
        self._db_session = db_session

    def create_game(self, name: str, owner_id: UUID, max_players: int, public: bool, password: Optional[str] = None) -> Game:
        # Generate a join code, unique to the game
        join_code = self._auth_manager.generate_join_code()
        # Verify the join code is unique
        while self._db_session.query(Game).filter(Game.join_code == join_code).first():
            join_code = self._auth_manager.generate_join_code()
            
        max_players = min(max_players, settings.max_players_per_game)
        
        hashed_password = None
        if password is not None:
            hashed_password = self._auth_manager.hash_password(password)
        new_game = Game(name = name, owner_id = owner_id, join_code = join_code, status = GameStatus.NEW, max_players = max_players, public = public, hashed_password = hashed_password)
        self._db_session.add(new_game)
        self._db_session.commit()
        return new_game
    
    def get_game_by_join_code(self, join_code: str) -> Game:
        return self._db_session.query(Game).filter(Game.join_code == join_code).first()
    
    def get_game_by_id(self, game_id: UUID) -> Game:
        return self._db_session.query(Game).filter(Game.id == game_id).first()
    
    def get_new_public_games(self) -> list[Game]:
        return self._db_session.query(Game).filter(Game.public == True, Game.status == GameStatus.NEW).all()
    
    def get_games_by_owner_id(self, owner_id: UUID) -> list[Game]:
        return self._db_session.query(Game).filter(Game.owner_id == owner_id).all()
    
    def delete_game(self, game_id: UUID) -> bool:
        game = self._db_session.query(Game).filter(Game.id == game_id).first()
        if not game:
            return False
        self._db_session.delete(game)
        self._db_session.commit()
        return True
    
    def update_game_status(self, game_id: UUID, status: GameStatus) -> Game:
        game = self._db_session.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise Exception("Game not found")
        game.status = status
        self._db_session.commit()
        return game