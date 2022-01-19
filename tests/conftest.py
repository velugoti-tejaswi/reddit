from starlette.types import Scope
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app import models
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"username": "Tejaswi",
                 "password": "1234",
                 "client_id": "hi", 
                 "client_secret": "dummy", 
                 "user_agent": "ddd"
                }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})



@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client



@pytest.fixture
def test_comments(test_user, session):
    comments_data = [{
        "top_comment": "\"Oh hey look, carepackage.\" *Walks over* and then the water begins its retribution on humanity",
        "url": "https://v.redd.it/96j3kh8ijy581",
        "id": 1,
        "author": "losermode9000",
        "title": "This busted UNDERWATER hideout feels like a hack 😂",
        "reply": "-"
    }, 
    {
       "top_comment": "Welp this is getting patched",
        "url": "https://v.redd.it/96j3kh8ijy581",
        "id": 2,
        "author": "SilentReavus",
        "title": "This busted UNDERWATER hideout feels like a hack 😂",
        "reply": "Thanks..." 
    },    
    {
        "top_comment": "I’ve been hiding in trees as Rev. Thx for the new strat",
        "url": "https://v.redd.it/96j3kh8ijy581",
        "id": 3,
        "author": "mrpeepeetoucher",
        "title": "This busted UNDERWATER hideout feels like a hack 😂",
        "reply": "Will Look into this... Thanks For Your Feedback"
    }, 
    {
        "top_comment": "Patchnotes: decreased the depth of the water",
        "url": "https://v.redd.it/96j3kh8ijy581",
        "id": 5,
        "author": "nulllzero",
        "title": "This busted UNDERWATER hideout feels like a hack 😂",
        "reply": "Thanks For Your Feedback"
    }]

    def create_comment_model(comment):
        return models.Comment(**comment)

    comment_map = map(create_comment_model, comments_data)
    comments = list(comment_map)

    session.add_all(comments)
    session.commit()

    comments = session.query(models.Comment).all()
    return comments


@pytest.fixture
def test_votes(test_user, session):
    votes_data = [{
        "top_comment": "\"Oh hey look, carepackage.\" *Walks over* and then the water begins its retribution on humanity",
        "commented_by": "losermode9000",
        "vote_type": "downvote",
        "id": 1
    }, 
    {
       "top_comment": "Welp this is getting patched",
        "commented_by": "SilentReavus",
        "vote_type": "downvote",
        "id": 2
    },    
    {
        "top_comment": "I’ve been hiding in trees as Rev. Thx for the new strat",
        "commented_by": "mrpeepeetoucher",
        "vote_type": "upvote",
        "id": 3
    }, 
    {
        "top_comment": "lol this is like hiding in the bushes on KC but better.",
        "commented_by": "h4mx0r",
        "vote_type": "upvote",
        "id": 4
    }]

    def create_vote_model(vote):
        return models.Vote(**vote)

    vote_map = map(create_vote_model, votes_data)
    votes = list(vote_map)

    session.add_all(votes)
    session.commit()

    comments = session.query(models.Vote).all()
    return comments