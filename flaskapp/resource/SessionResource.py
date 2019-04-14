from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.User import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_claims

class SessionResource(Resource):
    @jwt_required
    def get(self):
        user_info = get_jwt_claims()

        return {'user': user_info }

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