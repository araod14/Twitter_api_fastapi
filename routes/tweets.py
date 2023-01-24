from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from typing import List
from schemas.tweet import Tweet
import json 



tweets = APIRouter()

##Tweets
###Show all tweets
@tweets.get(
    path= '/',
    response_model= List[Tweet],
    status_code=status.HTTP_200_OK,
    summary= 'Show Tweets',
    tags= ['Tweet'])
def home():
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
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results 

###Post a tweet
@tweets.post(
    path= '/post',
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
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        if tweet_dict['update_at']:
            tweet_dict['update_at'] = str(tweet_dict['update_at'])  ###OJO
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

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