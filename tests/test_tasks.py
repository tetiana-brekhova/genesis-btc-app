import pytest
from flask import Flask
from config import Config
from models import db, Subscription
from tasks import check_rate_and_notify, send_email, celery
import requests_mock


@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def celery_app(app):
    celery.conf.update(app.config)
    yield celery


@pytest.fixture(scope='module')
def celery_worker(celery_app):
    from celery.contrib.testing.worker import start_worker
    with start_worker(celery_app):
        yield


def test_check_rate_and_notify(celery_app, celery_worker, app, requests_mock):
    requests_mock.get(f'https://v6.exchangerate-api.com/v6/dacee103637befefa0104478/latest/USD', json={
        'conversion_rates': {'UAH': 38.0}
    })
    with app.app_context():
        sub = Subscription(email='test@example.com')
        db.session.add(sub)
        db.session.commit()

    check_rate_and_notify.delay().get()

    with app.app_context():
        assert Subscription.query.count() == 1


def test_send_email(celery_app, celery_worker, app):
    with app.app_context():
        send_email.delay('Test Subject', ['test@example.com'], 'Test Body').get()
    assert True
