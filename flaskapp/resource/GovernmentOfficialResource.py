from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.GovernmentOfficial import GovernmentOfficial
from flask_jwt_extended import jwt_required, get_jwt_claims

class GovernmentOfficialResource(Resource):
    # As currently there is no route to limit only for government official,
    # we can use jwt_required to secure government_official routes
    # as operator can access what a government official can do, we can
    # just check if the request has a valid token
    @jwt_required
    def get(self):
        user_info = get_jwt_claims()

        return {'hello': userinfo }

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