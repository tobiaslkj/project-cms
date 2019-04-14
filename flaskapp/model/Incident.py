from flaskapp import db
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from flaskapp.model.User import User
from flaskapp.model.Operator import *
from sqlalchemy.ext.associationproxy import association_proxy
# from flaskapp import mamake
from marshmallow import fields, Schema

#For a time being putting all inside the same file first - seperate the class later

def sgtimestampnow():
    return datetime.now(pytz.timezone('Asia/Singapore'))

#incident has emergencyType M2M relationship table
incident_has_emergencyType = db.Table('incident_has_emergencyType',
    db.Column('eid', db.Integer, db.ForeignKey('emergency_type.eid')),
    db.Column('incidentID', db.Integer, db.ForeignKey('incident.incidentID'))
)
    
class EmergencyType(db.Model):
    __tablename__ = 'emergency_type'
    
    eid = db.Column(db.Integer, primary_key=True)
    emergencyName = db.Column(db.String(30), unique=True, nullable=False)

    
    def __init__(self, **kwargs):
        super(EmergencyType, self).__init__(**kwargs)


#request M2M relationship table
incident_request_assistanceType = db.Table('incident_request_assistanceType',
    #db.metadata.reflect(engine=engine),
    db.Column('aid', db.Integer, db.ForeignKey('assistance_type.aid')),
    db.Column('incidentID', db.Integer, db.ForeignKey('incident.incidentID'))
)
   
#M2M with incident
class AssistanceType(db.Model):
    __tablename__ = 'assistance_type'
    aid = db.Column(db.Integer, primary_key=True)
    assistanceName = db.Column(db.String(30),unique=True, nullable=False)
   
    def __init__(self, **kwargs):
        super(AssistanceType, self).__init__(**kwargs)


class GeneralPublic(db.Model):
    _tablename_ = 'general_public'
    gpid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    gp = db.relationship('Incident', backref='GeneralPublic', lazy=True)
    name = db.Column(db.String(40), unique=False, nullable=False)  
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    mobilePhone = db.Column(db.String(8), unique=False, nullable=False)
    

    def __init__(self, **kwargs):
        super(GeneralPublic, self).__init__(**kwargs)


class IncidentAssignedToRelevantAgencies(db.Model):
    _tablename_ = "incident_assigned_to_relevant_agencies"

    # Attributes
    agency_id = db.Column(db.Integer, db.ForeignKey('relevant_agency.agencyid'), primary_key=True)
    incidentID = db.Column(db.Integer, db.ForeignKey('incident.incidentID'), primary_key=True)
    link = db.Column(db.String(255))
    ackTimeStamp = db.Column(db.DateTime)

    # Relationships
    incident = db.relationship('Incident', backref=db.backref("incident_assigned_to_relevant_agencies", cascade="all, delete-orphan"))
    relevantAgency = db.relationship("RelevantAgency", backref=db.backref("relevant_agency"))

   

#M2M with incident
class RelevantAgency(db.Model):
    _tablename_ = 'relevant_agency'
    agencyid = db.Column(db.Integer, primary_key=True)
    agencyName = db.Column(db.String(50), unique=False, nullable=False)
    agencyNumber = db.Column(db.Integer, unique=True, nullable=False)
    #assignAssociation = db.relationship('Incident', secondary=incident_assign_to_relevantAgencies, backref=db.backref('agency', lazy='joined'))

    def __init__(self, **kwargs):
        super(RelevantAgency, self).__init__(**kwargs)

# class IncidentSchema(Schema):
#     class Meta:
#         #fields to be exposed into json
#         fields = ("incidentID", "postalCode", "address", "description","longtitude", "latitude", "gpid","operatorID")
        
class StatusSchema(Schema):
    statusID = fields.Int()
    statusName = fields.Str()

class IncidentHasStatusSchema(Schema):
    statusTime = fields.DateTime()
    statusID = fields.Int()
    statusName = fields.Nested(StatusSchema, only=["statusName"])

class IncidentHasStatusSchema2(Schema):
    statusTime = fields.DateTime()
    #statusID = fields.Int()
    statusName = fields.Str()
  
class GeneralPublicSchema(Schema):
    gpid = fields.Int()
    name = fields.Str()
    userIC = fields.Str()
    mobilePhone = fields.Int()

class assistanceTypeSchema(Schema):
    #aid = fields.Int()
    assistanceName = fields.Str()
    
class RelevantAgencySchema(Schema):
    #agencyid = fields.Int()
    agencyName = fields.Str()
    agencyNumber = fields.Int()

class EmergencyTypeSchema(Schema):
    #eid = fields.Int()
    emergencyName = fields.Str()

class IncidentSchema(Schema):    
    incidentID = fields.Int()
    postalCode = fields.Str()
    address = fields.Str()
    description = fields.Str()
    operatorID = fields.Int()
    timeStamp = fields.DateTime()
    longtitude = fields.Str()
    latitude = fields.Str()
    reportedUser = fields.Nested(GeneralPublicSchema)
    emergencyType = fields.List(fields.Nested(EmergencyTypeSchema))
    assistanceType = fields.List(fields.Nested(assistanceTypeSchema))
    relevantAgencies = fields.List(fields.Nested(RelevantAgencySchema))
    status = fields.List(fields.Nested(IncidentHasStatusSchema))
    statuses = fields.List(fields.Nested(IncidentHasStatusSchema2))

    

class Incident(db.Model):
    __tablename__ = 'incident'

    # Attributes
    incidentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postalCode = db.Column(db.String(10), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    
    #Will be computed based by address entered
    longtitude = db.Column(db.String(120), unique=False, nullable=False)
    latitude = db.Column(db.String(120), unique=False, nullable=False)
    
    gpid = db.Column(db.Integer, db.ForeignKey('general_public.gpid'))
    operatorID = db.Column(db.Integer, db.ForeignKey('operator.operatorid'))
    timeStamp=db.Column(db.DateTime, nullable=False, default=sgtimestampnow)

    # Relationships
    # Association of proxy incident_assigned_to_relevant_agencies to releevant_agencies
    emergencyType = db.relationship("EmergencyType", secondary=incident_has_emergencyType, backref="incidents")
    assistanceType = db.relationship("AssistanceType", secondary=incident_request_assistanceType, backref="incidents")
    relevantAgencies = association_proxy('incident_assigned_to_relevant_agencies', 'relevantAgency',creator=lambda relevantAgency: IncidentAssignedToRelevantAgencies(relevantAgency=relevantAgency))
    operator = relationship("Operator", backref="incidents")
    reportedUser = relationship("GeneralPublic", backref="reportedIncident")
    # To access list of statues from incident, use incidentInstance.statues. Return a list of status objects
    # to access derived table, from incident table use incidentInstance.incident_has_status or statusInstance.incidents
    statuses = association_proxy('incident_has_status', 'status',creator=lambda status: IncidentHasStatus(status=status))

    def __init__(self, **kwargs):
        super(Incident, self).__init__(**kwargs)
        

class Status(db.Model):
    __tablename__= 'status'
    statusID = db.Column(db.Integer, primary_key=True)
    statusName = db.Column(db.String(20), nullable=False)

    def __init__(self, **kwargs):
        super(Status, self).__init__(**kwargs)

class IncidentHasStatus(db.Model):
    __tablename__ = 'incident_has_status'
    statusTime = db.Column(db.DateTime, primary_key=True, nullable=False, default=sgtimestampnow)
    statusID = db.Column(db.Integer, db.ForeignKey('status.statusID'))
    incidentID = db.Column(db.Integer, db.ForeignKey('incident.incidentID'))

    # Relationships
    incident = db.relationship('Incident', backref=db.backref("incident_has_status", cascade="all, delete-orphan"))
    status = db.relationship("Status", backref=db.backref("incidents"))
    

    def __init__(self, **kwargs):
        super(IncidentHasStatus, self).__init__(**kwargs)

