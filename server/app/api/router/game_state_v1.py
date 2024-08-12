from fastapi import APIRouter, Cookie, HTTPException, Response
from typing import List

from db.model.game_user import GameUser
from dependancies import auth_manager, get_game_crud, get_game_user_crud
from ..model import GameDetailsV1, GameCreateV1

router = APIRouter(
    prefix = "/v1/game-state",
    tags = ["game_state"],
    responses = {404: {"description": "Not found"}},
)

@router.post("/create-game", response_model = GameDetailsV1)
def create_game(game: GameCreateV1, token: str = Cookie(None)):
    # Verify the jwt token
    jwt_payload = None
    try:
        jwt_payload = auth_manager.validate_jwt(token)
        if not jwt_payload:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    game_crud = get_game_crud()
    game = game_crud.create_game(game.name, jwt_payload.sub, game.public, game.password)
    return game

@router.post("/join-game")
def join_game(code: str, password: str, token: str = Cookie(None)):
    # Verify the jwt token
    jwt_payload = None
    try:
        jwt_payload = auth_manager.validate_jwt(token)
        if not jwt_payload:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    game_crud = get_game_crud()
    game_user_crud = get_game_user_crud()
    # Get the game by the join code
    game = game_crud.get_game_by_join_code(code)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    try:
        game = game_user_crud.create_game_user(game_id = game.id, user_id = jwt_payload.sub, game_password = password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return True

@router.get("/joined-games", response_model = List[GameDetailsV1])
def get_joined_games(token: str = Cookie(None)):
    # Verify the jwt token
    jwt_payload = None
    try:
        jwt_payload = auth_manager.validate_jwt(token)
        if not jwt_payload:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    game_user_crud = get_game_user_crud()
    games: List[GameUser] = game_user_crud.get_games_by_user_id(user_id = jwt_payload.sub)
    print(games)
    # Get game details
    game_crud = get_game_crud()
    game_details: List[GameDetailsV1] = []
    for game in games:
        game_details.append(game_crud.get_game_by_id(game.game_id))
    return game_details

@router.get("/public-games", response_model = List[GameDetailsV1])
def get_public_games(token: str = Cookie(None)):
    # Verify the jwt token
    jwt_payload = None
    try:
        jwt_payload = auth_manager.validate_jwt(token)
        if not jwt_payload:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    game_crud = get_game_crud()
    games: List[GameDetailsV1] = game_crud.get_public_games()
    return games

@router.get("/my-games", response_model = List[GameDetailsV1])
def get_my_games(token: str = Cookie(None)):
    # Verify the jwt token
    jwt_payload = None
    try:
        jwt_payload = auth_manager.validate_jwt(token)
        if not jwt_payload:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    game_crud = get_game_crud()
    games: List[GameDetailsV1] = game_crud.get_games_by_owner_id(owner_id = jwt_payload.sub)
    return games