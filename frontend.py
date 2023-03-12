"""
Modeule docstring
    
"""

import pandas as pd
import streamlit as st
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
                      ('None', 'Beaches', 'Cafes and Restaurants',
                       'Hikes and Trails', 'Indoor Activities', 'Museums', 
                       'Outdoor Activities', 'Parks and Botanical Gardens'))
date = var2.date_input('When do you wish to visit? (To get more accurate\
                       results, please enter a date that is not beyond 2-3\
                       days from today. Dates beyond 8 days from today are\
                       invalid!)')
time = var3.time_input("What time do you wish to visit?")
rating = var4.number_input("Minimum rating you want from 1-5", min_value =
                           0.0, max_value = 5.0, value = 3.5, step = 0.1)
price = var5.number_input("Maximum price level (from 1-5 with 1 being the\
                          lowest and 5 being the highest)", min_value = 1,
                          max_value = 5, step = 1)
location = var6.text_input("Enter your location or leave blank to use your\
                           current location")
enter_button = var7.button(label='Enter!')

if enter_button:

    api_key = backend.decode_api_key(const.ENCODED_GOOGLE_API_KEY)
    if location == "":
        location = backend.get_user_entered_loc(location)

    latitude, longitude = backend.get_latitude_and_longitude(location)
    meteostat_api_response = backend.call_meteostat_api(latitude, longitude,
                                                        date, time)

    queries = backend.basic_rules(meteostat_api_response, location)
    PREF = str(pref) + " in " + str(location)
    personal_pref = [PREF]

    google_api_response = backend.call_google_api(const.GOOGLE_MAPS_API,
                                                  queries, api_key,
                                                  'opening_hours', latitude,
                                                  longitude, rating, price)
    if pref != 'None':
        pref_df = backend.call_google_api(const.GOOGLE_MAPS_API,
                                          personal_pref, api_key,
                                          'opening_hours', latitude,
                                          longitude, rating, price)
    else:
        pref_df = pd.DataFrame()

    var1.empty()
    var2.empty()
    var3.empty()
    var4.empty()
    var5.empty()
    var6.empty()
    var7.empty()

    if google_api_response.empty:
        st.header('Oops! Looks like the weather is not favourable for your\
                  desired date and location :(')
    else:
        if meteostat_api_response == 0:
            st.header(":blue[The weather for your desired date is uncertain.\
                      Don't worry! We got you :)]")
        elif meteostat_api_response <= 2:
            st.header(':blue[The weather for your desired date is sunny\
                      :sun_with_face:]')
        elif meteostat_api_response <= 5:
            st.header(':blue[The weather for your desired date is cloudy\
                      :cloud:]')
        elif meteostat_api_response <= 11 or meteostat_api_response == 17 or\
            meteostat_api_response == 18:
            st.header(':blue[The weather for your desired date is rainy\
                      :rain_cloud:]')
        elif meteostat_api_response == 14 or meteostat_api_response == 15 or\
            meteostat_api_response == 21:
            st.header(':blue[The weather for your desired date is snowy\
                      :snowman:]')

    if pref != 'None':
        st.header('Here are some recommendations based on your preference!')
        st.subheader(pref)
        st.write(pref_df.head(5))
    else:
        pass

    if google_api_response.empty is False:
        st.header('Here are some recommendations from us!')
        for query in queries:
            if query.split(' in')[0] in PREF:
                continue
            st.subheader(query.split(' in')[0])
            df = google_api_response[google_api_response['Query']==query]
            df = df.head(5)
            st.write(df)
    else:
        pass
