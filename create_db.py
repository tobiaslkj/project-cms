# This file helps to create the relevant tables in the database
# The schema follow as what is defined in the Model classses in ./models folder
# To add a new schema, the model class should import db from flaskapp and extends from it.

# load the database environment variables
from dotenv import load_dotenv
load_dotenv()
from flaskapp import db


from flaskapp.model import *
from flaskapp.model.Incident import *

db.create_all()
emergencyType1 = EmergencyType(eid=1, emergType="Fire")
emergencyType2 = EmergencyType(eid=2, emergType="Flood")
emergencyType3 = EmergencyType(eid=3, emergType="Earthquake")
emergencyType4 = EmergencyType(eid=4, emergType="Gas Leak")
emergencyType5 = EmergencyType(eid=5, emergType="Drought")
emergencyType6 = EmergencyType(eid=6, emergType="Terrorist")
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

db.session.commit()



