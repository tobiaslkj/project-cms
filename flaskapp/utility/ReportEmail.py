from flask import Flask
from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.utility.EmailSender import send_email
from flaskapp.model.Incident import *
from datetime import datetime


def findReportContent():
    resolved = Status.query.filter_by(statusName='Resolved').first()
    resolvedID = resolved.statusID
    numresolvedIncidents = Incident.query.filter_by(statuses=resolvedID).count()
    
    ongoing = Status.query.filter_by(statusName='Ongoing').first()
    ongoingID = ongoing.statusID
    numongoingIncidents = Incident.query.filter_by(statuses=ongoingID).count()
    
    return {"numOfResolvedIncident":numresolvedIncidents, "numOfOngoingIncident":numongoingIncidents}
    