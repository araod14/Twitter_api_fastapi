from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Path
from typing import List
from schemas.user import User, UserRegister
from models.user import users
from config.db import conn
from cryptography.fernet import Fernet
from uuid import uuid4
from sqlalchemy.sql import select
import json 


key = Fernet.generate_key()
f =Fernet(key)
user = APIRouter()

#Path Operations
##Users
###Register a user
@user.post(
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

    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user
    """
    new_user = {'first_name':user.first_name,'last_name':user.last_name,'birth_date':user.birth_date, 'email':user.email_user}
    new_user['password'] = f.encrypt(user.password.encode('utf-8'))
    new_user['id'] = uuid4()
    conn.execute(users.insert().values(new_user))
    #return conn.execute(users.select().where(users.c.id==result.inserted_primary_key['id'])).first()
    #return result.inserted_primary_key['id']

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
    return conn.execute(select(users.c.id,users.c.first_name,users.c.last_name, users.c.email)).fetchall()
        
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
    return conn.execute(users.select().where(users.c.id == user_id)).first()

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
    conn.execute(users.delete().where(users.c.id == user_id))
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
    
    conn.execute(users.update().values(first_name = user.first_name, last_name = user.last_name,
        email= user.email_user).where(users.c.id == user_id))
    return conn.execute(users.select().where(users.c.id == id)).first()