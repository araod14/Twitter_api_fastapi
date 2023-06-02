from fastapi import APIRouter
from fastapi import status
from schemas.tweet import Tweet
from fastapi import Depends
from sqlalchemy.orm import Session
from models.models import *
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
def post_tweet(tweet: Tweet, 
               user_id:str, 
               db: Session = Depends(get_db)):
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

###Show all tweets from a user
@tweets.get(
    path= '/users/{user_id}/tweets',
    #response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'show all Tweets from a user',
    tags= ['Tweet'])
def show_all_tweets(user_id:str, db: Session = Depends(get_db)):
    """
    Show all tweets from a user
    This path operation show all tweets from a user
    Parameters:
        -Request Paths parameter
        -User_id
    
    Return a json with the tweets information:
        - tweet_id: UUID 
        - content_tweet : str 
        - created_at: datetime
        - by: User 
    """
    return crud.get_tweets_from_user(db=db, user_id=user_id)

###Delete a tweet
@tweets.delete(
    path= '/tweets/{tweet_id}/delete', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'delete a Tweet',
    tags= ['Tweet'])
def delete_a_tweet(tweet_id:str, db: Session = Depends(get_db)):
    """
    This path operation delete a tweet in the app
    Parameters:
    -tweet_id
    
    return 
    -deleted
    """ 
    crud.delete_a_tweet(db=db, tweet_id=tweet_id)
    return 'Deleted'

