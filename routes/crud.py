
from datetime import datetime, timedelta
from schemas.user import UserRegister, Token
from models.models import Users, Tweets
from config.db import session_local
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Any, Union
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from fastapi import HTTPException, status
from pydantic import ValidationError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/access-token"
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = "4685284629656970e8d44144d3f9e94baff7ff006ee10062f0171a28fdb3023f"
# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60

##Get database
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

##Create token acces
def create_access_token(
    subject: Union[str, Any], 
    expires_delta: timedelta = None
    ) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

##Users
def create_user(db:Session, user: UserRegister):
    hashed_password = get_password_hash(user.password)
    user_id = uuid4()
    new_user = Users(id=user_id, user_name=user.username ,password=hashed_password,
                    first_name=user.first_name, last_name=user.last_name,
                    birth_date=user.birth_date, email=user.email_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_user(db:Session):
    return db.query(Users).all()

def get_user_by_username(db:Session, username:str): 
    return db.query(Users).filter(Users.user_name == username).first()

def get(db:Session, id:str): 
    return db.query(Users).filter(Users.id == id).first()

def get_user_by_id(db:Session, user_id:str): 
    return db.query(Users).filter(Users.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(Users).filter(Users.email == email).first()

def authenticate(db: Session, *, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    #password_db = db.query(Users).filter(Users.password==password)
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="wrong password")
    return user

def get_current_user(
        db:Session=Depends(get_db), 
        token: str = Depends(reusable_oauth2)):
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=ALGORITHM
                )
            token_data = Token(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
        )
        user = get(db, id=token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
def delete_a_user(db:Session, user_id:str):
    # Buscar el usuario que deseas eliminar
    user = db.query(Users).filter_by(id = user_id).first()
    # Si el usuario existe, borrar todos sus tweets
    if user:
        db.query(Tweets).filter_by(owner_id = user.id).delete()
        db.delete(user)
    db.commit()

def update_user(db:Session, user_id:str, user:Users):
    db.query(Users).filter(Users.id == user_id).update({'first_name':user.first_name}, synchronize_session=False)
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