#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from typing import Optional
from uuid import UUID
from datetime import date


#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email_user: EmailStr =Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        max_length= 20,
        min_length=1
    )
    last_name: str = Field(
        ...,
        max_length= 20,
        min_length=1
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50
    )