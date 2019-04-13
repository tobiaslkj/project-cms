from flask_restful import Resource, reqparse
from flaskapp import db
from flask import Flask, jsonify
from flaskapp.model.Incident import *
from flaskapp.model.Operator import *
from datetime import datetime
import requests, json
from flaskapp.utility.WeblinkGenerator import generateURL
from flaskapp.access_control import operator_required
from flask_jwt_extended import get_jwt_claims
from flaskapp.utility.SMSSender import send_sms

#Operator create incident from user call in, status = "Ongoing"
#GP create incident set gp_create = True, has no status
class GPIncidentResource(Resource): 
    def get(self):
        return {'Incident': 'world' }

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('address', help='Address field cannot be blank', required = True)
        parser.add_argument('name', help='name cannot be blank',required=True)
        parser.add_argument('userIC', help='userIC cannot be blank',required=True)
        parser.add_argument('mobilePhone', help='mobilePhone cannot be blank', required=True)
        parser.add_argument('description', help='description cannot be blank',required=True)
        parser.add_argument('assistance_type', action='append', help='This field cannot be blank', required=False)
        parser.add_argument('emergency_type',action='append', help='This field cannot be blank',required=True)
        data = parser.parse_args()

        #check if the gp exist in database
        # if gp exists, update gp information
        # if gp information does not exist, create as new one
        gp = GeneralPublic.query.filter_by(userIC=data['userIC']).first()
        if(gp is None):
            gp = GeneralPublic(name=data['name'], userIC=data['userIC'], mobilePhone=data['mobilePhone'] )
        else:
            gp.name = data['name']
            gp.mobilePhone = data['mobilePhone']

        # get the full address lat, long and postalCode
        address = data['address']
        oneMap = "https://developers.onemap.sg/commonapi/search?searchVal=%s&returnGeom=Y&getAddrDetails=Y" %(address)
        # send get request and save as response object
        response = requests.get(oneMap)

        # extract result in json format
        result = response.json()

        latitude = result['results'][0]['LATITUDE']
        longtitude = result['results'][0]['LONGTITUDE']
        postalCode = result['results'][0]['POSTAL']
        address = result['results'][0]['ADDRESS']

        # Create the incident instance and add to db
        incident =Incident(address=address, postalCode=postalCode, longtitude=longtitude, 
                        latitude=latitude, description=data['description'])
        incident.reportedUser = gp
        db.session.add(incident)
        db.session.commit()

        #update incident_request_assistanceType table
        if (data['assistance_type']is not None):
            for x in data['assistance_type']:
                aid = AssistanceType.query.filter_by(aid=x).first()
                incident.assistanceType.append(aid)
                db.session.add(incident)

        #update incident_has_emergencyType table  
        for y in data['emergency_type']:
            eid = EmergencyType.query.filter_by(eid=y).first()
            incident.emergencyType.append(eid)
            db.session.add(incident)

        #get the statusID of Ongoing from status table
        status = Status.query.filter_by(statusName="Pending").first()
        print(status)
        statusID = status.statusID

        #update incident_has_status table
        status = IncidentHasStatus(statusID=statusID,incidentID=incident.incidentID)
        db.session.add(status)

        # Store the current session data into database.
        db.session.commit()
        return {"msg":"Incident created."},201

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}