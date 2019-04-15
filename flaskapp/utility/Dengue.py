import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
import xmltodict
import json

def getDengue():
    # Get the update geojson url
    meta = requests.get('https://data.gov.sg/api/action/resource_show?id=8af18201-f3b0-4a9c-924e-f0bd8dda7bf6')
    metaResult = meta.json()
    
    # Get the  geojson
    r = requests.get(metaResult['result']['url'])
    json_object = r.json()

    # processing and scraping
    for item in json_object['features']:
        soup = BeautifulSoup(item['properties']['Description'],'html.parser')
        th = soup.find_all('th', attrs={'colspan':None})
        td = soup.select('td')
        for k ,v in zip(th, td):
            item['properties'][k.text.strip()] = v.text.strip()
        
        # if harrison want description, remove proceeding line
        del item['properties']['Description']

    return json_object['features']

def getDengueMeta():
    response = requests.get("https://data.gov.sg/api/action/package_show?id=dengue-cases")
    print(response.status_code)
    body = response.content

    den_dict = {}
    den_dict['description'] = " ".join(
        ((json.loads(body)['result']['description'])).split())

    objects = json.loads(body)['result']['resources']
    for object in objects:
        name = ("".join(object['name'][17:-6].split())).lower()
        xmlresponse = requests.get(object['url'])
        response = json.loads(json.dumps(xmltodict.parse(xmlresponse.content)))
        den_dict[name] = response['kml']['Document']['Folder']['Placemark'][0]['ExtendedData']['SchemaData']['SimpleData'][1]['#text'][-1]
    
    return den_dict