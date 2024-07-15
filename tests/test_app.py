import pytest
from flask_app.app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
    yield client


def test_ask_endpoint(client):
    response = client.post('/ask', json={'question': 'Who was the 8th Israeli Prime minister?'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'answer' in data
