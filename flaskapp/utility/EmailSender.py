# if __name__ == "__main__" and __package__ is None:
#     from sys import path
#     from os.path import dirname as dir
#     path.append(dir(path[0]))
#     __package__ = "utility"


from flask import Flask
from ReportEmail import *
from flask_mail import Mail, Message
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

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

resultDict = findReportContent()
message = "Currently, there are {} incidents resolved and {} incidents still ongoing".format(\
            resultDict.get("numOfResolvedIncident"), resultDict.get("numOfOngoingIncident"))
send_email(message)

def send_email(message):
    msg = Message(
        message,
        sender = 'chuabck@gmail.com',
        recipients = ['wanglu1995.wl@gmail.com'])
    msg.body = "This is the email body testtesttest"
    mail.send(msg)
    return "Sent"

sched = BackgroundScheduler(daemon=True)
sched.add_job(send_email, trigger='interval', seconds=5)
sched.start()

if __name__ == "__main__":
    app.run(debug=True)