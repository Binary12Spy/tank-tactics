from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

import dependancies
from config import settings

from api.router.auth_v1 import router as auth_v1
from api.router.game_state_v1 import router as game_state_v1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_v1, prefix="/api")
app.include_router(game_state_v1, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = settings.server_host, port = settings.server_port, reload = True)