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
class IncidentResource(Resource): 
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('status', help='status field cannot be blank', required = True)
        parser.add_argument('order', help='order field cannot be blank', required = True)
        data = parser.parse_args()

       # return incident of Ongoing status and asc order
        if(data['status'] == 'Ongoing') and  data['order'] == 'Asc':
            for i, h, s in db.session.query(Incident, IncidentHasStatus, Status).\
                filter(Status.statusName=='Ongoing').\
                filter(Incident.incidentID==IncidentHasStatus.incidentID).\
                filter(IncidentHasStatus.statusID==Status.statusID).order_by(Incident.incidentID).all():
                #aType = db.session.query(AssistanceType).filter(AssistanceType.requestAssociation.any(Incident.incidentID==i.incidentID)).all()
                #eType = db.session.query(EmergencyType).filter(EmergencyType.emergencyAssociation.any(Incident.incidentID==i.incidentID)).all()
                print(i.incidentID, i.postalCode, i.address, i.longtitude, i.latitude, i.gpid, i.timeStamp, i.relevantAgencies)
                for ra in i.relevantAgencies:
                    print(ra.agencyid, ra.agencyName)
                for et in i.emergencyType:
                    print(et.eid, et.emergencyName)
                print(h.incidentID, h.statusID, h.statusTime, h.operatorid)
                print(i.__dict__)
                print(h.__dict__)
                print(s.__dict__)
                print(s.statusID, s.statusName)
                #print(eType, aType, relevantAgent)
                # for e in eType:
                #     print(e.eid,e.emergencyName)
                # for a in aType:
                #     print(a.aid,a.assistanceName)
                # for ra, iar in db.session.query(RelevantAgency, IncidentAssignedToRelevantAgencies).\
                #     filter(RelevantAgency.agencyid==IncidentAssignedToRelevantAgencies.agency_id).filter(IncidentAssignedToRelevantAgencies.incidentID==i.incidentID).all():
                # #relevantAgent = db.session.query(RelevantAgency).filter(RelevantAgency.assignAssociation.any(Incident.incidentID==i.incidentID)).all()
                #     for agent in ra:
                #             print(agent.agencyid, agent.agencyName, agent.agencyNumber)


        #return incident of Ongoing status and desc order  
        elif (data['status'] == 'Ongoing' and  data['order'] == 'Desc'):
             for i, h, s in db.session.query(Incident, IncidentHasStatus, Status).\
                filter(Status.statusName=='Ongoing').\
                filter(Incident.incidentID==IncidentHasStatus.incidentID).\
                filter(IncidentHasStatus.statusID==Status.statusID).order_by(Incident.incidentID.desc()).all():
                aType = db.session.query(AssistanceType).filter(AssistanceType.requestAssociation.any(Incident.incidentID==i.incidentID)).all()
                eType = db.session.query(EmergencyType).filter(EmergencyType.emergencyAssociation.any(Incident.incidentID==i.incidentID)).all()
                #relevantAgent = db.session.query(RelevantAgency).filter(RelevantAgency.assignAssociation.any(Incident.incidentID==i.incidentID)).all()
        
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
                            latitude=latitude, gpid=gpid, description=data['description'])
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

        #get the operator id
        operatorInfo = get_jwt_claims()
        operatorid = operatorInfo['operatorid']

        #update incident_has_status table
        status = IncidentHasStatus(statusID=statusID,incidentID=incident.incidentID,operatorid=operatorid)
        db.session.add(status)
        db.session.commit()


        return {"msg":"Incident created."},201
          

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}