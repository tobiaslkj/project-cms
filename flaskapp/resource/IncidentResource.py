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


#General Public create incident, status is Pending
#!!! is this the GP post from our website or is the operator submit the GP incident into the system?
# if is GP post from our website: dont have relevant agencies, dont have operatorid in incident_has_status table and status is pending
# if is operator submit the GP incident, den status should be ongoing cos alr approved and not pending
class IncidentResource(Resource): 
    def get(self):
        return {'Incident': 'world' }

    @operator_required
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('address', help='Address field cannot be blank', required = True)
        parser.add_argument('name', help='name cannot be blank',required=True)
        parser.add_argument('userIC', help='userIC cannot be blank',required=True)
        parser.add_argument('mobilePhone', help='mobilePhone cannot be blank', required=True)
        parser.add_argument('assistance_type', action='append', help='This field cannot be blank', required=True)
        parser.add_argument('emergency_type',action='append', help='This field cannot be blank',required=True)
        parser.add_argument('relevant_agencies',action='append', help='This field cannot be blank',required=True)
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



        # Create the incident instance and add to db
        incident =Incident(address=address, postalCode=postalCode, longtitude=longtitude, 
                            latitude=latitude, gpid=gpid)
        db.session.add(incident)
        db.session.commit()

        #update incident_request_assistanceType table
        for x in data['assistance_type']:
            aid = AssistanceType.query.filter_by(aid=x).first()
            incident.assist.append(aid)
            db.session.add(incident)

        #update incident_has_emergencyType table  
        for y in data['emergency_type']:
            eid = EmergencyType.query.filter_by(eid=y).first()
            incident.emergency.append(eid)
            db.session.add(incident)

        # Create an instance of the many to many derived table
        # using the incident instance and agencyid instance)
        for z in data['relevant_agencies']:
            randomURL = generateURL()
            agencyid = RelevantAgency.query.filter_by(agencyid=z).first()
            assignment = IncidentAssignedToRelevantAgencies(incident=incident, relevantAgency=agencyid, link=randomURL)
            db.session.add(assignment)

        # Store the current session data into database.
        db.session.commit()

        #get the statusID of Ongoing from status table
        status = Status.query.filter_by(statusName="Ongoing").first()
        statusID = status.statusID

        #get the operator id
        operatorInfo = get_jwt_claims()
        operatorid = operatorInfo['operatorid']

        #update incident_has_status table
        status = IncidentHasStatus(statusID=statusID,incidentID=incident.incidentID,operatorid=operatorid)
        db.session.add(status)
        db.session.commit()


        return data
          

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}