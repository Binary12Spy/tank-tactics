from fastapi import APIRouter, Cookie, HTTPException, Response

from dependancies import auth_manager, get_game_crud
from ..model import GameDetailsV1, GameCreateV1

router = APIRouter(
    prefix = "/v1/game-state",
    tags = ["game_state"],
    responses = {404: {"description": "Not found"}},
)

@router.post("/create-game", response_model = GameDetailsV1)
def create_game(game: GameCreateV1, token: str = Cookie(None)):
    # Verify the jwt token
    try:
        if not auth_manager.validate_jwt(token):
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    game_crud = get_game_crud()
    game = game_crud.create_game(game.name)
    return game