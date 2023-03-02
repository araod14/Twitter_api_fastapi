from pydantic import Field
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content_tweet : str = Field(
                        ...,
                        min_length= 1,
                        max_length= 256
                        )
    created_at: datetime= Field(default= datetime.now())
<<<<<<< HEAD
    update_at: Optional[datetime]= Field(default= datetime.now())
    by: User= Field(...)
=======
    owner_id:str
>>>>>>> basedata
