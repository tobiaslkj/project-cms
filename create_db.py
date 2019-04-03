# This file helps to create the relevant tables in the database
# The schema follow as what is defined in the Model classses in ./models folder
# To add a new schema, the model class should import db from flaskapp and extends from it.

# load the database environment variables
from dotenv import load_dotenv
load_dotenv()
from flaskapp import db


from flaskapp.model import *
from flaskapp.model.Incident import *

#give front end all the emergencyType, assistanceType, Relevant Agencies
db.create_all()
emergencyType1 = EmergencyType(eid=1, emergencyName="Fire")
emergencyType2 = EmergencyType(eid=2, emergencyName="Flood")
emergencyType3 = EmergencyType(eid=3, emergencyName="Earthquake")
emergencyType4 = EmergencyType(eid=4, emergencyName="Gas Leak")
emergencyType5 = EmergencyType(eid=5, emergencyName="Drought")
emergencyType6 = EmergencyType(eid=6, emergencyName="Terrorist")
db.session.add(emergencyType1)
db.session.add(emergencyType2)
db.session.add(emergencyType3)
db.session.add(emergencyType4)
db.session.add(emergencyType5)
db.session.add(emergencyType6)

assistanceType1 = AssistanceType(aid=1, assistanceName="Emergency Ambulance")
assistanceType2 = AssistanceType(aid=2, assistanceName="Rescue and Evacuation")
assistanceType3 = AssistanceType(aid=3, assistanceName="Fire Fighting")
assistanceType4 = AssistanceType(aid=4, assistanceName="Gas Leak Control")
db.session.add(assistanceType1)
db.session.add(assistanceType2)
db.session.add(assistanceType3)
db.session.add(assistanceType4)

relevantAgencies1 = RelevantAgency(agencyid=1, agencyName="Singapore Civil Defence Force", agencyNumber=999)
relevantAgencies2 = RelevantAgency(agencyid=2, agencyName="Hospital", agencyNumber=995)
relevantAgencies3 = RelevantAgency(agencyid=3, agencyName="Singapore Power", agencyNumber=62222333)
db.session.add(relevantAgencies1)
db.session.add(relevantAgencies2)
db.session.add(relevantAgencies3)

status1 = Status(statusID=1, statusName="Pending") #give front end the next stage status
status2 = Status(statusID=2, statusName="Ongoing")
status3 = Status(statusID=3, statusName="Resolved")
status4 = Status(statusID=4, statusName="Rejected")
status5 = Status(statusID=5, statusName="Deleted")
db.session.add(status1)
db.session.add(status2)
db.session.add(status3)
db.session.add(status4)
db.session.add(status5)


db.session.commit()



