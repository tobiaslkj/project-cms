from flask_restful import Resource, reqparse    
from flask_jwt_extended import jwt_required, create_access_token
from flask import jsonify, abort
from flaskapp.utility.Dengue import getDengue, getDengueMeta

class DengueResource(Resource):
    def get(self):
        data = getDengue()
        meta = getDengueMeta()
        return {"features":data, "meta": getDengueMeta()}
