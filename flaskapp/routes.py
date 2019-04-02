# Each resource class will register their end point in this file
# Define methods in the file in the resource folder
from flaskapp import api, db
from .resource.OperatorResource import OperatorResource
from .resource.GovernmentOfficialResource import GovernmentOfficialResource
from .resource.IncidentResource import IncidentResource
from .resource.SessionResource import SessionResource
from .model.User import User

api.add_resource(OperatorResource, '/user/operator')
api.add_resource(GovernmentOfficialResource, '/user/governmentofficial')
api.add_resource(IncidentResource, '/incident')
api.add_resource(SessionResource, '/session')