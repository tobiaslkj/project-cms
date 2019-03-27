# Initializion of app is done here
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from .config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config['FLASK_APP_SECRET']
sqlURI = "mysql://"+config['DATABASE_USERNAME']+":"+config['DATABASE_PASSWORD']+"@"+config['DATABASE_HOST']+"/"+config['DATABASE_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = sqlURI
db = SQLAlchemy(app)
api = Api(app)

from flaskapp import routes

