from sqlalchemy.orm import scoped_session

from ..model.games import Game, GameStatus

class GameCRUD:
    _db_session: scoped_session
    
    def __init__(self, db_session: scoped_session) -> None:
        from dependancies import auth_manager
        self._auth_manager = auth_manager
        self._db_session = db_session

    def create_game(self, name: str) -> Game:
        # Generate a join code, unique to the game
        join_code = self._auth_manager.generate_join_code()
        # Verify the join code is unique
        while self._db_session.query(Game).filter(Game.join_code == join_code).first():
            join_code = self._auth_manager.generate_join_code()
        
        new_game = Game(name = name, join_code = join_code, game_status = GameStatus.CREATED)
        self._db_session.add(new_game)
        self._db_session.commit()
        return new_game