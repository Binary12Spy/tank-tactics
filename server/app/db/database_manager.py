from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Engine

from db.database import database
from config import settings
from .model import *

class DatabaseManager:
    _engine: Engine = None
    _session: scoped_session 
    
    def __init__(self) -> None:
        self._engine = create_engine(settings.database_url)
        self._session = scoped_session(sessionmaker(bind = self._engine))
        
    def get_session(self) -> scoped_session:
        return self._session()
    
    def create_all(self) -> None:
        database.metadata.create_all(self._engine)
    
    def drop_all(self) -> None:
        database.metadata.drop_all(self._engine)