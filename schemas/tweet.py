from pydantic import Field
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from schemas.user import User


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content_tweet : str = Field(
        ...,
        min_length= 1,
        max_length= 256
    )
    created_at: datetime= Field(default= datetime.now())
    update_at: Optional[datetime]= Field(default= datetime.now())
    #by: User = Field(...)