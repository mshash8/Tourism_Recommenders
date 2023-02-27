"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import requests, json
from datetime import datetime,timedelta
from meteostat import Stations, Daily, Hourly

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# enter your api key here
api_key = 'AIzaSyDvXY6zrSDLbP_uNCc7UV1zWqobtkk0l7A'

# url variable store url
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# The text string on which to search
query = st.text_input('Search query: ')


# get method of requests module
# return response object
r = requests.get(url + 'query=' + query +
						'&key=' + api_key)

# json method of response object convert
# json format data into python format data
x = r.json()

# now x contains list of nested dictionaries
# we know dictionary contain key value pair
# store the value of result key in variable y
y = x['results']


# keep looping upto length of y
for i in range(len(y)):
	
	# Print value corresponding to the
	# 'name' key at the ith index of y
	st.write(y[i]['name'])


d = st.date_input(
    "When\'s your birthday")
st.write('Your birthday is:', d)


t = st.time_input(
    "What is the time")
st.write('The time is:', t)
stations = Stations()
stations = stations.nearby(47.6628, -122.3139)
station = stations.fetch(1)
station_id = station.index[0]

st.write(type(d))

st.write(type(t))

st.write(type(datetime(2023, 2, 23)))

dt = datetime.combine(d,t)

st.write(dt)
# Set time period
start = dt
end = dt + timedelta(days=1)

# Get hourly data
data = Hourly(station_id, start, end)
data = data.fetch()
st.write("meteostat response: ")
st.write(data)

