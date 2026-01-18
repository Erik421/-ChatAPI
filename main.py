from fastapi import FastAPI
from routers import chats

from database import Base, engine
import models



app = FastAPI(title="Chats API")

app.include_router(chats.router)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)