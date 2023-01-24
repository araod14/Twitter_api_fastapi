from fastapi import APIRouter
from fastapi import status
from fastapi import Body
from typing import List
import json 
from schemas.user import User, UserRegister



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
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user
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
    response_model= User,
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
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
###Show a users
@user.get(
    path= '/users/{user_id}',
    response_model= List[User],
    status_code=status.HTTP_200_OK,
    summary= 'Show a user',
    tags= ['Users']
)
def show_a_user():
    pass
###Delete a users
@user.delete(
    path= '/users/{user_id}/delete',
    response_model= User,
    status_code=status.HTTP_202_ACCEPTED,
    summary= 'Delete an user',
    tags= ['Users']
)
def delete_a_user():
    pass
###Update a users
@user.put(
    path= '/users/{user_id}/update',
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary= 'Update an user',
    tags= ['Users']
)
def update_a_user():
    pass