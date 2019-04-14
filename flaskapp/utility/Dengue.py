import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint

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
