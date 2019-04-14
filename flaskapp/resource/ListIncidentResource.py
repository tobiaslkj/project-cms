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
        statusDictQuery = Status.query.all()
        statusDict = {}
        for s in statusDictQuery:
            statusDict[s.statusName] = s.statusID

        if data['status'] not in statusDict.keys() and data['status'].lower() != 'All'.lower():
            return {"msg":"please input a valid status"},400

       # Return List of incidents 
       # Either Ongoing, Pending or All status in Asc(oldest->latest) or Desc order(latest->oldest)
        # if(data['order'] == 'Asc'):
        #     incidentList = Incident.query.all()
        # elif(data['order'] =='Desc'):
        #     incidentList = Incident.query.order_by(Incident.incidentID.desc()).all()
                
        # call Schema class constructors
        incident_schema = IncidentSchema()
        if data['status'].lower() == "All".lower():
            queryObject = Incident.query
        else:
            queryObject = IncidentHasStatus.query.filter(IncidentHasStatus.statusID==statusDict[data['status']])

        if data['order'].lower()=='Desc'.lower():
            if data['status'].lower() == "All".lower():
                queryObject = queryObject.order_by(Incident.incidentID.desc())
            else:
                queryObject = queryObject.order_by(IncidentHasStatus.incidentID.desc())

        result = queryObject.all()
        
        il = []
        # Filtering and structuring
        if data['status'].lower() != "All".lower():
            for ihs in result:
                if ihs.incident.statuses[len(ihs.incident.statuses)-1].statusID == statusDict[data['status']]:
                    incidentdict = {}
                    incidentdict['type']="Feature"
                    incidentdict['geometry']={ "type":"Point", "coordinates":[ihs.incident.longtitude,ihs.incident.latitude] }
                    incidentdict['properties'] = incident_schema.dump(ihs.incident)
                    il.append(incidentdict)
        else:
            for ihs in result:
                incidentdict = {}
                incidentdict['type']="Feature"
                incidentdict['geometry']={ "type":"Point", "coordinates":[ihs.longtitude,ihs.latitude] }
                incidentdict['properties'] = incident_schema.dump(ihs)
                il.append(incidentdict)

        
        # count = 0
        # for i in incidentList:
        #     data = {}
        #     for s in i.statuses:
        #         if(data['status'] =='Ongoing') and (s.statusName=='Ongoing'): # ongoing incident
        #             if len(i.statuses) is 1  or 2: # if incident has 1 status(for opCreate) 2(for gpCreate) statuses, then it must be Ongoing
        #                 il.append(i)
        #                 count = count+1
        #         elif(data['status'] =='Pending') and (s.statusName=='Pending'): # pending incident
        #             if len(i.statuses) is 1: # if incident has 1 status, then it must be pending.
        #                 il.append(i)
        #                 count = count+1
        #     if (data['status'] == 'All'): # get all incident
        #         statusNo = len(i.statuses) # get the latest status of each incident (for verifying)
        #         currentStatus = i.statuses[statusNo-1] 
        #         il.append(i) 
        #         count = count+1

        # data = incident_schema.dump(il, many=True)
        return {"data":il, "count":len(il)}