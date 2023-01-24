#Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


#Fastapi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email_user: EmailStr =Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        max_length= 20,
        min_length=1
    )
    last_name: str = Field(
        ...,
        max_length= 20,
        min_length=1
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content_tweet : str = Field(
        ...,
        min_length= 1,
        max_length= 256
    )
    created_at: datetime= Field(default= datetime.now())
    update_at: Optional[datetime]= Field(default= datetime.now())
    by: User = Field(...)

#Path Operations
##Users
###Register a user
@app.post(
    path= '/signup',
    response_model= User,
    status_code=status.HTTP_201_CREATED,
    summary= 'Regiter an user',
    tags= ['Users']
)
def signup(user: UserRegister = Body(...)):
    """
    Singup
    This path operation register a user in the app
    Parameters:
        -Request body parameter
            -user : UserRegiser
    
    Return a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - Last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user
###Login a user
@app.post(
    path= '/login',
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary= 'login an user',
    tags= ['Users']
)
def login():
    pass
###Show all users
@app.get(
    path= '/users',
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary= 'Show all users',
    tags= ['Users']
)
def show_all_users():
    """
    This path operation show all users in the app
    Parameters:
    -
    return a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - Last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
###Show a users
@app.get(
    path= '/users/{user_id}',
    response_model= List[User],
    status_code=status.HTTP_200_OK,
    summary= 'Show a user',
    tags= ['Users']
)
def show_a_user():
    pass
###Delete a users
@app.delete(
    path= '/users/{user_id}/delete',
    response_model= User,
    status_code=status.HTTP_202_ACCEPTED,
    summary= 'Delete an user',
    tags= ['Users']
)
def delete_a_user():
    pass
###Update a users
@app.put(
    path= '/users/{user_id}/update',
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary= 'Update an user',
    tags= ['Users']
)
def update_a_user():
    pass

##Tweets
###Show all tweets
@app.get(
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
@app.post(
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
@app.get(
    path= '/tweets/{tweet_id}', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'show a Tweet',
    tags= ['Tweet'])
def show_a_tweet():
        pass

###Delete a tweet
@app.delete(
    path= '/tweets/{tweet_id}/delete', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'delete a Tweet',
    tags= ['Tweet'])
def delete_a_tweet():
        pass

###Update a tweet
@app.put(
    path= '/tweets/{tweet_id}/update', ###OJO
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'update a Tweet',
    tags= ['Tweet'])
def update_a_tweet():
        pass