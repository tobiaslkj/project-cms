from flask_restful import Resource, reqparse    
from flaskapp import db
from flaskapp.model.Incident import IncidentAssignedToRelevantAgencies, Incident, IncidentSchema, IncidentHasStatusSchema, Status, RelevantAgencySchema
from flask_jwt_extended import jwt_required, create_access_token
from pprint import pprint
from flask import jsonify, abort
import datetime
import pytz

class IncidentUpdateResource(Resource):
    def get(self, urlpath=None):
        if urlpath is None:
            abort(404)
        # Check if incident ha
        iatra = IncidentAssignedToRelevantAgencies.query.filter_by(link=urlpath).first()
        if iatra is None:
            return {"msg":"Sorry does not exist"}, 404
        incidentSchema = IncidentSchema()
        statustime_schema = IncidentHasStatusSchema()
        ihss =[]
        for ihs in iatra.incident.incident_has_status:
            data1 = statustime_schema.dump(ihs)
            data1['statusname'] = ihs.status.statusName
            ihss.append(data1)
        
        data = incidentSchema.dump(iatra.incident)
        del data['relevantAgencies']

        rar = iatra.incident.incident_assigned_to_relevant_agencies
        newRelevantAgencies=[]
        for ra in rar:
            newRa = {}
            newRa['relevantagency_id']=ra.relevantAgency.agencyid
            newRa['relevantagency_name']=ra.relevantAgency.agencyName
            newRa['acknowledged_at'] = None if ra.ackTimeStamp is None else ra.ackTimeStamp
            newRa['acknowledged'] = False if ra.ackTimeStamp is None else True
            newRelevantAgencies.append(newRa)
        
        data['relevantAgencies'] = newRelevantAgencies

        del data['statuses']
        data['statuses'] = ihss
        raSchema = RelevantAgencySchema()
        data['current_relevant_agency']=raSchema.dump(iatra.relevantAgency)

        return data

    def post(self, urlpath=None):
        if urlpath is None:
            abort(404)
        iatra = IncidentAssignedToRelevantAgencies.query.filter_by(link=urlpath).first()
        if iatra is None:
            return {"msg":"Sorry does not exist"}, 404
        
        # Check if incident has any status beyond ongoing or end status
        # pending status will not have a link and thuse cannot exceed the preivous if statement
        for s in iatra.incident.statuses:
            if s.statusID is (3 or 4 or 5): 
                return {"msg":"Unable to change status"},400

        # filtered
        iatra.ackTimeStamp = datetime.datetime.now(pytz.timezone('Asia/Singapore'))
        
        result = IncidentAssignedToRelevantAgencies.query.filter(IncidentAssignedToRelevantAgencies.incidentID==iatra.incidentID).filter(IncidentAssignedToRelevantAgencies.ackTimeStamp.isnot(None)).all()
        if len(result) is len(iatra.incident.relevantAgencies):
            s = Status.query.get(3)
            iatra.incident.statuses.append(s)

        db.session.add(iatra)
        db.session.commit()

        return {"msg":"Incident has been updated"},200