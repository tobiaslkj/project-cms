from flask import Flask, request
import requests
import json

app = Flask(__name__)
@app.route('/weather')
def getWeather():
    r = requests.get('https://api.data.gov.sg/v1/environment/2-hour-weather-forecast')
    data = r.json()

    for elements in data['area_metadata']:
        topName = elements['name']
        coordinates = elements['label_location']
        longitude = elements['label_location']['longitude']
        lat = elements['label_location']['latitude']

        for elements in data['items']:
            for d in elements['forecasts']:
                bottomName = d['area']
                if topName == bottomName:
                    forecast = d['forecast']
                    forecastList = {"location": bottomName, "forecast": forecast}
                    print(topName)
                    print(longitude)
                    print(lat)
                    print(forecast)

    # for elements in data['area_metadata']:
    #     coordinates = elements['label_location']
    #     coordinateList = {"coordinates": coordinates}
    #     print(coordinateList)

    # for elements in data['items']:
    #     for d in elements['forecasts']:
    #         name = d['area']
    #         forecast = d['forecast']
    #         forecastList = {"location": name, "forecast": forecast}
    #         print(forecastList)

    #print(locationList)
    
    # for fuck in elements:
    #     print(fuck['label_location'])
    # for elements in data['area_metadata']:
    #     print(elements['name'])
    # for elements in data['area_metadata']['label_location']:
    #     for elements in elements['label_location']:
    #         print(elements['longitude'])
    # print(data['area_metadata'][0]['name'])
    return "FUCK YOU"

if __name__ == '__main__':  
    app.run(debug=True)

    # geojson = {
    #     "type": "FeatureCollection",
    #     "features": [
    #     {
    #         "type": "Feature",
    #         "geometry": {
    #             "type": "Point",
    #             "coordinates": [d["lable_location"]],
    #         },
    #         "properties": {
    #             "location": [d["name"]],
    #             "forecast": ["item"],
    #         }
    #     } for d in elements
    #     ]
    # }
    # weather = json.loads(json.dumps(geojson))
    # weatherList.append(weather)
    # print(weatherList)