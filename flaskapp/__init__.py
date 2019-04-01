# Initializion of app is done here
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = config['FLASK_APP_SECRET']
sqlURI = "mysql://"+config['DATABASE_USERNAME']+":"+config['DATABASE_PASSWORD']+"@"+config['DATABASE_HOST']+"/"+config['DATABASE_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = sqlURI
db = SQLAlchemy(app)
api = Api(app)

# Configuration for jwt
app.config['JWT_SECRET_KEY']=config['FLASK_APP_SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES']=86400
jwt = JWTManager(app)   

from flaskapp import routes

@jwt.user_claims_loader
def jwt_extend_claims_override(user):
    return {
        "userIC": user.userIC,
        "role": user.discriminator
    }

@jwt.user_identity_loader
def jwt_extend_identity_override(user):
    return user.userIC

