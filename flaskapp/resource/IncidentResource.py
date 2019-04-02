from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.Incident import Incident
from flaskapp.model.Incident import GeneralPublic
from datetime import datetime
import requests, json

class IncidentResource(Resource):
    def get(self):
        return {'Incident': 'world' }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('address', help='Address field cannot be blank', required = True)
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
    
        
        # get the full address lat, long and postalCode
        address = data['address']
        oneMap = "https://developers.onemap.sg/commonapi/search?searchVal=%s&returnGeom=Y&getAddrDetails=Y" %(address)
        # send get request and save as response object
        response = requests.get(oneMap)

        # extract result in json format
        result = response.json()
        print(response.content)

        latitude = result['results'][0]['LATITUDE']
        longtitude = result['results'][0]['LONGTITUDE']
        postalCode = result['results'][0]['POSTAL']
        address = result['results'][0]['ADDRESS']

        print(latitude, longtitude, postalCode, address)


        # Create the incident instance and add to db
        incident =Incident(address=address, postalCode=postalCode, longtitude=longtitude, 
                            latitude=latitude, assignedBy=data['assignedBy'], gpid=gpid, eid=data['eid'])
        db.session.add(incident)
        db.session.commit()
        return data
          

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}