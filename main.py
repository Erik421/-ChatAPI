from fastapi import FastAPI
from routers import chats

from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chats API")

app.include_router(chats.router)
