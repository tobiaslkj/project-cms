from flaskapp.access_control import operator_required
from flaskapp.utility.Twitter import postToTwitter
from flask_restful import Resource, reqparse

class SocialMediaResource(Resource): 
    @operator_required
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('message', help='Address field cannot be blank', required = True)
        # parser.add_argument('social_media_target',action='append', help='This field cannot be blank',required=True)
        data = parser.parse_args()  
        postToTwitter(data['message'])
        return {"message":"Twitter updated"}
        