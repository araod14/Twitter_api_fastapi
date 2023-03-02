
from schemas.user import UserRegister
from models.models import Users, Tweets
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from uuid import uuid4


key = Fernet.generate_key()
f =Fernet(key)


##Users
def create_user(db:Session, user: UserRegister):
    password_encrypted = f.encrypt(user.password.encode('utf-8'))
    user_id = uuid4()
    new_user = Users(id=user_id, password=password_encrypted,
                    first_name=user.first_name, last_name=user.last_name,
                    birth_date=user.birth_date, email=user.email_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_user(db:Session):
    return db.query(Users).all()

def get_user_by_id(db:Session, user_id:str):
    return db.query(Users).filter(Users.id == user_id).first()

def delete_a_user(db:Session, user_id:str):
    db.query(Users).filter(Users.id == user_id).delete(synchronize_session=False)
    db.commit()

##Tweets
def create_tweet(db:Session, tweet: Tweets, user_id:str):
    tweet_id = uuid4()
    db_tweet = Tweets(id_tweets=tweet_id, content=tweet.content_tweet, 
                    created=tweet.created_at, owner_id=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

def get_tweets(db:Session):
    return db.query(Tweets).all()

def get_tweets_from_user(db:Session, user_id:str):
    return db.query(Tweets).filter(Tweets.owner_id == user_id).all()

def delete_a_tweet(db:Session, tweet_id:str):
    db.query(Tweets).filter(Tweets.id_tweets == tweet_id).delete(synchronize_session=False)
    db.commit()