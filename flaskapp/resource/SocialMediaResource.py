from flaskapp.access_control import operator_required
from flaskapp.utility.SocialMedia import postToSocialMedia
from flask_restful import Resource, reqparse

class SocialMediaResource(Resource): 
    # @operator_required
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('message', help='Address field cannot be blank', required = True)
        parser.add_argument('social_media_target', help='This field cannot be blank',required=True)
        data = parser.parse_args()  
        
        if(data['social_media_target'].isdigit()):
            postToSocialMedia(data['message'],int(data['social_media_target']))
        else:
            return {"message":"Wrong input, must be integer"},400

        
        return {"message":"Social Media updated"}
        