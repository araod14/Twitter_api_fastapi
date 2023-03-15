from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base



class Users(Base):
    __tablename__ = "users" 
    id = Column(String,primary_key=True, index=True)
    user_name = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    birth_date = Column(String, index=True)
    password = Column(String)

    tweets = relationship("Tweets", back_populates="owner")

class Tweets(Base):
    __tablename__ = "tweets"
    id_tweets = Column(String,primary_key=True, index=True)
    content = Column(String, index=True)
    created = Column(String, index=True)
    #updted = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="tweets")