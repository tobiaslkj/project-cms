from flask_restful import Resource, reqparse
from flaskapp import db
from flask import Flask, jsonify, abort
from flaskapp.model.Incident import *
from flaskapp.model.Operator import *
from flaskapp.validate.ValidateIc import *
from datetime import datetime
from flaskapp.utility.WeblinkGenerator import generateURL
from flaskapp.access_control import operator_required
from flask_jwt_extended import get_jwt_claims
from flaskapp.utility.SMSSender import send_sms
from flaskapp.utility.Address import getAddress
from flaskapp.utility.Template import *
from flaskapp.utility.SocialMedia import postToSocialMedia

#Operator create incident from user call in, status = "Ongoing"
#GP create incident set gp_create = True, has no status
class IncidentResource(Resource): 
    def get(self,incident_id=None):
        if incident_id is None:
            abort(404)
        
        i = db.session.query(Incident).filter(Incident.incidentID==incident_id).first()

        if(i is None):
            return {"msg":"Incident not found"},404
        
        incident_schema = IncidentSchema()
        
        statustime_schema = IncidentHasStatusSchema()
        ihss =[]
        for ihs in i.incident_has_status:
            data1 = statustime_schema.dump(ihs)
            data1['statusname'] = ihs.status.statusName
            ihss.append(data1)
        
        data = incident_schema.dump(i)
        data['status'] = ihss
        del data['statuses']
        del data['longtitude']
        del data['latitude']
        return data

    
    @operator_required
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('address', help='Address field cannot be blank', required = True)
        parser.add_argument('name', help='name cannot be blank',required=True)
        parser.add_argument('userIC', help='userIC cannot be blank',required=True)
        parser.add_argument('description', help='description cannot be blank',required=False)
        parser.add_argument('mobilePhone', help='mobilePhone cannot be blank', required=True)
        parser.add_argument('assistance_type', action='append', help='This field cannot be blank', required=True)
        parser.add_argument('emergency_type',action='append', help='This field cannot be blank',required=True)
        parser.add_argument('relevant_agencies',action='append', help='This field cannot be blank',required=True)
        data = parser.parse_args()
        
        #validating if the entered NRIC is valid or not
        validIc = validateNRIC(data['userIC'])
        if (validIc is False):
            return {"msg":"Please enter a valid NRIC"}, 400
        else:
            validatedIc = data['userIC']
            
         
        #check if the gp exist in database
        # if gp exists, update gp information
        # if gp information does not exist, create as new one
        gp = GeneralPublic.query.filter_by(userIC=data['userIC']).first()
        if(gp is None):
            gp = GeneralPublic(name=data['name'], userIC=data['userIC'], mobilePhone=data['mobilePhone'] )
        else:
            gp.name = data['name']
            gp.mobilePhone = data['mobilePhone']
    
        
        # get the full address lat, long and postalCode
        result = getAddress(data['address'])

        latitude = result['latitude']
        longtitude = result['longtitude']
        postalCode = result['postalCode']
        address = result['address']

        #get the operator id
        operatorInfo = get_jwt_claims()
        operatorid = operatorInfo['operatorid']

        # Create the incident instance and add to db
        incident =Incident(address=address, postalCode=postalCode, longtitude=longtitude, 
                            latitude=latitude, description=data['description'], operatorID=operatorid)
        incident.reportedUser = gp
        db.session.add(incident)
        db.session.commit()

        #update incident_request_assistanceType table
        for x in data['assistance_type']:
            aid = AssistanceType.query.filter_by(aid=x).first()
            incident.assistanceType.append(aid)
            db.session.add(incident)

        #update incident_has_emergencyType table  
        for y in data['emergency_type']:
            eid = EmergencyType.query.filter_by(eid=y).first()
            incident.emergencyType.append(eid)
            db.session.add(incident)

        # Create an instance of the many to many derived table
        # using the incident instance and agencyid instance)
        for z in data['relevant_agencies']:
            randomURL = generateURL()
            agencyid = RelevantAgency.query.filter_by(agencyid=z).first()
            number = f'+65 {agencyid.agencyNumber}' 
            send_sms(number, f'http://ec2-54-254-185-54.ap-southeast-1.compute.amazonaws.com/ra/{randomURL}')
            assignment = IncidentAssignedToRelevantAgencies(incident=incident, relevantAgency=agencyid, link=randomURL)
            db.session.add(assignment)
        
        # Store the current session data into database.
        db.session.commit()

        #get the statusID of Ongoing from status table
        status = Status.query.filter_by(statusName="Ongoing").first()
        statusID = status.statusID

        #update incident_has_status table
        status = IncidentHasStatus(statusID=statusID,incidentID=incident.incidentID)
        db.session.add(status)
        db.session.commit()
        
        #if the incident submited is very serious: Earthquake, Terrorist, then send twitter & FB
        # EarthquakeID=3, TerroristID=6
        seriousType = ['3','6']
        enteredType = data['emergency_type']
    
        set1 = set(seriousType)
        set2 = set(enteredType)
        
        intersect = bool(set2.intersection(set1))
        if (intersect is True):
            if '3' in enteredType and '6' not in enteredType:
                # call template for earthquake
                # call fb and twitter api
                message1 = one_emergency_facebook_template.format('Earthquake',data['address'])
                postToSocialMedia(message1,2)
                message2 = one_emergency_twitter_template.format('Earthquake',data['address'])
                postToSocialMedia(message2,1)
                
            
            elif '6' in enteredType and '3' not in enteredType:
                # call template for terrorist
                # call fb and twitter api
                message1 = one_emergency_facebook_template.format('Terrorist Attack',data['address'])
                postToSocialMedia(message1,2)
                message2 = one_emergency_twitter_template.format('Terrorist Attack',data['address'])
                postToSocialMedia(message2,1)
            
            elif '3' in enteredType and '6' in enteredType: 
                # call template for terrorist and earthquake
                # call fb and twitter api
                message1 = two_emergency_facebook_template.format('Earthquake','Terrorist Attack', data['address'])
                postToSocialMedia(message1,2)
                message2 = two_emergency_twitter_template.format('Earthquake','Terrorist Attack', data['address'])
                postToSocialMedia(message2,1)
            

        return {"msg":"Incident created."},201
          
    @operator_required
    def patch(self, incident_id=None):
        if incident_id is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('action', help='This field cannot be blank')
        parser.add_argument('address')
        parser.add_argument('name')
        parser.add_argument('userIC')
        parser.add_argument('description')
        parser.add_argument('mobilePhone')
        parser.add_argument('assistance_type', action='append')
        parser.add_argument('emergency_type',action='append')
        parser.add_argument('relevant_agencies',action='append')
        data = parser.parse_args()

        if(data['action'] not in ['approve','reject']):
            return {"msg":"Please choose a valid action"}, 400
        
        if data['action'] == 'reject':
            i = Incident.query.get(incident_id)
            if len(i.statuses) == 1: # got more status other than pending
                if i.statuses[0].statusID == 1:
                    s = Status.query.get(4)
                    i.statuses.append(s)
                    db.session.add(i)
                    db.session.commit()
                    return {"msg":"Incident has been rejected"},200

            return {"msg":"Unable to reject incident as it is not in pending state"}, 400
        
        dataMustHave = ['address','name','userIC', 'description','mobilePhone','assistance_type','emergency_type', 'relevant_agencies']

        errorMessages={}
        failFlag = 0
        for dmh in dataMustHave:
            if data[dmh] is None:
                failFlag = 1
                errorMessages[dmh]="This field is required"
        
        if failFlag:
            return errorMessages,400
            
        ## ensure that the array is not zero legnth 
        if(len(data['relevant_agencies']) is 0):
            return {"error":"should not have 0 relevant agencies"},400
        
        i = Incident.query.get(incident_id)
        if i is None or len(i.statuses) is not 1: # status should only have 1 length, not length of 1 means its not in pending state
            return {"msg":"Incident not found"},404

        operatorInfo = get_jwt_claims()
        o = Operator.query.get(operatorInfo['operatorid'])
        i.operator = o
        
        gp = GeneralPublic.query.filter_by(userIC = data['userIC']).first()
        if gp is None:
            gp = GeneralPublic(userIC = data['userIC'])
        gp.mobilePhone = data['mobilePhone']
        gp.name = data['name']

        i.reportedUser = gp
        i.description = data['description']

        result = getAddress(data['address'])

        i.latitude = result['latitude']
        i.longtitude = result['longtitude']
        i.postalCode = result['postalCode']
        i.address = result['address']

        i.emergencyType = []
        for y in data['emergency_type']:
            eid = EmergencyType.query.filter_by(eid=y).first()
            i.emergencyType.append(eid)
            db.session.add(i)
        
        #update incident_request_assistanceType table
        i.assistanceType = []
        for x in data['assistance_type']:
            aid = AssistanceType.query.filter_by(aid=x).first()
            i.assistanceType.append(aid)
            db.session.add(i)

        # attached relevant agencies to this incidnet
        for raid in data['relevant_agencies']:
            randomURL = generateURL()
            ra = RelevantAgency.query.get(raid)
            number = f'+65 {ra.agencyNumber}' 
            send_sms(number, f'http://ec2-54-254-185-54.ap-southeast-1.compute.amazonaws.com/ra/{randomURL}')
            iatra = IncidentAssignedToRelevantAgencies(incident=i, relevantAgency=ra, link=randomURL)
            db.session.add(iatra)


        # add a new row of incident has status
        s = Status.query.get(2) # id 2 is status pending
        ihs = IncidentHasStatus(incident = i, status = s)
        db.session.add(ihs)
        db.session.commit()
        
        #post to socialmedia if is terrorist(6) or earthquake(3)
        seriousType = ['3','6']
        enteredType = data['emergency_type']
    
        set1 = set(seriousType)
        set2 = set(enteredType)
        intersect = bool(set2.intersection(set1))
        if (intersect is True):
            if '3' in enteredType and '6' not in enteredType:
                # call template for earthquake
                # call fb and twitter api
                message1 = one_emergency_facebook_template.format('Earthquake',data['address'])
                postToSocialMedia(message1,2)
                message2 = one_emergency_twitter_template.format('Earthquake',data['address'])
                postToSocialMedia(message2,1)
                
            
            elif '6' in enteredType and '3' not in enteredType:
                # call template for terrorist
                # call fb and twitter api
                message1 = one_emergency_facebook_template.format('Terrorist Attack',data['address'])
                postToSocialMedia(message1,2)
                message2 = one_emergency_twitter_template.format('Terrorist Attack',data['address'])
                postToSocialMedia(message2,1)
            
            elif '3' in enteredType and '6' in enteredType: 
                # call template for terrorist and earthquake
                # call fb and twitter api
                message1 = two_emergency_facebook_template.format('Earthquake','Terrorist Attack', data['address'])
                postToSocialMedia(message1,2)
                message2 = two_emergency_twitter_template.format('Earthquake','Terrorist Attack', data['address'])
                postToSocialMedia(message2,1)
            
        
        return {"msg":"Incident status has been approved"},201

    def delete(self):
        return {"wow":"deteled"}