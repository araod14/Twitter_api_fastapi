#import json
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

tweets = [
    {
        "content_tweet": "First tweet"
    },
    {
        "content_tweet": "Second tweet"
    }
]
def test_post_tweet():
    response = client.post("/users/1/post", json=tweets[0])
    assert response.status_code == 201
    assert response.json()["content_tweet"] == "First tweet"

def test_get_tweets():
    response = client.get("/tweets")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["content_tweet"] == "First tweet"
    assert response.json()[1]["content_tweet"] == "Second tweet"

def test_get_tweets_from_user():
    response = client.get("/users/1/tweets")
    assert response.status_code == 200
    assert len(response.json()) == 2


