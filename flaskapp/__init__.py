# Initializion of app is done here
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flaskapp.utility.ReportEmail import *
from flask_mail import Mail, Message
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

#print("========================================================================================================")
app = Flask(__name__,static_folder='./client', static_url_path='')
app.config['SECRET_KEY'] = config['FLASK_APP_SECRET']
sqlURI = "mysql://"+config['DATABASE_USERNAME']+":"+config['DATABASE_PASSWORD']+"@"+config['DATABASE_HOST']+"/"+config['DATABASE_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = sqlURI
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

# Configuration for jwt
app.config['JWT_SECRET_KEY']=config['FLASK_APP_SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES']=86400
jwt = JWTManager(app)   

#ma = Marshmallow(app)
from flaskapp import routes

@jwt.user_claims_loader
def jwt_extend_claims_override(user):
    return user.getClaimsOfUser()

@jwt.user_identity_loader
def jwt_extend_identity_override(user):
    return user.userIC

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory('client', path)


#app = Flask(__name__)

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