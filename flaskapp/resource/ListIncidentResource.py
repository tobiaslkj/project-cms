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
        parser.add_argument('status',action='append', help='status field cannot be blank', required = True)
        parser.add_argument('order', help='order field cannot be blank', required = True)
        data = parser.parse_args()
        statusDictQuery = Status.query.all()
        statusDict = {}
        for s in statusDictQuery:
            statusDict[s.statusName.lower()] = s.statusID

        statusQuery = []
        for x in data['status']:
            if x.lower() not in statusDict.keys():
                return {"msg":f"{x} is not a valid status"},400
            else:
                statusQuery.append(statusDict[x])

                
        # call Schema class constructors
        incident_schema = IncidentSchema()
        queryObject = Incident.query

        if data['order'].lower()=='Desc'.lower():
            queryObject = queryObject.order_by(Incident.incidentID.desc())

        result = queryObject.all()
        
        il = []
        # Filtering and structuring
        for i in result:
            if i.statuses[len(i.statuses)-1].statusID in statusQuery:
                incidentdict = {}
                incidentdict['type']="Feature"
                incidentdict['geometry']={ "type":"Point", "coordinates":[i.longtitude,i.latitude] }
                incidentdict['properties'] = incident_schema.dump(i)
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