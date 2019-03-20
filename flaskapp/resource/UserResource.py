from flask_restful import Resource
from flaskapp import db
from flaskapp.model.User import User

class UserResource(Resource):
    def get(self):
        print(User.query.all())
        return {'hello': 'world' }

    def post(self):
        return {"wow":"ok i got posted"}

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}