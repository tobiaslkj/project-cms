from flask_restful import Resource

class IncidentResource(Resource):
    def get(self):
        return {'Incident': 'world' }

    def post(self):
        return {"incident":"ok i got posted"}

    def put(self):
        return {"wow":"oklor"}

    def delete(self):
        return {"wow":"deteled"}