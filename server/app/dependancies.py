from db.database_manager import DatabaseManager
from auth_manager import AuthManager

from db.crud import *

from config import settings

db_manager = DatabaseManager()
db_manager.create_all()

auth_manager = AuthManager(
    secret_key = settings.jwt_secret_key,
    token_expiry_minutes = settings.jwt_lifetime_minutes
)

def get_db():
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()
        
def get_auth_manager() -> AuthManager:
    return auth_manager

def get_user_crud() -> UserCRUD:
    return UserCRUD(db_manager.get_session())

def get_game_crud() -> GameCRUD:
    return GameCRUD(db_manager.get_session())

def get_game_user_crud() -> GameUserCRUD:
    return GameUserCRUD(db_manager.get_session())