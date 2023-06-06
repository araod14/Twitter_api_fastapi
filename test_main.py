import json
from main import app
from fastapi.testclient import TestClient
from config.db import session_local, engine
from models.models import Base


Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

## Tweets
tweets = [
    {
  "tweet_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "content_tweet": "First tweet",
  "created_at": "2023-06-05T13:05:12.120637",
  "owner_id": "83dfed72-c2e3-4970-9b6c-ee05a7f67f2b"
    },
    {
  "tweet_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "content_tweet": "Second tweet",
  "created_at": "2023-06-05T13:05:12.120637",
  "owner_id": "83dfed72-c2e3-4970-9b6c-ee05a7f67f2b"
    }
]

def test_post_tweet():
    response = client.post("/users/83dfed72-c2e3-4970-9b6c-ee05a7f67f2b/post", json=tweets[0])
    assert response.status_code == 201
    assert response.json()["content"] == "First tweet"

def test_get_tweets():
    response = client.get("/tweets")
    assert response.status_code == 200
    assert response.json()[0]["content"] == "string"
    assert response.json()[1]["content"] == "string"

def test_get_tweets_from_user():
    response = client.get("/users/75d74717-f6ad-4ed6-91b0-44db56d4dbd4/tweets")
    assert response.status_code == 200
    assert len(response.json()) == 4


## Users