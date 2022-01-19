from typing import Optional
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text, true
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, String
from sqlalchemy.sql.visitors import TraversibleType
from .database import Base
from sqlalchemy import Column, Integer 

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    top_comment = Column(String, nullable=False)
    author = Column(String, nullable=False)
    reply = Column(String, default="-")
    replyed_by = Column(String, default="-")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    user_agent = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, nullable=False)
    top_comment = Column(String, nullable=False)
    commented_by = Column(String, nullable=False)
    vote_type = Column(String, nullable=False)
    voted_by = Column(String, nullable=False)


class Reply(Base):
    __tablename__ = "reply"
    id = Column(Integer, primary_key=True, nullable=False)
    positive_replies = Column(String, nullable=False)
    negative_replies = Column(String, nullable=False)
    neutral_replies = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))