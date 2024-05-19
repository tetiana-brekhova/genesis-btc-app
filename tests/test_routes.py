import pytest
from flask import Flask
from config import Config
from models import db, Subscription
from routes import bp
from config import Config


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.register_blueprint(bp)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_subscribe(client):
    response = client.post('/api/subscribe', json={'email': 'test@example.com'})
    assert response.status_code == 200
    assert response.json == {'message': 'Subscribed successfully'}

def test_subscribe_no_email(client):
    response = client.post('/api/subscribe', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Email is required'}

def test_rate(client, requests_mock):
    requests_mock.get(f'https://v6.exchangerate-api.com/v6/dacee103637befefa0104478/latest/USD', json={
        'conversion_rates': {'UAH': 38.0}
    })
    response = client.get('/api/rate')
    assert response.status_code == 200
    assert response.json == {'rate': 38.0}
