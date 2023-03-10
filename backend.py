import pandas as pd
import requests, json
import base64
from datetime import datetime,timedelta
from meteostat import Stations, Daily, Hourly
import geocoder
from geopy.geocoders import Nominatim
import const

def call_google_api(url, query, api_key, fields):
    req = requests.get(url + 'query=' + query + '&fields=' + fields + '&key=' + api_key)
    req_json = req.json()
    return req_json.get('results')

def call_meteostat_api(latitude, longitude, date, time):
    stations = Stations()
    date_time = datetime.combine(date,time)
    nearby_stations = stations.nearby(latitude, longitude)
    station = nearby_stations.fetch(1)
    station_id = station.index[0]
    start = date_time
    end = date_time + timedelta(days=1)
    data = Hourly(station_id, start, end)
    data = data.fetch()
    weather = list(data['coco'].values)
    unique  = list(set(weather))
    return max(unique)

def decode_api_key(encoded_key):
    base64_bytes = encoded_key.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    api_key = message_bytes.decode('ascii')
    return api_key

def get_latitude_and_longitude(location):
    try:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(str(location))
        lat = float(location.latitude)
        longi = float(location.longitude)
    except:
        lat, longi = get_current_loc(location)
    return lat, longi

def get_user_entered_loc(location_as_string):
    geolocator = Nominatim(user_agent="geoapi_recommender")
    lat, longi = get_current_loc()
    location_as_string = geolocator.geocode(str(lat)+","+str(longi))
    return location_as_string

def get_current_loc():
    g = geocoder.ip('me')
    latlng = g.latlng
    lat = float(latlng[0])
    longi = float(latlng[1])
    return lat, longi


def basic_rules(defining_weather, location):
    defining_weather = int(defining_weather)
    location = str(location)
    weather_rules = const.WEATHER_CODES
    if defining_weather <= 2:
        queries = ['Outdoor activities near %s' % location, 'Parks near %s' % location, 
        'Beaches near %s' % location, 'Hikes or Trails near %s' % location]
        alt_query = 'Things to do near' + location + 'when it is' + weather_rules[str(defining_weather)]
        query = 'Outdoor activities in Seattle'
    elif defining_weather <= 5:
        alt_query = 'Things to do near' + location + 'when it is' + weather_rules[str(defining_weather)]
    alt_query = 'Things to do near' + location + 'when it is' + weather_rules[str(defining_weather)]
    return alt_query