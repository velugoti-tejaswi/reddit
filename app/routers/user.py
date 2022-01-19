import app
from app.database import SessionLocal
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from ..database import SessionLocal, engine, get_db
from sqlalchemy.orm.session import Session


router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash  the passwod

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    print("Check it......")
    print(user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} does'nt exit")

    return user