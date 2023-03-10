"""
This module is used to make api calls and
write the recommendation rules
"""
import base64
from datetime import datetime,timedelta
import geocoder
from geopy.geocoders import Nominatim
from meteostat import Stations, Hourly
import requests
import constants


def call_google_api(url, query, api_key, fields):
    """
    function docstring
    """
    req = requests.get(url + 'query=' + query + '&fields=' + fields + '&key=' + api_key)
    req_json = req.json()
    return req_json.get('results')

def call_meteostat_api(latitude, longitude, date, time):
    """
    function docstring
    """
    stations = Stations()
    date_time = datetime.combine(date,time)
    nearby_stations = stations.nearby(latitude, longitude)
    station = nearby_stations.fetch(1)
    station_id = station.index[0]
    data = Hourly(station_id, date_time, date_time + timedelta(days=1))
    data = data.fetch()
    weather = list(data['coco'].values)
    unique  = list(set(weather))
    return max(unique)

def decode_api_key(encoded_key):
    """
    function docstring
    """
    base64_bytes = encoded_key.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')

def get_latitude_and_longitude(location):
    """
    function docstring
    """
    if location:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(str(location))
        lat, longi = float(location.latitude), float(location.longitude)
    else:
        lat, longi = get_current_loc()
    return lat, longi

def get_user_entered_loc(location_as_string):
    """
    function docstring
    """
    geolocator = Nominatim(user_agent="geoapi_recommender")
    lat, longi = get_current_loc()
    location_as_string = geolocator.geocode(str(lat)+","+str(longi))
    return location_as_string

def get_current_loc():
    """
    function docstring
    """
    geo = geocoder.ip('me')
    return float(geo.latlng[0]), float(geo.latlng[1])

def basic_rules(defining_weather, location):
    """
    function docstring
    """
    defining_weather = int(defining_weather)
    location = str(location)
    if defining_weather <= 2:
        #queries = ['Outdoor activities near %s' % location, 'Parks near %s' % location,
        #'Beaches near %s' % location, 'Hikes or Trails near %s' % location]
        alt_query = 'Things to do near %s when it is %s' \
        % (location, constants.WEATHER_CODES[str(defining_weather)])
        #query = 'Outdoor activities in Seattle'
    elif defining_weather <= 5:
        alt_query = 'Things to do near %s when it is %s' \
        % (location, constants.WEATHER_CODES[str(defining_weather)])
    alt_query = 'Things to do near %s when it is %s' \
    % (location, constants.WEATHER_CODES[str(defining_weather)])
    return alt_query
