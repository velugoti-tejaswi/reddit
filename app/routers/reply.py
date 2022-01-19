import app
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from sqlalchemy.orm.session import Session
from ..database import SessionLocal, engine, get_db

router = APIRouter(prefix="/reply", tags=['Reply'])

@router.post("/", status_code=201, response_model=schemas.ReplyOut)
def create_reply(replys: schemas.ReplyCreate, db: Session = Depends(get_db)):
    print(replys)
    new_reply = models.Reply(**replys.dict())
    print("Check it...")
    print(replys)
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)

    return new_reply