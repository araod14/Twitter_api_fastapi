from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://danel149:danel@localhost/twitter')

session_local = sessionmaker(engine)

conn = engine.connect()

meta = MetaData()