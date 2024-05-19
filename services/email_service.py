from flask_mail import Mail, Message
from flask import Flask


app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.ukr.net',
    MAIL_PORT=465,
    MAIL_USERNAME='your@ukr.net',
    SECRET_KEY='your very secret key',
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    DEBUG=True,
)
mail = Mail(app)
mail.init_app(app)


def send_email(subject, recipients, body):
    # with app.app_context():
    msg = Message(subject, recipients=recipients, body=body)
    mail.send(msg)
