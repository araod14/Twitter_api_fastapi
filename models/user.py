from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from config.db import meta, engine


users = Table(
    'users', 
    meta, 
    Column('id',String(255),primary_key=True),
    Column('first_name', String(255)),
    Column('last_name', String(255)),
    Column('email', String(255)),
    Column('birth_date', String(255)),
    Column('password', String(255))
)
meta.create_all(engine)