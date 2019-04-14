from flask_restful import Resource, reqparse    
from flask_jwt_extended import jwt_required, create_access_token
from flask import jsonify, abort
from flaskapp.utility.PSI import getPSI

class PSIResource(Resource):
    def get(self):
        data = getPSI()
        
        return {"features":data},200
