"""
Modeule docstring
    
"""

import math
import base64
import datetime as dt
import pandas as pd
import numpy as np
import requests
from meteostat import Stations, Hourly
import geocoder
from geopy.geocoders import Nominatim


def call_google_api(url, queries, api_key, fields, lat, long, rating, price):
    """
    function docstring
    
    """
    places_df = pd.DataFrame()
    location_df = pd.DataFrame([[lat,long]], columns = ['Lat','Long'])

    for query in queries:
        req = requests.get(url + 'query=' + query + '&fields=' + fields +
                           '&key=' + api_key)
        req_json = req.json()
        api_response = req_json.get('results')
        output_df = pd.json_normalize(api_response)
        lat_long_df = pd.DataFrame(np.repeat(location_df.values,
                                             len(output_df.index), axis = 0))
        lat_long_df.columns = location_df.columns
        if output_df.empty is False:
            if set(['geometry.location.lat',
                    'geometry.location.lng']).issubset(output_df.columns):
                output_df['Distance'] = haversine(lat_long_df['Lat'],
                                            lat_long_df['Long'],
                                            output_df['geometry.location.lat'],
                                            output_df['geometry.location.lng'])
                output_df['Distance'] = np.round(output_df['Distance'], 1)
            else:
                output_df.loc[:, 'Distance'] = -1
            output_df['Query'] = query
            places_df = pd.concat([places_df, output_df], ignore_index=True)
        else:
            continue

    if places_df.empty is False:
        places_df = clean_and_sort(places_df, rating, price)
    else:
        pass

    return places_df


def call_meteostat_api(latitude, longitude, date, time):
    """
    function docstring
    
    """
    stations = Stations()
    date_time = dt.datetime.combine(date,time)
    nearby_stations = stations.nearby(latitude, longitude)
    station = nearby_stations.fetch(1)
    station_id = station.index[0]
    start = date_time
    end = date_time + dt.timedelta(days=1)
    data = Hourly(station_id, start, end)
    data = data.fetch()
    weather = list(data['coco'].values)
    unique  = list(set(weather))
    values = []
    for element in unique:
        if not math.isnan(element):
            values.append(element)
        else:
            continue

    if not values:
        values.append(0)
    else:
        pass

    pred_weather = sum(values)/len(values)

    return round(pred_weather, 0)


def decode_api_key(encoded_key):
    """
    function docstring
    
    """
    base64_bytes = encoded_key.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    api_key = message_bytes.decode('ascii')

    return api_key


def get_latitude_and_longitude(location):
    """
    function docstring

    """
    if str(location) == "":
        lat, longi = get_current_loc()
    else:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(str(location))
        lat, longi = float(location.latitude), float(location.longitude)

    return lat, longi


def get_user_entered_loc():
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


def check_date_invalid(date, time):
    """
    function docstring

    """
    datetime_then = dt.datetime.combine(date, time)
    datetime_now = dt.datetime.now().replace(second=0, microsecond=0)
    duration = datetime_then - datetime_now
    days = duration.days

    if days > 8 or days < 0:
        raise ValueError("The date and time must be in the future and within\
                          8 days from today!")


def check_address_characters(location):
    """
    function docstring

    """
    if str(location) != "":
        for _ , character in enumerate(location):
            if character not in (',', ' ') and character.isalpha() is False and\
                character.isdigit() is False:
                raise ValueError("The location has invalid special\
                                  characters!")
    else:
        pass


def check_address_invalid(location):
    """
    function docstring

    """
    if location != "":
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(str(location))
        if location is None:
            raise ValueError("The location does not exist in our database!")
    else:
        pass


def basic_rules(defining_weather, location):
    """
    function docstring
    
    """
    defining_weather = int(defining_weather)
    location = str(location)

    if defining_weather == 0:
        alt_query = [f'Beaches in {location}',
                     f'Cafes and Restaurants in {location}',
                     f'Hikes and Trails in {location}',
                     f'Indoor Activities in {location}',
                     f'Museums in {location}',
                     f'Outdoor Activities in {location}',
                     f'Parks and Botanical Gardens in {location}']
        return alt_query
    else:
        pass

    if defining_weather <= 2:
        queries = [f'Beaches in {location}',
                   f'Botanical Gardens in {location}',
                   f'Hikes and Trails in {location}',
                   f'Outdoor Activities in {location}',
                   f'Parks in {location}']
    elif defining_weather <= 5:
        queries = [f'Cafes in {location}', f'Hikes and Trails in {location}',
                   f'Indoor Activities in {location}',
                   f'Museums in {location}', f'Restaurants in {location}']
    elif defining_weather <= 11 or defining_weather == 17 or\
        defining_weather == 18:
        queries = [f'Cafes in {location}', f'Indoor Activities in {location}',
                   f'Museums in {location}', f'Restaurants in {location}']
    elif defining_weather == 14 or defining_weather == 15 or\
        defining_weather == 21:
        queries = [f'Cafes in {location}', f'Snow Hikes in {location}',
                   f'Indoor Activities in {location}',
                   f'Museums in {location}', f'Restaurants in {location}']
    else:
        queries = []

    return queries


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.
    
    Returns distance in miles.

    """
    earth_radius = 3958.8

    lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
    value = np.sin((lat2-lat1)/2.0)**2 + np.cos(lat1) * np.cos(lat2) *\
        np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(value))


def clean_and_sort(places_df, rating, price):
    """
    function docstring
    
    """
    places_df = places_df.drop_duplicates(subset = ['name',
                                                    'formatted_address'])
    #places_df['Distance'] = places_df['Distance'].astype(int)
    places_df = places_df.loc[(places_df['Distance'] <= 30.0)]

    if 'price_level' in places_df.columns:
        places_df.loc[places_df['price_level'].isna(), 'price_level'] = 0.0
        places_df = places_df.loc[(places_df['price_level'] <= price)]
    else:
        places_df.loc[:, 'price_level'] = "Unknown"

    if 'rating' in places_df.columns:
        places_df = places_df.loc[(places_df['rating'] >= rating)]
        if 'user_ratings_total' in places_df.columns:
            places_df.sort_values(['rating','Distance','user_ratings_total'],
                                  ascending = [False, True, False], inplace =
                                  True, na_position = "last")
        else:
            places_df.sort_values(['rating','Distance'], ascending =
                                  [False, True], inplace = True, na_position =
                                  "last")
    else:
        places_df.loc[:, 'rating'] = "Unknown"
        places_df.sort_values(['Distance'], ascending = [True],
                              inplace = True, na_position = "last")

    return places_df
    