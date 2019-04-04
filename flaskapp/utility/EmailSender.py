from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    #EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "8scomplements@gmail.com",
    MAIL_PASSWORD = "trutrutru"
)

mail = Mail(app)

def send_email():
    msg = Message(
        'Hello fwen',
        sender = 'chuabck@gmail.com',
        recipients = ['chuabck@hotmail.com'])
    msg.body = "This is the email body testtesttest"
    mail.send(msg)
    return "Sent"

if __name__ == "__main__":
    app.run(debug=True)