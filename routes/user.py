from datetime import timedelta
from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Path
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User, UserRegister
from models.models import Users
from sqlalchemy.orm import Session
from . import crud
from config.db import session_local, engine, Base


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
    db_user = crud.get_user_by_email(db=db, email=user.email_user)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    else:
        return crud.create_user(db=db, user=user)

###Login a user
@user.post(
    path= '/login/access-token',
    status_code=status.HTTP_200_OK,
    summary= 'login an user',
    tags= ['Users']
)
def login(
        db: Session = Depends(get_db), 
        form_data:OAuth2PasswordRequestForm = Depends()
        ):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        db, username=form_data.username, password=form_data.password
        )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": crud.create_access_token(
        user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        }

@user.get(
    path= '/users/me',
    status_code=status.HTTP_200_OK,
    summary= 'login an user',
    tags= ['Users']
    )
def me(current_user: Users = Depends(crud.get_current_user)):
    """
    Test access
    """
    return current_user

###Show all users
@user.get(
    path= '/users',
    status_code=status.HTTP_200_OK,
    summary= 'Show all users',
    tags= ['Users']
)
def show_all_users(db:Session = Depends(get_db)):
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
    return crud.get_all_user(db=db)

        
###Show a users by id
@user.get(
    path= '/users/{user_id}',
    status_code=status.HTTP_200_OK,
    summary= 'Show a user',
    tags= ['Users']
)
def show_a_user(user_id: str = Path(
                                ...,
                                title = "User's ID",
                                description = "This is the person id. It's required"
                                ),  
                db: Session = Depends(get_db)):
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
    return crud.get_user_by_id(db=db, user_id=user_id)


###Delete a users
@user.delete(
    path= '/users/{user_id}/delete',
    status_code=status.HTTP_202_ACCEPTED,
    summary= 'Delete an user',
    tags= ['Users']
)
def delete_a_user(user_id: str= Path(
                                ...,
                                title = "Delete a user",
                                description = "This path delete the user"
                                ),
                db: Session = Depends(get_db)
                ):
    """
    This path operation delete a user in the app
    Parameters:
    -user_id
    
    return 
    -deleted
    """ 
    crud.delete_a_user(db=db, user_id=user_id)
    return 'Deleted'

###Update a users
@user.put(
    path= '/users/{user_id}/update',
    status_code=status.HTTP_200_OK,
    summary= 'Update an user',
    tags= ['Users']
)
def update_a_user(user: User= Body(...),
                  user_id: str= Path(
                        ...,
                        title = "Update a user",
                        description = "This path update the user name information"
                        ),
                db: Session = Depends(get_db)
                ):
    """
    This path operation delete a user in the app
    Parameters:
    - user_id
    
    return 
    -updated
    """ 
    crud.update_user(db=db, user_id=user_id, user=user)
    return 'Updated'
    