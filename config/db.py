from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://danel149:danel@localhost/twitter')
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#conn = engine.connect()
Base = declarative_base()