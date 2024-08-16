from typing import Optional
from pydantic import EmailStr
from sqlalchemy import UUID
from sqlalchemy.orm import scoped_session

from ..model.player import Player
from ..model.game import Game, GameStatus

class PlayerCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        from dependancies import auth_manager
        self._auth_manager = auth_manager
        self._db_session = db_session

    def create_player(self, user_id: UUID, game_id: UUID, game_password: Optional[str] = None) -> Optional[Player]:
        if self._is_user_in_game(user_id, game_id):
            return Player
        
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
        
        if self._get_player_count(game_id) >= game.max_players:
            raise Exception("Game is full")
        
        new_game_user = Player(user_id = user_id, game_id = game_id)
        self._db_session.add(new_game_user)
        self._db_session.commit()
        return new_game_user
    
    def get_games_by_user_id(self, user_id: UUID) -> list[Player]:
        return self._db_session.query(Player).filter(Player.user_id == user_id).all()
    
    def delete_all_players_by_game_id(self, game_id: UUID) -> bool:
        players = self._db_session.query(Player).filter(Player.game_id == game_id).all()
        for player in players:
            self._db_session.delete(player)
        self._db_session.commit()
        return True
    
    def delete_player_from_game(self, user_id: UUID, game_id: UUID) -> bool:
        player = self._db_session.query(Player).filter(Player.user_id == user_id, Player.game_id == game_id).first()
        if not player:
            return False
        self._db_session.delete(player)
        self._db_session.commit()
        return True

    def _is_user_in_game(self, user_id: UUID, game_id: UUID) -> bool:
        return self._db_session.query(Player).filter(Player.user_id == user_id, Player.game_id == game_id).first() is not None
    
    def _get_player_count(self, game_id: UUID) -> int:
        return self._db_session.query(Player).filter(Player.game_id == game_id).count()