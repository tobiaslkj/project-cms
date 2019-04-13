from flask_restful import Resource, reqparse
from flaskapp import db
from flask import Flask, jsonify
from flaskapp.model.Incident import *
from flaskapp.model.Operator import *
from datetime import datetime 
from sqlalchemy import desc
import requests, json
from pprint import pprint


class ListIncidentResource(Resource): 
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('status', help='status field cannot be blank', required = True)
        parser.add_argument('order', help='order field cannot be blank', required = True)
        data = parser.parse_args()

       # Return List of incidents 
       # Either Ongoing, Pending or All status in Asc(oldest->latest) or Desc order(latest->oldest)
        if(data['order'] == 'Asc'):
                incidentList = Incident.query.all()
        elif(data['order'] =='Desc'):
                incidentList = Incident.query.order_by(Incident.incidentID.desc()).all()

        # call Schema class constructors
        incident_schema = IncidentSchema(many=True)
        status_schema = IncidentHasStatusSchema()
        
        il = []
        ihsl =[]
        for i in incidentList:
            for s in i.statuses:
                if(data['status'] =='Ongoing') and (s.statusName=='Ongoing'): # ongoing incident
                    if len(i.statuses) is 1  or 2: # if incident has 1 status(for opCreate) 2(for gpCreate) statuses, then it must be Ongoing
                        il.append(i)
                elif(data['status'] =='Pending') and (s.statusName=='Pending'): # pending incident
                    if len(i.statuses) is 1: # if incident has 1 status, then it must be pending.
                        il.append(i)
            if (data['status'] == 'All'): # get all incident
                statusNo = len(i.statuses) # get the latest status of each incident (for verifying purposes)
                currentStatus = i.statuses[statusNo-1] 
                il.append(i) 

        
        data = incident_schema.dump(il, many=True)   
        
        return data, 200