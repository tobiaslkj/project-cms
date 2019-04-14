from flask import Flask, request
import requests
import json

def getWeather():
    r = requests.get('https://api.data.gov.sg/v1/environment/2-hour-weather-forecast')
    data = r.json()
    firstPart = data['area_metadata']
    secondPart = data['items'][0]['forecasts']
    weatherList=[]
    for i,j in zip(firstPart,secondPart):
        weatherItem = {}
        weatherItem['type'] = "Feature"
        weatherItem['geometry'] = {"type":"Point","coordinates":[i['label_location']['longitude'], i['label_location']['latitude']]}
        weatherItem['properties']={"location": j['area'],"forecast": j['forecast']}
        weatherList.append(weatherItem)

    return weatherList

def getForecastWeather():
    response = requests.get("https://api.data.gov.sg/v1/environment/4-day-weather-forecast")

    body = response.content
    # print(body)
    object = json.loads(body)['items'][0]['forecasts']

    lst = []

    for index, item in enumerate(object):
        date = ((item['date'])[8:] + "-" + (item['date'])
            [5:7] + "-" + (item['date'])[0:4])

        forecast = item['forecast']
        high = str(item['temperature']['high'])
        low = str(item['temperature']['low'])

        o = {"date": date, "temperature(high)": high,
            "temperature(low)": low, "forecast": forecast}

        weather = json.loads(json.dumps(o, indent=4))
        lst.append(weather)
    return lst
#     # for elements in data['area_metadata']:
#     #     topName = elements['name']
#     #     coordinates = elements['label_location']
#     #     longitude = elements['label_location']['longitude']
#     #     lat = elements['label_location']['latitude']

#     #     for elements in data['items']:
#     #         for d in elements['forecasts']:
#     #             bottomName = d['area']
#     #             if topName == bottomName:
#     #                 forecast = d['forecast']
#     #                 forecastList = {"location": bottomName, "forecast": forecast}
#     #                 print(topName)
#     #                 print(longitude)
#     #                 print(lat)
#     #                 print(forecast)

#     # for elements in data['area_metadata']:
#     #     coordinates = elements['label_location']
#     #     coordinateList = {"coordinates": coordinates}
#     #     print(coordinateList)

#     # for elements in data['items']:
#     #     for d in elements['forecasts']:
#     #         name = d['area']
#     #         forecast = d['forecast']
#     #         forecastList = {"location": name, "forecast": forecast}
#     #         print(forecastList)

#     #print(locationList)
    
#     # for fuck in elements:
#     #     print(fuck['label_location'])
#     # for elements in data['area_metadata']:
#     #     print(elements['name'])
#     # for elements in data['area_metadata']['label_location']:
#     #     for elements in elements['label_location']:
#     #         print(elements['longitude'])
#     # print(data['area_metadata'][0]['name'])
#     return "FUCK YOU"

# if __name__ == '__main__':  
#     app.run(debug=True)

#     # geojson = {
#     #     "type": "FeatureCollection",
#     #     "features": [
#     #     {
#     #         "type": "Feature",
#     #         "geometry": {
#     #             "type": "Point",
#     #             "coordinates": [d["lable_location"]],
#     #         },
#     #         "properties": {
#     #             "location": [d["name"]],
#     #             "forecast": ["item"],
#     #         }
#     #     } for d in elements
#     #     ]
#     # }
#     # weather = json.loads(json.dumps(geojson))
#     # weatherList.append(weather)
#     # print(weatherList)