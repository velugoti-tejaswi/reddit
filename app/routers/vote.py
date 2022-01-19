from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import praw
from praw.models import MoreComments
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from .. import schemas, database, models, oauth2
from .comments import get_comments
from app.database import SessionLocal, get_db
from textblob import TextBlob
import psycopg2
from ..config import settings

router = APIRouter(prefix="/vote", tags=['vote'])

@router.post("/")
def vote(db: SessionLocal = Depends(get_db)):
    user_connection = psycopg2.connect(user=settings.database_username, password=settings.database_password, host=settings.database_hostname, port=settings.database_port, database=settings.database_name)    
    cursor = user_connection.cursor()
    sql_query = "select * from users"
    cursor.execute(sql_query)
    user_records = cursor.fetchall()
    for rec in user_records:
        #print(rec)
        #print("User login")
        all_comments_list = []
        reddit = praw.Reddit(
            client_id=rec[2],
            client_secret=rec[3],
            user_agent=rec[4],
            username=rec[1],
            password="Janejames@143",
            check_for_async=False
        )
        submission = reddit.submission(url="https://www.reddit.com/r/apexlegends/comments/rhyjbi/this_busted_underwater_hideout_feels_like_a_hack/")
        #print("After request...")
        for top_level_comment in submission.comments:
            #print("Inside For loop...")
            try:
                if top_level_comment.author != None:
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    all_comments_list = {}
                    all_comments_list['top_comment'] = top_level_comment.body
                    all_comments_list['commented_by'] = str(top_level_comment.author)
                    all_comments_list['voted_by'] = rec[1]
                    if TextBlob(top_level_comment.body.lower()).sentiment.polarity > 0:
                        top_level_comment.upvote()
                        all_comments_list['vote_type'] = "upvote"
                    else:
                        top_level_comment.downvote()
                        all_comments_list['vote_type'] = "downvote"
                    new_vote = models.Vote(**all_comments_list)
                    db.add(new_vote)
                    db.commit()
            except:
                pass
            #print("End for loop...")
    return {"message": "Voted successfully..."}

@router.get("/getvotes")
def get_votes(db: SessionLocal = Depends(get_db)):
    votes = db.query(models.Vote).all()
    if votes:
        return votes