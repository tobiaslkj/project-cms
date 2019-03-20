# Each resource class will register their end point in this file
# Define methods in the file in the resource folder
from flaskapp import api, db
from .resource.UserResource import UserResource
from .resource.IncidentResource import IncidentResource
from .model.User import User

api.add_resource(UserResource, '/user')
api.add_resource(IncidentResource, '/incident')