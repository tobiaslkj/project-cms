from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.GovernmentOfficial import GovernmentOfficial
from flask_jwt_extended import jwt_required, get_jwt_identity

class GovernmentOfficialResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        return {'hello': current_user }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', help = 'This field cannot be blank', required = True)
        parser.add_argument('userIC', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        go = GovernmentOfficial.findUserByIC(data['userIC'])
        if go and isinstance(go, GovernmentOfficial):
            return {"Error":"GovernmentOfficial record already exist"}, 400
        
        # create GovernmentOfficial instance and add in database
        governmentofficial = GovernmentOfficial(name=data['name'],userIC=data['userIC'],password=data['password'])
        governmentofficial.save()
        return parser.parse_args()
    
    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}