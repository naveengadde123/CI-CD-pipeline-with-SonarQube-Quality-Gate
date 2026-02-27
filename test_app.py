from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_add():
    client = app.test_client()
    response = client.post("/add", json={"a": 5, "b": 3})
    assert response.json["result"] == 8