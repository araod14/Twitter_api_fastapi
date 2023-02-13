from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.db import meta, engine


tweets = Table(
    'tweets', 
    meta, 
    Column('id_tweets',String(255),primary_key=True),
    Column('content', String(255)),
    Column('created', String(255)),
    Column('updted', String(255)),
    Column('id', String(255),ForeignKey("users.id"))
)
meta.create_all(engine)