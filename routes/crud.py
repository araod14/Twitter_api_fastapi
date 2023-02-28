
from schemas.user import User, UserRegister
from models.user import Users
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from uuid import uuid4


key = Fernet.generate_key()
f =Fernet(key)

def create_user(db:Session, user: UserRegister):
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
    password_encrypted = f.encrypt(user.password.encode('utf-8'))
    user_id = uuid4()
    new_user = Users(id=user_id,password=password_encrypted,
    first_name=user.first_name, last_name=user.last_name,
    birth_date=user.birth_date, email=user.email_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user