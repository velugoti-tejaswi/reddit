from fastapi import FastAPI
from . import models
from .database import engine
from .routers import comments, user, auth, vote, reply
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(comments.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(reply.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Reddit API"}
