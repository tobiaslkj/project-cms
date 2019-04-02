from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.Operator import Operator
from flask_jwt_extended import jwt_required, get_jwt_identity
from flaskapp.access_control import operator_required

class OperatorResource(Resource):
    @operator_required
    def get(self):
        current_user = get_jwt_identity()

        return {'hello': current_user }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', help = 'This field cannot be blank', required = True)
        parser.add_argument('userIC', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        o = Operator.findUserByIC(data['userIC'])
        if o and isinstance(o, Operator):
            return {"Error":"Operator record already exist"}, 400
        
        # create operator instance and add in database
        operator = Operator(name=data['name'],userIC=data['userIC'],password=data['password'])
        operator.save()
        return parser.parse_args()

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}