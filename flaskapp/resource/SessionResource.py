from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.User import User
from flask_jwt_extended import jwt_required, create_access_token

class SessionResource(Resource):
    def get(self):
        return {'hello': 'world' }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('userIC', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        user = User.authenticate(data['userIC'], data['password'])

        if user:
            access_token = create_access_token(identity=user)
            return {'token':access_token}, 200
        else:
            return {"msg":"wrong password"}

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}