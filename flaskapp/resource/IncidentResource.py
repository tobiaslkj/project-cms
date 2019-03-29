from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.Incident import Incident

class IncidentResource(Resource):
    def get(self):
        return {'Incident': 'world' }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('address', help='Address field cannot be blank', required = True)
        parser.add_argument('postalCode', help='Postal Code field cannot be blank', required = True)
        parser.add_argument('longtitude', help='This field cannot be blank', required = True)
        parser.add_argument('latitude', help='This field cannot be blank', required = True)
        parser.add_argument('assignedBy', help='This field cannot be blank', required = True)
        parser.add_argument('gpIC', help='This field cannot be blank', required = True)
        parser.add_argument('emerType', help='This field cannot be blank', required = True)

        # Create the user instance and add to db
        incident =Incident(address=data['address'], postalCode=data['postalCode'], longtitude=data['longtitude'], latitude=data['latitude'], assignedBy=data['assignedBy'], gpIC=data['gpIC'], emerType=data['emerType'])
        db.session.add(incident)
        db.session.commit()
        return parser.parse_args()
          

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}