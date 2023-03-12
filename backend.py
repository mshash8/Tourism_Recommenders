import pandas as pd
import numpy as np
import math
import requests, json
import base64
from datetime import datetime,timedelta
from meteostat import Stations, Daily, Hourly
import geocoder
from geopy.geocoders import Nominatim
import const

def call_google_api(url, queries, api_key, fields, latitude, longitude, r, b):
    places_df = pd.DataFrame()
    location_df = pd.DataFrame([[latitude,longitude]], columns = ['Lat','Long'])
    for query in queries:
        req = requests.get(url + 'query=' + query + '&fields=' + fields + '&key=' + api_key)
        req_json = req.json()
        api_response = req_json.get('results')
        df = pd.json_normalize(api_response)
        lat_long_df = pd.DataFrame(np.repeat(location_df.values, len(df.index), axis=0))
        lat_long_df.columns = location_df.columns
        df['Distance'] = haversine(lat_long_df['Lat'], lat_long_df['Long'], df['geometry.location.lat'], df['geometry.location.lng'])
        df['Query'] = query
        places_df = pd.concat([places_df,df])
    
    if places_df.empty == False:
        places_df = clean_and_sort(places_df, r, b)
    
    return places_df

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
    if 'nan' in unique:
        unique.remove('nan')
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
    if math.isnan(defining_weather) == True:
        alt_query = 'Tourist Places in' + str(location) 
        return alt_query
    defining_weather = int(defining_weather)
    location = str(location)
    weather_rules = const.WEATHER_CODES
    if defining_weather <= 2:
        queries = ['Parks in %s' % location, 'Beaches in %s' % location, 
        'Hikes in %s' % location, 'Trails in %s' % location,
        'Botanical Gardens in %s' % location, 'Outdoor activities in %s' % location]
    elif defining_weather <= 5:
        queries = ['Restaurants in %s' % location, 'Cafes in %s' % location, 
        'Hikes in %s' % location, 'Trails in %s' % location,
        'Museums in %s' % location, 'Indoor activities in %s' % location]
    elif defining_weather <= 11 or defining_weather == 17 or defining_weather == 18:
        queries = ['Restaurants in %s' % location, 'Cafes in %s' % location,
        'Museums in %s' % location, 'Indoor activities in %s' % location]
    elif defining_weather == 14 or defining_weather == 15 or defining_weather == 21:
        queries = ['Restaurants in %s' % location, 'Cafes in %s' % location, 
        'Snow hikes in %s' % location, 'Snow trails in %s' % location,
        'Skiing spots in %s' % location, 'Museums in %s' % location, 
        'Indoor activities in %s' % location]
    else:
        queries = []
    return queries

def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6378):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.
    
    Returns distance in kms.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
    a = np.sin((lat2-lat1)/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))

def clean_and_sort(df, r, b):
    df = df.drop_duplicates(subset = ['name', 'formatted_address'])
    df['Distance'] = df['Distance'].astype(int)
    df = df.loc[(df['Distance'] <=20) & (df['rating']>=r)]
    high_price_index = df[(df['price_level'] > b)].index
    df.drop(high_price_index , inplace=True)
    
    df.sort_values(['rating','Distance','user_ratings_total'], ascending = [False, True, False], inplace=True, na_position="last")
    return df
    