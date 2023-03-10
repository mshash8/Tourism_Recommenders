import streamlit as st
import pandas as pd
import requests, json
import base64
from datetime import datetime,timedelta
from meteostat import Stations, Daily, Hourly

# enter your api key here
api_key_encode = 'QUl6YVN5RHZYWTZ6clNETGJQX3VOQ2M3VVYxeldxb2J0a2swbDdB'
base64_bytes = api_key_encode.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
api_key = message_bytes.decode('ascii')


# url variable store url
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# The text string on which to search
query=''
query = st.text_input('Search query: ')


# get method of requests module
# return response object
r = requests.get(url + 'query=' + query +
                        '&fields=opening_hours' +
						'&key=' + api_key)


# json method of response object convert
# json format data into python format data
x = r.json()

# now x contains list of nested dictionaries
# we know dictionary contain key value pair
# store the value of result key in variable y
y = x['results']

r = st.number_input("Minimum rating you want 1-5")
b = st.number_input("Price level 1-5")
d = st.date_input("When do you wish to visit (only upto 1 day beyond today")
t = st.time_input("What time do you wish to visit")


# keep looping upto length of y

res_set=[]
for i in range(len(y)):
    if y[i]['rating']>=r:
        res_set.append(y[i])



try:
    if query !='':
        st.write("TOP 5 PLACES BASED ON YOUR SEARCH")
    for i in range(5):
        st.write(res_set[i]['name'])
        place_id = res_set[i]['place_id']
        new_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+place_id+'&key=' + api_key+'&fields=name,opening_hours'
        rw = requests.get(new_url)
        xw = rw.json()
        st.write("Rating: " + str(res_set[i]['rating']))
        try:
            st.write("Price Level: "+ str(res_set[i]['price_level']))
        except:
            st.write("price level Data not available")
        try:
            st.write(xw['result']['opening_hours']['weekday_text'])
        except:
            st.write("Open hours not available")

except:
    pass
    
stations = Stations()
stations = stations.nearby(47.6628, -122.3139)
station = stations.fetch(1)
station_id = station.index[0]
dt = datetime.combine(d,t)
#st.write(dt)
start = dt
end = dt + timedelta(days=1)
# Get hourly data
data = Hourly(station_id, start, end)
data = data.fetch()
weather = list(data['coco'].values)
unique  = list(set(weather))
defining_weather = max(unique)
#st.write(unique)
weather_codes = {
1	: 'Clear',
2	: 'Fair',
3	: 'Cloudy',
4	: 'Overcast',
5	: 'Fog',
6	: 'Freezing Fog',
7	: 'Light Rain',
8	: 'Rain',
9	: 'Heavy Rain',
10	: 'Freezing Rain',
11	: 'Heavy Freezing Rain',
12	: 'Sleet',
13	: 'Heavy Sleet',
14	: 'Light Snowfall',
15	: 'Snowfall',
16	: 'Heavy Snowfall',
17	: 'Rain Shower',
18	: 'Heavy Rain Shower',
19	: 'Sleet Shower',
20	: 'Heavy Sleet Shower',
21	: 'Snow Shower',
22	: 'Heavy Snow Shower',
23	: 'Lightning',
24	: 'Hail',
25	: 'Thunderstorm',
26	: 'Heavy Thunderstorm',
27	: 'Storm'
}

if query!='':
    if defining_weather > 5:
        st.write("SUGGESTED PLACES BECAUSE THE WEATHER ON THE DAY YOU HAVE ENTIRED IS "+weather_codes[defining_weather])
        r3 = requests.get(url + 'query=' + 'Indoor Activities in Seattle' +
                            '&key=' + api_key)
        x3 = r3.json()

        # now x contains list of nested dictionaries
        # we know dictionary contain key value pair
        # store the value of result key in variable y
        y3 = x3['results']
        for i in range(5):
            st.write(y3[i]['name'])
            place_id = y3[i]['place_id']
            new_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+place_id+'&key=' + api_key+'&fields=name,opening_hours'
            rw = requests.get(new_url)
            xw = rw.json()
            st.write("Rating: " + str(y3[i]['rating']))


    else:
        st.write("SUGGESTED PLACES BECAUSE THE WEATHER ON THE DAY YOU HAVE ENTIRED IS CLEAR, NO RAIN OR SNOW")
        r3 = requests.get(url + 'query=' + 'Parks and Beaches in Seattle' +
                            '&key=' + api_key)
        x3 = r3.json()

        # now x contains list of nested dictionaries
        # we know dictionary contain key value pair
        # store the value of result key in variable y
        y3 = x3['results']
        for i in range(5):
            st.write(y3[i]['name'])
            place_id = y3[i]['place_id']
            new_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+place_id+'&key=' + api_key+'&fields=name,opening_hours'
            rw = requests.get(new_url)
            xw = rw.json()
            st.write("Rating: " + str(y3[i]['rating']))




