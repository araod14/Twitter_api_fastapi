#Fastapi
from fastapi import FastAPI
from routes.user import user
from routes.tweets import tweets

app = FastAPI(
    title='API Twitter',
    description='API models twitter',
    version='0.0.9'
    )

app.include_router(user)
app.include_router(tweets)