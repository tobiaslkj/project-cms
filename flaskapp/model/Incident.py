from flaskapp import db
from sqlalchemy.orm import relationship

#For a time being putting all inside the same file first - seperate the class later

class EmergencyType(db.Model):
    __tablename__ = 'EmergencyType'
    eid = db.Column(db.Integer, primary_key=True)
    emergencyType = db.Column(db.String(30), unique=True, nullable=False)
    emerType = db.relationship('Incident', backref='EmergencyType', lazy=True)

    def __init__(self, **kwargs):
        super(EmergencyType, self).__init__(**kwargs)


# #M2M with incident
# class AssistanceType(db.Model):
#     __tablename__ = 'AssistanceType'
#     aid = db.Column(db.Integer, primary_key=True)
#     def __init__(self, assistType):
#         super(AssistanceType, self).__init__(assistType)


class GeneralPublic(db.Model):
    _tablename_ = 'general_public'
    gpid = db.Column(db.Integer, primary_key=True)
    gp = db.relationship('Incident', backref='general_public', lazy=True)
    name = db.Column(db.String(40), unique=False, nullable=False)  
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    mobilePhone = db.Column(db.String(8), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(GeneralPublic, self).__init__(**kwargs)

# #M2M with incident
# class RelevantAgencies(db.Model):
#     _tablename_ = 'RelevantAgencies'
#     agencyid = db.Column(db.Integer, primary_key=True)
#     agencyName = db.Column(db.String(50), unique=False, nullable=False)

#     def __init__(self, **kwargs):
#         super(RelevantAgencies, self).__init__(**kwargs)


class Incident(db.Model):
    __tablename__ = 'Incident'
    incidentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postalCode = db.Column(db.String(10), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    
    #Will be computed based by postalCode
    longtitude = db.Column(db.String(120), unique=False, nullable=False)
    latitude = db.Column(db.String(120), unique=False, nullable=False)
    
    #Have to change assignedBy, hardcoding it now
    assignedBy = db.Column(db.String(50), unique=False, nullable=False)
    
    eid = db.Column(db.Integer, db.ForeignKey('EmergencyType.eid'))
    gpid = db.Column(db.Integer, db.ForeignKey('general_public.gpid'))

    def __init__(self, **kwargs):
        super(Incident, self).__init__(**kwargs)


