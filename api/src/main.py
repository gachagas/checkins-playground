from fastapi import FastAPI

from src.routes.checkins import router

app = FastAPI()

app.include_router(router)
