from flask_restful import Resource, reqparse #resource is a like a path, need to create resource type object
from flaskapp import db
from flaskapp.model.User import User

#if u query sth, den use a GET, if you update/create, den use POST

class UserResource(Resource):
    def get(self):
        return {'hello': 'world' }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True) #parser is to get request body #help is an error message
        parser.add_argument('name', help = 'This field cannot be blank', required = True) #required is the HTTP required
        parser.add_argument('userIC', help = 'This field cannot be blank', required = True)
        parser.add_argument('mobilePhone', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        # Chceck if user exists
        if User.findUserByIC(data['userIC']):
            return {"Error":"User exists"}, 400

        # create user instance and add in databsed 
        user = User(name=data['name'],userIC=data['userIC'],mobilePhone=data['mobilePhone'],password=data['password'])
        db.session.add(user)
        db.session.commit()
        return parser.parse_args()

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}