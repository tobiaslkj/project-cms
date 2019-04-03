from flaskapp import db
from sqlalchemy.orm import relationship
from datetime import datetime
from flaskapp.model.User import User
from sqlalchemy.ext.associationproxy import association_proxy

#For a time being putting all inside the same file first - seperate the class later

#incident has emergencyType M2M relationship table
incident_has_emergencyType = db.Table('incident_has_emergencyType',
    db.Column('eid', db.Integer, db.ForeignKey('emergency_type.eid')),
    db.Column('incidentID', db.Integer, db.ForeignKey('incident.incidentID'))
)
    
class EmergencyType(db.Model):
    __tablename__ = 'emergency_type'
    eid = db.Column(db.Integer, primary_key=True)
    emergencyName = db.Column(db.String(30), unique=True, nullable=False)
    emergencyAssociation = db.relationship('Incident', secondary=incident_has_emergencyType, backref=db.backref('emergency', lazy='dynamic'))
    
    def __init__(self, **kwargs):
        super(EmergencyType, self).__init__(**kwargs)


#request M2M relationship table
incident_request_assistanceType = db.Table('incident_request_assistanceType',
    db.Column('aid', db.Integer, db.ForeignKey('assistance_type.aid')),
    db.Column('incidentID', db.Integer, db.ForeignKey('incident.incidentID'))
)
   
#M2M with incident
class AssistanceType(db.Model):
    __tablename__ = 'assistance_type'
    aid = db.Column(db.Integer, primary_key=True)
    assistanceName = db.Column(db.String(30),unique=True, nullable=False)
    requestAssociation = db.relationship('Incident', secondary=incident_request_assistanceType, backref=db.backref('assist', lazy='dynamic'))
  
    def __init__(self, **kwargs):
        super(AssistanceType, self).__init__(**kwargs)


class GeneralPublic(db.Model):
    _tablename_ = 'general_public'
    gpid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    gp = db.relationship('Incident', backref='GeneralPublic', lazy=True)
    name = db.Column(db.String(40), unique=False, nullable=False)  
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    mobilePhone = db.Column(db.String(8), unique=True, nullable=False)

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
    relevantAgency = db.relationship("RelevantAgency")

   

#M2M with incident
class RelevantAgency(db.Model):
    _tablename_ = 'relevant_agency'
    agencyid = db.Column(db.Integer, primary_key=True)
    agencyName = db.Column(db.String(50), unique=False, nullable=False)
    agencyNumber = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(RelevantAgency, self).__init__(**kwargs)


class Incident(db.Model):
    __tablename__ = 'incident'

    # Attributes
    incidentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postalCode = db.Column(db.String(10), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    
    #Will be computed based by postalCode
    longtitude = db.Column(db.String(120), unique=False, nullable=False)
    latitude = db.Column(db.String(120), unique=False, nullable=False)
    
    gpid = db.Column(db.Integer, db.ForeignKey('general_public.gpid'))
    timeStamp=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    # Association of proxy incident_assigned_to_relevant_agencies to releevant_agencies
    relevantAgencies = association_proxy('incident_assigned_to_relevant_agencies', 'relevant_agency')

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
    statusTime = db.Column(db.DateTime, primary_key=True, nullable=False, default=datetime.utcnow)
    statusID = db.Column(db.Integer, db.ForeignKey('status.statusID'))
    incidentID = db.Column(db.Integer, db.ForeignKey('incident.incidentID'))
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))

    def __init__(self, **kwargs):
        super(IncidentHasStatus, self).__init__(**kwargs)

