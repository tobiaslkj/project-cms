from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.Incident import Incident
from flaskapp.model.Incident import GeneralPublic
from datetime import datetime

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
        parser.add_argument('eid', help='This field cannot be blank', required = True)
        parser.add_argument('name', help='name cannot be blank',required=True)
        parser.add_argument('userIC', help='userIC cannot be blank',required=True)
        parser.add_argument('mobilePhone', help='mobilePhone cannot be blank', required=True)
        data = parser.parse_args()

        # Check if a GP does not exist in database
        if(GeneralPublic.query.filter_by(userIC=data['userIC']).first() is None):
            gp = GeneralPublic(name=data['name'], userIC=data['userIC'], mobilePhone=data['mobilePhone'] )
            db.session.add(gp)
            db.session.commit()
        
        gp = GeneralPublic.query.filter_by(userIC=data['userIC']).first()
        gpid = gp.gpid

        # Create the incident instance and add to db
        incident =Incident(address=data['address'], postalCode=data['postalCode'], longtitude=data['longtitude'], 
                            latitude=data['latitude'], assignedBy=data['assignedBy'], gpid=gpid, eid=data['eid'])
        db.session.add(incident)
        db.session.commit()
        return data
          

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}