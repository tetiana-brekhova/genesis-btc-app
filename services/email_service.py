from flask_mail import Mail, Message
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

def send_email(subject, recipients, body):
    with app.app_context():
        msg = Message(subject, recipients=recipients, body=body)
        mail.send(msg)
