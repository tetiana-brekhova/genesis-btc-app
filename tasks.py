from celery import Celery
from services.exchange_rate_service import get_current_rate
from services.email_service import send_email
from models import Subscription, db
from config import Config
from flask import Flask

celery = Celery(__name__)
celery.config_from_object(Config)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.ukr.net'  # Change to your mail server
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'b-t-p@ukr.net'  # Change to your email
app.config['MAIL_PASSWORD'] = 'AZCpy8Nc7fYusMoa'     # Change to your password
db.init_app(app)


@celery.task
def check_rate_and_notify():
    current_rate = get_current_rate()
    with app.app_context():
        subscriptions = Subscription.query.all()
        recipients = [sub.email for sub in subscriptions]
        send_email('USD/UAH Exchange Rate', recipients, f'The current exchange rate is {current_rate} UAH per USD.')
