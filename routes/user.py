from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Path
from fastapi import HTTPException, Depends
from typing import List
from schemas.user import User, UserRegister
from models.user import *
from sqlalchemy.orm import Session
from . import crud
from config.db import session_local, engine

Base.metadata.create_all(bind=engine)
user = APIRouter()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

#Path Operations
##Users
###Register a user
@user.post(
    path= '/signup',
    #response_model= User,
    status_code=status.HTTP_201_CREATED,
    summary= 'Regiter an user',
    tags= ['Users']
)
def signup_user(user: UserRegister, db: Session = Depends(get_db)):
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
    return crud.create_user(db=db, user=user)

###Login a user
@user.post(
    path= '/login',
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary= 'login an user',
    tags= ['Users']
)
def login():
    pass

###Show all users
@user.get(
    path= '/users',
    #response_model= User,
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
    pass
    #return conn.execute(select(Users.c.id,Users.c.first_name,Users.c.last_name, Users.c.email)).fetchall()
        
###Show a users
@user.get(
    path= '/users/{user_id}',
    #response_model= List[User],
    status_code=status.HTTP_200_OK,
    summary= 'Show a user',
    tags= ['Users']
)
def show_a_user(user_id: str = Path(
        ...,
        title = "User's ID",
        description = "This is the person id. It's required"
        )):
    """
    This path operation show a user in the app
    Parameters:
    -
    return a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - Last_name: str
        - birth_date: datetime
    """
    pass
    #return conn.execute(Users.select().where(Users.c.id == id)).first()

###Delete a users
@user.delete(
    path= '/users/{user_id}/delete',
    #response_model= User,
    status_code=status.HTTP_202_ACCEPTED,
    summary= 'Delete an user',
    tags= ['Users']
)
def delete_a_user(user_id: str= Path(
        ...,
        title = "Delete a user",
        description = "This path delete the user"
        )):
    """
    This path operation delete a user in the app
    Parameters:
    user_id
    -
    return deleted
    """ 
    #conn.execute(Users.delete().where(Users.c.id == user_id))
    return 'deleted'

###Update a users
@user.put(
    path= '/users/{user_id}/update',
    #response_model= User,
    status_code=status.HTTP_200_OK,
    summary= 'Update an user',
    tags= ['Users']
)
def update_a_user(user: User= Body(...),user_id: str= Path(
        ...,
        title = "Update a user",
        description = "This path update the user information"
        )):
    """
    This path operation delete a user in the app
    Parameters:
    user_id
    -
    return deleted
    """ 
    pass
    #conn.execute(Users.update().values(first_name = user.first_name, last_name = user.last_name,
    #    email= user.email_user).where(Users.c.id == user_id))
    #return conn.execute(Users.select().where(Users.c.id == id)).first()