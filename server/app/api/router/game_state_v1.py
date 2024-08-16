from fastapi import APIRouter, Cookie, HTTPException, Response
from typing import List

from db.model.game import GameStatus
from db.model.player import Player
from dependancies import auth_manager, get_game_crud, get_player_crud
from ..model import GameDetailsV1, GameCreateV1

router = APIRouter(
    prefix = "/v1/game-state",
    tags = ["game_state"],
    responses = {404: {"description": "Not found"}},
)

@router.post("/create-game", response_model = GameDetailsV1)
def create_game(game: GameCreateV1, token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    game_crud = get_game_crud()
    player_crud = get_player_crud()
    game_db = game_crud.create_game(game.name, jwt_payload.sub, game.max_players, game.public, game.password)
    player_crud.create_player(game_id = game_db.id, user_id = jwt_payload.sub, game_password = game.password)
    return game_db

@router.post("/join-game")
def join_game(code: str, password: str, token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    game_crud = get_game_crud()
    game_user_crud = get_player_crud()
    # Get the game by the join code
    game = game_crud.get_game_by_join_code(code)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    try:
        game = game_user_crud.create_player(game_id = game.id, user_id = jwt_payload.sub, game_password = password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return True

@router.get("/joined-games", response_model = List[GameDetailsV1])
def get_joined_games(token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    player_crud = get_player_crud()
    games: List[Player] = player_crud.get_games_by_user_id(user_id = jwt_payload.sub)
    print(games)
    # Get game details
    game_crud = get_game_crud()
    game_details: List[GameDetailsV1] = []
    for game in games:
        game_details.append(game_crud.get_game_by_id(game.game_id))
    return game_details

@router.get("/public-games", response_model = List[GameDetailsV1])
def get_public_games(token: str = Cookie(None)):
    _ = auth_manager.fastapi_validate_jwt(token)
    game_crud = get_game_crud()
    games: List[GameDetailsV1] = game_crud.get_new_public_games()
    return games

@router.get("/my-games", response_model = List[GameDetailsV1])
def get_my_games(token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    game_crud = get_game_crud()
    games: List[GameDetailsV1] = game_crud.get_games_by_owner_id(owner_id = jwt_payload.sub)
    return games

@router.delete("/delete-game")
def delete_game(game_id: str, token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    game_crud = get_game_crud()
    player_crud = get_player_crud()
    game = game_crud.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if str(game.owner_id) != jwt_payload.sub:
        raise HTTPException(status_code=403, detail="You are not the owner of this game")
    game_crud.delete_game(game_id)
    player_crud.delete_all_players_by_game_id(game_id)
    return True

@router.post("/leave-game")
def leave_game(game_id: str, token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    player_crud = get_player_crud()
    try:
        player_crud.delete_player_from_game(jwt_payload.sub, game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return True

@router.post("/start-game")
def start_game(game_id: str, token: str = Cookie(None)):
    jwt_payload = auth_manager.fastapi_validate_jwt(token)
    game_crud = get_game_crud()
    game = game_crud.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if str(game.owner_id) != jwt_payload.sub:
        raise HTTPException(status_code=403, detail="You are not the owner of this game")
    game_crud.update_game_status(game_id = game_id, status = GameStatus.RUNNING)
    return True