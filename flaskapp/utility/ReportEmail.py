from flask import Flask
from flask_restful import Resource, reqparse
# from flaskapp import db
from flaskapp.utility.EmailSender import send_email
from flaskapp.model.Incident import *
from datetime import datetime
from sqlalchemy import func


def findReportContent():
    # ongoing statusID = 2, resolved statusID = 3
    # search only the incident table, find the statuses see if ==2/3 
    # create an ongoing and resolved list, add in the fulfilled incident
    totIncidents = Incident.query.all()
    resolvedIncident = []
    ongoingIncident =[] 
    
    for i in totIncidents:
        if len(i.statuses)==0:
            continue
        elif i.statuses[len(i.statuses)-1].statusID==3:
            resolvedIncident.append(i)
        elif i.statuses[len(i.statuses)-1].statusID==2:
            ongoingIncident.append(i)
   
    numOfOngoingIncident = len(ongoingIncident)
    numOfResolvedIncident = len(resolvedIncident)
  
    return {"numOfResolvedIncident":numOfResolvedIncident, "numOfOngoingIncident":numOfOngoingIncident}
    
    