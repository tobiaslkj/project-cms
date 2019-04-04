from flask_restful import Resource, reqparse
from flaskapp import db
from flask import Flask, request, json, jsonify
from flaskapp.model.Incident import *
from flaskapp.model.Incident import GeneralPublic

from datetime import datetime
import requests

class IncidentResource(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('status', help='status field cannot be blank', required = True)
        parser.add_argument('order', help='order field cannot be blank', required = True)
        data = parser.parse_args()

       # return incident of pending status and asc date order
        if(data['status'] == 'Ongoing' and  data['order'] == 'Asc'):
            for i, h, s in db.session.query(Incident, IncidentHasStatus, Status).\
                filter(Status.statusName=='Ongoing').\
                filter(Incident.incidentID==IncidentHasStatus.incidentID).\
                filter(IncidentHasStatus.statusID==Status.statusID).order_by(Incident.incidentID).all():
                aType = db.session.query(AssistanceType).filter(AssistanceType.requestAssociation.any(Incident.incidentID==i.incidentID)).all()
                eType = db.session.query(EmergencyType).filter(EmergencyType.emergencyAssociation.any(Incident.incidentID==i.incidentID)).all()
                relevantAgent = db.session.query(RelevantAgencies).filter(RelevantAgencies.assignAssociation.any(Incident.incidentID==i.incidentID)).all()
                

            
        elif (data['status'] == 'Ongoing' and  data['order'] == 'Desc'):
             for i, h, s in db.session.query(Incident, IncidentHasStatus, Status).\
                filter(Status.statusName=='Ongoing').\
                filter(Incident.incidentID==IncidentHasStatus.incidentID).\
                filter(IncidentHasStatus.statusID==Status.statusID).order_by(Incident.incidentID.desc()).all():
                aType = db.session.query(AssistanceType).filter(AssistanceType.requestAssociation.any(Incident.incidentID==i.incidentID)).all()
                eType = db.session.query(EmergencyType).filter(EmergencyType.emergencyAssociation.any(Incident.incidentID==i.incidentID)).all()
                relevantAgent = db.session.query(RelevantAgencies).filter(RelevantAgencies.assignAssociation.any(Incident.incidentID==i.incidentID)).all()


            
        
            # incident = db.session.query(Incident).join(IncidentHasStatus).join(Status).filter(Status.statusName=='Pending').order_by(Incident.incidentID).all()
            # for i in incident:
            #     print(i.incidentID, i.postalCode, i.address, i.longtitude, i.latitude, i.gpid, i.timeStamp)
            #     incident_status = db.session.query(IncidentHasStatus).join(Incident).filter(IncidentHasStatus.incidentID==i.incidentID)
            #     for s in incident_status:
            #         print(s.statusTime, s.statusID, s.incidentID, s.uid)

        return data

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
            db.session.commit()

        #update incident_has_emergencyType table  
        for y in data['emergency_type']:
            eid = EmergencyType.query.filter_by(eid=y).first()
            incident.emergency.append(eid)
            db.session.add(incident)
            db.session.commit()

        #update incident_assign_to_relevantAgencies table    
        for z in data['relevant_agencies']:
            agencyid = RelevantAgencies.query.filter_by(agencyid=z).first()
            incident.agency.append(agencyid)
            db.session.add(incident)
            db.session.commit()

        return data
          

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}