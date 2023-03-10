import streamlit as st
import pandas as pd
import constants
import backend

r = st.number_input("Minimum rating you want 1-5")
b = st.number_input("Price level 1-5")
date = st.date_input("When do you wish to visit (only upto 1 day beyond today")
time = st.time_input("What time do you wish to visit")
location = st.text_input("Enter your location or leave blank to use your current location")

api_key = backend.decode_api_key(constants.ENCODED_GOOGLE_API_KEY)
if location == "":
    location = backend.get_user_entered_loc(location)

st.write(location)

latitude, longitude = backend.get_latitude_and_longitude(location)
meteostat_api_response = backend.call_meteostat_api(latitude,longitude,date,time)
st.write(meteostat_api_response)


query = backend.basic_rules(meteostat_api_response, location)
google_api_response = backend.call_google_api(constants.GOOGLE_MAPS_API, query, api_key, 'opening_hours')
st.write(google_api_response)


## ST.WRITE TO THE FRONT END HERE

# loc = st.text_input("Enter your location or leave blank to use your current location")

# res = backend.user_entered_loc(loc)

# st.write(res)
