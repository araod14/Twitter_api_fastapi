"""
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base


class Tweets(Base):
    __tablename__ = "tweets"
    id_tweets = Column(String,primary_key=True, index=True)
    content = Column(String, index=True)
    created = Column(String, index=True)
    updted = Column(String, index=True)
    owner_id = Column(String, ForeignKey("Users.id"))

    owner = relationship("Users", back_populates="Tweets")
    """
