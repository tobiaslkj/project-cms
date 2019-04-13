from flask_restful import Resource, reqparse    
from flaskapp import db
from flaskapp.model.Incident import IncidentAssignedToRelevantAgencies, Incident, IncidentSchema, IncidentHasStatusSchema
from flask_jwt_extended import jwt_required, create_access_token
from pprint import pprint
from flask import jsonify, abort

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
        data['status'] = ihss

        return data
