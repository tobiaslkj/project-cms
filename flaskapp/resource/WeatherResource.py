from flask_restful import Resource, reqparse    
from flask_jwt_extended import jwt_required, create_access_token
from flask import jsonify, abort
from flaskapp.utility.Weather import getWeather, getForecastWeather

class WeatherResource(Resource):
    def get(self):
        data = getWeather()
        forecast = getForecastWeather()
        return {"features":data, "information":forecast},200
