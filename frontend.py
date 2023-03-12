import streamlit as st
import pandas as pd
import math
import const
import backend

st.set_page_config(layout = "wide")

var1 = st.empty()
var2 = st.empty()
var3 = st.empty()
var4 = st.empty()
var5 = st.empty()
var6 = st.empty()
var7 = st.empty()

pref = var1.selectbox('Do you have any particular preference for a place?', 
        ('None', 'Beaches', 'Cafes and Restaurants', 'Hikes and Trails',
         'Indoor Activities', 'Museums', 'Outdoor Activities',
         'Parks & Botanical Gardens', 'Skiing Spots'))
date = var2.date_input("When do you wish to visit? (To get more accurate results, please enter a date that is not beyond 2-3 days from today)\nNOTE: Dates beyond 8 days from today are invalid!")
time = var3.time_input("What time do you wish to visit?")
r = var4.number_input("Minimum rating you want from 1-5", min_value=0.0, max_value=5.0, value = 3.5, step=0.1)
b = var5.number_input("Maximum price level (from 1-5 with 1 being the lowest and 5 being the highest)", min_value=1, max_value=5, step=1)
location = var6.text_input("Enter your location or leave blank to use your current location")
enter_button = var7.button(label='Enter!')

if enter_button: 
    api_key = backend.decode_api_key(const.ENCODED_GOOGLE_API_KEY)
    if location == "":
        location = backend.get_user_entered_loc(location)
            
    latitude, longitude = backend.get_latitude_and_longitude(location)
    meteostat_api_response = backend.call_meteostat_api(latitude,longitude,date,time)
            
    queries = backend.basic_rules(meteostat_api_response, location)
    google_api_response = backend.call_google_api(const.GOOGLE_MAPS_API, queries, api_key, 'opening_hours', latitude, longitude, r, b)

    var1.empty()
    var2.empty()
    var3.empty()
    var4.empty()
    var5.empty()
    var6.empty()
    var7.empty()

    if google_api_response.empty:
        st.header('Oops! Looks like the weather is not favourable at your desired location :(')
    else:
        if math.isnan(meteostat_api_response) == True:
            st.header('The weather for your desired date is uncertain')
        if meteostat_api_response <= 2:
            st.header('The weather for your desired date is sunny :sun_with_face:')
        elif meteostat_api_response <= 5:
            st.header('The weather for your desired date is cloudy :cloud:')
        elif meteostat_api_response <= 11 or meteostat_api_response == 17 or meteostat_api_response == 18:
            st.header('The weather for your desired date is rainy :rain_cloud:')
        elif meteostat_api_response == 14 or meteostat_api_response == 15 or meteostat_api_response == 21:
            st.header('The weather for your desired date is snowy :snowman:')

        st.subheader('Here are our recommendations!')
        for query in queries:
            st.subheader(query.split(' in')[0])
            df = google_api_response[google_api_response['Query']==query]
            st.write(df)

