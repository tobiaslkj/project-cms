from flask_restful import Resource, reqparse
from flaskapp import db
from flaskapp.model.GPmobile import *
from sqlalchemy import update

class GPmobileResource(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('mobilePhone', help='mobilePhone field cannot be blank', required = True)
        parser.add_argument('postalCode', help='postalCode cannot be blank', required=True)
        data = parser.parse_args()
        
        #check if the mobilePhone number exist in database
        #if not exist, add a new row into db
        phone = GPMobile.query.filter_by(mobilePhone=data['mobilePhone']).first()
        if(phone is None):
            newPhone = GPMobile(mobilePhone=data['mobilePhone'], postalCode=data['postalCode'])
            db.session.add(newPhone)
            db.session.commit()
            
            return {"msg":"a new reported user phone and area are added."},201
        
        #if exist, update the postalCode under that phone number
        else:
            phone.postalCode = data['postalCode']
            db.session.commit()
            
            return {"msg":"new area is updated for existing reported user."},201
            
