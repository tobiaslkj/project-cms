from flask_restful import Resource, reqparse
from flaskapp import db
from flask import Flask, jsonify, abort
from flaskapp.model.Incident import *
from flaskapp.model.Operator import *
from datetime import datetime
import requests, json
import pprint
from flaskapp.utility.WeblinkGenerator import generateURL
from flaskapp.access_control import operator_required
from flask_jwt_extended import get_jwt_claims
from flaskapp.utility.SMSSender import send_sms
from pprint import pprint

#Operator create incident from user call in, status = "Ongoing"
#GP create incident set gp_create = True, has no status
class IncidentResource(Resource): 
    def get(self,incident_id):
        
        i = db.session.query(Incident).filter(Incident.incidentID==incident_id).first()
        incident_schema = IncidentSchema()
        
        statustime_schema = IncidentHasStatusSchema()
        ihss =[]
        for ihs in i.incident_has_status:
            data1 = statustime_schema.dump(ihs)
            data1['statusname'] = ihs.status.statusName
            ihss.append(data1)
            
        
        data = incident_schema.dump(i)
        data['status'] = ihss
        return data

    
        

    @operator_required
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('address', help='Address field cannot be blank', required = True)
        parser.add_argument('name', help='name cannot be blank',required=True)
        parser.add_argument('userIC', help='userIC cannot be blank',required=True)
        parser.add_argument('description', help='description cannot be blank',required=True)
        parser.add_argument('mobilePhone', help='mobilePhone cannot be blank', required=True)
        parser.add_argument('assistance_type', action='append', help='This field cannot be blank', required=True)
        parser.add_argument('emergency_type',action='append', help='This field cannot be blank',required=True)
        parser.add_argument('relevant_agencies',action='append', help='This field cannot be blank',required=True)
        data = parser.parse_args()
            
        # If gp_create = False, it is operator create incident
        # Check if a GP exist in database
        if(GeneralPublic.query.filter_by(userIC=data['userIC']).first() is None):
            gp = GeneralPublic(name=data['name'], userIC=data['userIC'], mobilePhone=data['mobilePhone'])
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

        latitude = result['results'][0]['LATITUDE']
        longtitude = result['results'][0]['LONGTITUDE']
        postalCode = result['results'][0]['POSTAL']
        address = result['results'][0]['ADDRESS']

        #get the operator id
        operatorInfo = get_jwt_claims()
        operatorid = operatorInfo['operatorid']

        # Create the incident instance and add to db
        incident =Incident(address=address, postalCode=postalCode, longtitude=longtitude, 
                            latitude=latitude, gpid=gpid, description=data['description'], operatorID=operatorid)
        db.session.add(incident)
        db.session.commit()

        #update incident_request_assistanceType table
        for x in data['assistance_type']:
            aid = AssistanceType.query.filter_by(aid=x).first()
            incident.assistanceType.append(aid)
            db.session.add(incident)

        #update incident_has_emergencyType table  
        for y in data['emergency_type']:
            eid = EmergencyType.query.filter_by(eid=y).first()
            incident.emergencyType.append(eid)
            db.session.add(incident)

        # Create an instance of the many to many derived table
        # using the incident instance and agencyid instance)
        for z in data['relevant_agencies']:
            randomURL = generateURL()
            agencyid = RelevantAgency.query.filter_by(agencyid=z).first()
            number = f'+65 {agencyid.agencyNumber}' 
            send_sms(number, f'http://tobiaslkj.com/{randomURL}')
            assignment = IncidentAssignedToRelevantAgencies(incident=incident, relevantAgency=agencyid, link=randomURL)
            db.session.add(assignment)
        
        # Store the current session data into database.
        db.session.commit()

        #get the statusID of Ongoing from status table
        status = Status.query.filter_by(statusName="Ongoing").first()
        statusID = status.statusID

        #update incident_has_status table
        status = IncidentHasStatus(statusID=statusID,incidentID=incident.incidentID)
        db.session.add(status)
        db.session.commit()


        return {"msg":"Incident created."},201
          
    @operator_required
    def patch(self, incidentID=None):
        if incidentID is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('relevant_agencies',action='append', help='This field cannot be blank',required=True)
        data = parser.parse_args()

        ## ensure that the array is not zerio legnth 
        if(len(data['relevant_agencies']) is 0):
            return {"error":"should not have 0 relevant agencies"},422
        
        i = Incident.query.get(incidentID)
        if i is None or len(i.statuses) is not 1: # status should only have 1 length, not length of 1 means its not in pending state
            return {"msg":"Incident not found"},404

        operatorInfo = get_jwt_claims()
        o = Operator.query.get(operatorInfo['operatorid'])
        i.operator = o
        
        # attached relevant agencies to this incidnet
        for raid in data['relevant_agencies']:
            randomURL = generateURL()
            ra = RelevantAgency.query.get(raid)
            number = f'+65 {ra.agencyNumber}' 
            send_sms(number, f'http://tobiaslkj.com/{randomURL}')
            iatra = IncidentAssignedToRelevantAgencies(incident=i, relevantAgency=ra, link=randomURL)
            db.session.add(iatra)

        #Add the relationship of who approved the incident
        db.session.add(i)

        # add a new row of incident has status
        s = Status.query.get(2) # id 2 is status pending
        ihs = IncidentHasStatus(incident = i, status = s)
        db.session.add(ihs)
        db.session.commit()
        
        return {"msg":"Incident status has been approved"},201

    def delete(self):
        return {"wow":"deteled"}