import time
import random
from fastapi.param_functions import Body
import praw
from praw.models import MoreComments
from urllib.parse import quote_plus
from sqlalchemy.sql.functions import mode
from starlette.routing import Route
import app
from app import oauth2
from app.database import SessionLocal
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from ..database import SessionLocal, engine, get_db
from textblob import TextBlob
from ..config import settings
import psycopg2

router = APIRouter(prefix='/comments', tags=['comments'])

@router.post("/")
def get_comments(db: SessionLocal = Depends(get_db)):
    positive_lis = []
    negative_lis = []
    neutral_lis = []
    user_connection = psycopg2.connect(user=settings.database_username, password=settings.database_password, host=settings.database_hostname, port=settings.database_port, database=settings.database_name)    
    cursor = user_connection.cursor()
    sql_query = "select * from users"
    cursor.execute(sql_query)
    user_records = cursor.fetchall()
    reply_query = "select * from reply"
    cursor.execute(reply_query)
    reply_records = cursor.fetchall()
    for rep in reply_records:
        positive_lis.append(rep[1])
        negative_lis.append(rep[2])
        neutral_lis.append(rep[3])
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
        authors_list = []
        #print("Started commenting")
        for top_level_comment in submission.comments:
            try:
                if top_level_comment.author != None:
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    all_comments_list = {}
                    all_comments_list['url'] = submission.url
                    all_comments_list['title'] = submission.title
                    all_comments_list['top_comment'] = top_level_comment.body
                    all_comments_list['author'] = str(top_level_comment.author)
                    try:
                        for rep in top_level_comment.replies:
                            authors_list.append(rep.author)
                    except:
                        pass
                    if TextBlob(top_level_comment.body.lower()).sentiment.polarity > 0:
                        if rec[1] not in authors_list:
                            top_level_comment.reply(random.choice(positive_lis))
                            all_comments_list['reply'] = random.choice(positive_lis)
                            all_comments_list['replyed_by'] = rec[1]
                        else:
                            try:
                                for top in top_level_comment.replies:
                                    if top.author == rec[1]:
                                        if top.body:
                                            all_comments_list['reply'] = top.body
                                            all_comments_list['replyed_by'] = rec[1]
                            except:
                                pass
                    elif TextBlob(top_level_comment.body.lower()).sentiment.polarity < 0:
                        if rec[1] not in authors_list:
                            top_level_comment.reply(random.choice(negative_lis))
                            all_comments_list['reply'] = random.choice(negative_lis)
                            all_comments_list['replyed_by'] = rec[1]
                        else:
                            try:
                                for top in top_level_comment.replies:
                                    if top.author == rec[1]:
                                        if top.body:
                                            all_comments_list['reply'] = top.body
                                            all_comments_list['replyed_by'] = rec[1]
                            except:
                                pass
                    else:
                        try:
                            for top in top_level_comment.replies:
                                auth_rep_list = []
                                auth_rep_list.append(top.author)
                        except:
                            pass
                        if rec[1] not in auth_rep_list:
                            top_level_comment.reply(random.choice(neutral_lis))
                            all_comments_list['reply'] = random.choice(neutral_lis)
                            all_comments_list['replyed_by'] = rec[1]
                new_comment = models.Comment(**all_comments_list)
                db.add(new_comment)
                db.commit()
            except:
                pass        
        all_comments = db.query(models.Comment).all()
        #print("Before time")
        time.sleep(settings.time_lapse)
        #print("After time")
    return {"message": "Succesfully stored comments in database"}
    
@router.get("/allcomments")
def allcomments(db: SessionLocal = Depends(get_db)):
    comments = db.query(models.Comment).all()
    if comments:
        return comments