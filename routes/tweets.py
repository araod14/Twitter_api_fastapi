from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from typing import List
from schemas.tweet import Tweet
from models.tweets import tweets
from config.db import conn
from uuid import uuid4
from sqlalchemy import select



tweets = APIRouter()

##Tweets
###Show all tweets
@tweets.get(
    path= '/tweets',
    #response_model= List[Tweet],
    status_code=status.HTTP_200_OK,
    summary= 'Show Tweets',
    tags= ['Tweet'])
def home():
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
    
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results 
    """
    return conn.execute(select(tweets.c.id_tweets,tweets.c.content,tweets.c.created)).fetchall()

###Post a tweet
@tweets.post(
    path= 'users/{user_id}/post',
    response_model= Tweet,
    status_code=status.HTTP_201_CREATED,
    summary= 'Post a Tweet',
    tags= ['Tweet'])
def post(tweet: Tweet = Body(...)):
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
    new_tweet = {'content':Tweet.content_tweet,'created':Tweet.created_at,'id':Tweet.by}
    new_tweet['id_tweets'] = uuid4()
    conn.execute(tweets.insert().values(new_tweet))

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