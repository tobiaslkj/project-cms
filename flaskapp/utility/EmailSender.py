
from flaskapp import app
from flask_mail import Mail, Message
import time
import atexit


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

TEMPLATE = '''\
Dear Prime Minister,
      
{0}
        
Please feel free to contact us if you need any further information.
           
Sincerely,
Crisis Management System - Team 8scomplements
        
Note: This is an automatically generated email.
       
'''

def send_email(message):
    with app.app_context():
        msg = Message(
            'Interval Report',
            sender = 'chuabck@gmail.com',
            recipients = ['wanglu1995.wl@gmail.com'])
        msg.body = TEMPLATE.format(message)
        mail.send(msg)
        return "Sent"

if __name__ == "__main__":
    app.run(debug=True)