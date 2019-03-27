# This file helps to create the relevant tables in the database
# The schema follow as what is defined in the Model classses in ./models folder
# To add a new schema, the model class should import db from flaskapp and extends from it.

# load the database environment variables
from dotenv import load_dotenv
load_dotenv()
from flaskapp import db


from flaskapp.model import *

db.drop_all()