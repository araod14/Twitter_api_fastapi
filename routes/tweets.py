from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from typing import List
from schemas.tweet import Tweet
from schemas.user import User
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user import *
from . import crud
from config.db import session_local, engine

Base.metadata.create_all(bind=engine)
tweets = APIRouter()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


##Tweets
###Show all tweets
@tweets.get(
    path= '/tweets',
    #response_model= List[Tweet],
    status_code=status.HTTP_200_OK,
    summary= 'Show Tweets',
    tags= ['Tweet'])
def home(db:Session = Depends(get_db)):
    """
    Show all tweets
    This path operation show all tweets in the app
    Parameters:
        -Request Paths parameter
    
    Return a json with the tweets information:
        - tweet_id: UUID 
        - content_tweet : str 
        - created_at: datetime
        - by: User 
    """
    return crud.get_tweets(db=db)

###Post a tweet
@tweets.post(
    path= '/users/{user_id}/post',
    #response_model= Tweet,
    status_code=status.HTTP_201_CREATED,
    summary= 'Post a Tweet',
    tags= ['Tweet'])
def post_tweet(tweet: Tweet, user_id:str, db: Session = Depends(get_db)):
    """
    Post a tweet
    This path operation post a tweet in the app
    Parameters:
        -Request body parameter
            -tweet : Tweet
    
    Return a json with the basic tweet information:
        - tweet_id: UUID 
        - content_tweet : str 
        - created_at: datetime
        - update_at: Optional[datetime]
        - by: User 
    """
    return crud.create_tweet(db=db, tweet=tweet, user_id=user_id)

###Show a tweet
@tweets.get(
    path= '/tweets/{tweet_id}', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'show a Tweet',
    tags= ['Tweet'])
def show_a_tweet():
        pass

###Delete a tweet
@tweets.delete(
    path= '/tweets/{tweet_id}/delete', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'delete a Tweet',
    tags= ['Tweet'])
def delete_a_tweet():
        pass

###Update a tweet
@tweets.put(
    path= '/tweets/{tweet_id}/update', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'update a Tweet',
    tags= ['Tweet'])
def update_a_tweet():
        pass