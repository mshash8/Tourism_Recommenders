"""
Backend code for the Weather-Integrated Tourism Recommendation System

This script has functions defined which are useful in extracting data
from the Google Maps API and the Meteostat Weather API to recommend
tourist attractions and activities for the users based on the weather.
Two types of recommendations are provided - one based on the user
preference, and the other based on what we think would be a good place
to visit based on the weather. All the recommendations are made taking
into account the user inputs like date, time, price level, rating, and
proximity.

The script requires that the 'math', 'base64', 'datetime', 'pandas',
'numpy', 'requests', 'meteostat', 'geocoder' and 'geopy' packages be
installed within the Python environment this script is being run in.

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
    This function fetches a list of places from the Google Maps API
    using the URL, the decoded API key, and the search queries
    generated from basic_rules(). The results obtained from the API are
    of json type which are then converted to a dataframe.

    It takes eight arguments - 'url' which is a constant string value
    representing the Maps API URL, 'queries' which is a list of search
    queries each of type string, 'api_key' which is a constant string
    value of the decoded API key, 'fields' which is a list of string
    values of the extra variables one would want from the API on top of
    the default variables, 'lat' and 'long' which are float values of
    the latitude and longitude of the user's location, 'rating' which
    is a float value of the user's preferred rating, and 'price' which
    is an integer value of the user's maximum price-level preference.

    The return value - 'places_df' is the final filtered and sorted
    dataframe containing a list of recommendations based on the weather.

    """
    places_df = pd.DataFrame()
    location_df = pd.DataFrame([[lat,long]], columns = ['Lat','Long'])

    for query in queries:
        #fetch data from the Google Maps API
        req = requests.get(url + 'query=' + query + '&fields=' + fields +
                           '&key=' + api_key)
        req_json = req.json()
        api_response = req_json.get('results')

        #convert json format to a dataframe
        output_df = pd.json_normalize(api_response)

        lat_long_df = pd.DataFrame(np.repeat(location_df.values,
                                             len(output_df.index), axis = 0))
        lat_long_df.columns = location_df.columns

        if output_df.empty is False:
            if set(['geometry.location.lat',
                    'geometry.location.lng']).issubset(output_df.columns):
                #compute distance between user's location and recommendation
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
    This function takes the user input for latitude, longitude, date
    and time to compute the weather conditions. The hourly weather data
    is fetched from the nearby weather stations and the weather
    condition codes are extracted. Weather condition codes are constant
    values ranging from 1 to 27 each depicting a particular weather
    condition (clear, fog, rain, snow, etc.). The average hourly
    weather condition code is then computed.

    It takes four arguments - 'latitude', 'longitude', 'date' and
    'time' based on the user's input. The variables 'latitude' and
    'longitude' correspond to the user's desired location and are float
    values. The variables 'date' and 'time' correspond to the user's
    desired date and time of travel, and are of type date and time
    respectively.

    The return value - 'pred_weather' is the predicted average hourly
    weather condition rounded to zero decimal. It is of type float.

    Exceptions - Raises an error when the input date and time belong to
    the past or are beyond 8 days from the current date.

    """
    stations = Stations()
    date_time = dt.datetime.combine(date,time)

    #find weather stations near the input latitude and longitude
    nearby_stations = stations.nearby(latitude, longitude)

    #fetch hourly weather data from the stations for one day
    station = nearby_stations.fetch(1)
    station_id = station.index[0]
    start = date_time
    end = date_time + dt.timedelta(days=1)
    data = Hourly(station_id, start, end)
    data = data.fetch()

    #extract the weather condition code values
    weather = list(data['coco'].values)
    unique  = list(set(weather))

    values = []

    #remove nan values in the weather condition codes data
    for element in unique:
        if not math.isnan(element):
            values.append(element)
        else:
            continue

    #if the weather codes list is empty, assign a default value of 0
    if not values:
        values.append(0)
    else:
        pass

    #compute the average hourly weather code for the input date and time
    pred_weather = sum(values)/len(values)

    return round(pred_weather, 0)


def decode_api_key(encoded_key):
    """
    The function gets the constant encoded Google Maps API key and
    decodes it to allow the program to extract data from the API.

    It takes one argument - 'encoded_key' which is of string type.

    The return value - 'api_key' which is the decoded API key, and is
    of string type too.

    """
    base64_bytes = encoded_key.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    api_key = message_bytes.decode('ascii')

    return api_key


def get_latitude_and_longitude(location):
    """
    This function returns the latitude and longitude values of the
    location whether it is a user-entered location or the user's
    current location. If the user leaves the location input blank,
    get_current_loc() is called to obtain the corresponding latitude
    and longitude values. Otherwise, the latitude and longitude values
    are extracted from the user's input location.

    It takes one argument - 'location' which is the user's input
    location, and is of string type.

    The return value - 'lat' and 'longi' are the latiude and longitude
    values respectively of the input location, and are of type float.

    Exceptions - Raises an error when the user's input location is
    invalid or contains characters other than the english letters,
    digits, and commas.

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
    This function is called when the user allows the program to access
    their current location. The function get_current_loc() is called to
    get the latitude and longitude of the user's current location.
    These values are then used to extract the location of the user in
    the form of a string. Location in the form of a string allows the
    program to build search queries that can be used to call the Google
    Maps API. Note that if the user enters only spaces in the input,
    the current location is fetched.

    No arguments are taken for this function.

    The return value - 'location_as_string' is the current location of
    the user, and of type string.

    """
    geolocator = Nominatim(user_agent="geoapi_recommender")
    lat, longi = get_current_loc()
    location_as_string = geolocator.geocode(str(lat)+","+str(longi))

    return location_as_string


def get_current_loc():
    """
    This function is called by get_user_entered_loc() to extract the
    latitude and longitude values of the user's current location.

    No arguments are taken for this function.

    The return values - 'geo.latlng[0]' and 'geo.latlng[1]' are the
    latitude and longitude values respectively, and of the type float.

    """
    geo = geocoder.ip('me')

    return float(geo.latlng[0]), float(geo.latlng[1])


def check_date_invalid(date, time):
    """
    This function checks the validity of the user's input date and
    time. A value error is raised if the user's input date and time are
    in the past or are beyond 8 days from today.

    It takes two arguments - 'date' and 'time' corresponding to the
    user's desired date and time of travel. These variables are of type
    date and time respectively.

    There are no return values for this function.

    Exceptions - Raises an error when the input date and time belong to
    the past or are beyond 8 days from the current date.

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
    This function checks for invalid special characters in the user's
    input location and raises a value error. These invalid characters
    include anything other than the english letters, digits or commas.

    It takes one argument - 'location' which is the user-entered
    location and is of type string. Note that in case of the user's
    current location being used, this function does not execute the
    checks.

    There are no return values for this function.

    Exceptions - Raises an error when the user's input location
    contains characters other than the english letters, digits, and
    commas.

    """
    if str(location).strip() != "":
        for _ , character in enumerate(location):
            if character not in (',', ' ') and character.isalpha() is False\
                and character.isdigit() is False:
                raise ValueError("The location has invalid special\
                                  characters!")
    else:
        pass


def check_address_invalid(location):
    """
    This function checks for invalid input address and raises a value error.
    An address is considered to be invalid when the geolocator.geocode() is
    not able to retrieve the location from the input.

    It takes one argument - 'location' which is the user-entered
    location and is of type string. Note that in case of the user's
    current location being used, this function does not execute the
    checks.

    There are no return values for this function.

    Exceptions - Raises an error when the user's input location is
    invalid

    """
    if str(location).strip() != "":
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(str(location))
        if location is None:
            raise ValueError("The location does not exist in our database!")
    else:
        pass


def basic_rules(defining_weather, location):
    """
    This function curates a list of search queries based on the weather
    condition of the user's desired date and time of travel. A weather
    condition code equal to zero implies that the weather for that day
    is uncertain. In such a case, recommendations are made across all
    categories without taking weather into consideration. A weather
    condition code <= 2 implies a clear and sunny day. In such case,
    beaches, parks, hikes, etc. are recommended. A weather condition
    code >2 and <= 5 implies a cloudy day. In such case, cafes, hikes,
    musuems, etc. are recommended. A weather condition code >5 and
    <= 11, or equal to 17 or 18 implies a rainy day. In such case,
    cafes, musuems, indoor activities etc. are recommended. A weather
    condition code equal to 14, 15 or 21 implies a snowy day. In such
    case, cafes, snow hikes, restaurants, etc. are recommended. For any
    other value, the weather is not favourable to go out, and thus no
    recommendations are made.

    It takes two input arguments - 'defining_weather' which is the
    average hourly weather condition for the user's preferred date and
    time, and 'location' which is the user's location. The arguments
    are of type float and string respectively.

    The return value - 'queries' is a list of search queries where all
    the search queries are of string type. These search queries allow
    the Google Maps API to fetch data.

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
    elif defining_weather in (14, 15, 21):
        queries = [f'Cafes in {location}', f'Snow Hikes in {location}',
                   f'Indoor Activities in {location}',
                   f'Museums in {location}', f'Restaurants in {location}']
    else:
        queries = []

    return queries


def haversine(lat1, lon1, lat2, lon2):
    """
    This function uses the Haversine formula to compute the great
    circle distance between two points on a sphere using the
    corresponding latitude and longitude values. This helps the program
    recommend places based on proximity.

    It takes four arguments - 'lat1', 'lon1', 'lat2', and 'lon2' where
    'lat1' and 'lon1' correspond to the coordinates of the user's input
    location while 'lat2' and 'lon2' correspond to the coordinates of
    the recommended places. All the input variables are of type float.

    The return value - 'distance' is the distance between the two input
    locations and is measured in miled. It is a float value.

    """
    earth_radius = 3958.8

    lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
    value = np.sin((lat2-lat1)/2.0)**2 + np.cos(lat1) * np.cos(lat2) *\
        np.sin((lon2-lon1)/2.0)**2
    distance = earth_radius * 2 * np.arcsin(np.sqrt(value))

    return distance


def clean_and_sort(places_df, rating, price):
    """
    This function takes the dataframe of recommended places along with
    the user's preferred rating and price to filter and sort the
    recommendations. It is important to note that the columns
    'price_level' and 'rating' in the dataframe may not always exist
    as the Google Maps dataset does not have this variable for all
    locations. Thus, checks are performed to ensure that these columns
    exist before applying any filters. Sorting is also performed in the
    order of Rating, Distance and Total User Ratings to recommend
    places that have high ratings, are nearby and have a high number of
    total user ratings.

    It takes three arguments - 'places_df' which is the dataframe of
    recommendations and of type dataframe, 'rating' which is the user's
    preferred rating and of type float, 'price' which is the user's
    preferred price-level and of type int.

    The return value - 'places_df' is a cleaned and sorted dataframe
    with recommendations based on the user's preference of pricing and
    rating.

    """
    places_df = places_df.drop_duplicates(subset = ['name',
                                                    'formatted_address'])
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
    