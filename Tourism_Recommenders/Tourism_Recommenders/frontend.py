"""
Frontend code for the Weather Integrated Tourism Recommendation System

This script looks into the frontend of the code where user inputs like
preference, date and time of travel, preferred minimum rating,
preferred maximum price level, and location are taken. These variables
are then used to call the backend module and fetch a list of
recommendations which are then showed as an output to the user.

The script requires that the 'pandas', 'streamlit' and 'const' packages
be installed within the Python environment this script is being run in.
This script also imports the 'backend' module to execute the program.

"""

import pandas as pd
import streamlit as st
from Tourism_Recommenders import const
from Tourism_Recommenders import backend


st.set_page_config(layout = "wide")

var = st.empty()

#create a container that takes user inputs
with var.container():
    st.header(":blue[ANITA: Weather Integrated Tourism Recommendation System]")
    pref = st.selectbox(':violet[Do you have any particular preference for a\
                        place?]', ('None', 'Beaches', 'Cafes and Restaurants',
                        'Hikes and Trails', 'Indoor Activities', 'Museums',
                        'Outdoor Activities', 'Parks and Botanical Gardens'))
    date = st.date_input(':violet[When do you wish to visit?] (To get more\
                         accurate results based on weather predictions, please\
                         enter a date that is not beyond 2-3 days from today.\
                         Due to the limitations in our weather dataset, dates\
                         beyond 8 days from today are invalid!)')
    time = st.time_input(":violet[What time do you wish to visit?]")
    rating = st.number_input(":violet[Minimum rating you want from 1-5]",
                            min_value = 0.0, max_value = 5.0, value = 3.5,
                            step = 0.1)
    price = st.number_input(":violet[Maximum price level] (From 1-5 with 1\
                            being the lowest and 5 being the highest)",
                            min_value = 1, max_value = 5, value = 3, step = 1)
    location = st.text_input(":violet[Enter your location or leave blank to\
                             use your current location] (Permissible\
                             characters are uppercase english letters [A-Z],\
                             lowercase english letters [a-z], digits [0-9],\
                             and commas [,])")
    enter_button = st.button(label='Enter!')

var.container()

if enter_button:

    var.empty()
    return_button = st.button(label='Return')

    #check for exceptions
    backend.check_date_invalid(date, time)
    backend.check_address_characters(location)
    backend.check_address_invalid(location)

    if return_button:
        var.container()
    else:
        api_key = backend.decode_api_key(const.ENCODED_GOOGLE_API_KEY)

        if location.strip() == "":
            location = backend.get_user_entered_loc()
        else:
            pass

        latitude, longitude = backend.get_latitude_and_longitude(location)
        meteostat_api_response = backend.call_meteostat_api(latitude,
                                                            longitude, date,
                                                            time)

        queries = backend.basic_rules(meteostat_api_response, location)

        PREF = str(pref) + " in " + str(location)
        personal_pref = [PREF]

        #fetch places based on weather recommendations
        google_api_response = backend.call_google_api(const.GOOGLE_MAPS_API,
                                                    queries, api_key,
                                                    'opening_hours.periods',
                                                    latitude, longitude,
                                                    rating, price)

        #fetch places if the user inputs that they have a preference
        if pref != 'None':
            pref_df = backend.call_google_api(const.GOOGLE_MAPS_API,
                                            personal_pref, api_key,
                                            'opening_hours', latitude,
                                            longitude, rating, price)
        else:
            pref_df = pd.DataFrame()

        #write header based on the weather condition
        if google_api_response.empty:
            st.header('Oops! Looks like the weather is not favourable for\
                      your desired date and location :(')
        else:
            if meteostat_api_response == 0:
                st.header(":blue[The weather for your desired date is\
                          uncertain. But don't worry! We got you :)]")
            elif meteostat_api_response <= 2:
                st.header(':blue[The weather for your desired date is sunny\
                        :sun_with_face:]')
            elif meteostat_api_response <= 5:
                st.header(':blue[The weather for your desired date is cloudy\
                        :cloud:]')
            elif meteostat_api_response <= 11 or meteostat_api_response == 17\
                or meteostat_api_response == 18:
                st.header(':blue[The weather for your desired date is rainy\
                        :rain_cloud:]')
            elif meteostat_api_response in (14, 15, 21):
                st.header(':blue[The weather for your desired date is snowy\
                        :snowman:]')

        #output when the user has a particular preference
        if pref != 'None' and not google_api_response.empty:
            st.header(':violet[Here are some recommendations based on your\
                    preference!]')
            if  'Beaches' in pref:
                st.subheader(f"""**{pref}** :beach_with_umbrella:""")
            elif  'Botanical Gardens' in pref:
                st.subheader(f"""**{pref}** :herb:""")
            elif  'Cafes' in pref:
                st.subheader(f"""**{pref}** :cake:""")
            elif  'Hikes' in pref:
                st.subheader(f"""**{pref}** :national_park:""")
            elif  'Indoor Activities' in pref:
                st.subheader(f"""**{pref}** :house_buildings:""")
            elif  'Museums' in pref:
                st.subheader(f"""**{pref}** :classical_building:""")
            elif  'Outdoor Activities' in pref:
                st.subheader(f"""**{pref}** :running:""")
            elif  'Parks' in pref:
                st.subheader(f"""**{pref}** :deciduous_tree:""")
            else:
                st.subheader(f"""**{pref}** :fork_and_knife:""")

            pref_df = pref_df.head(3)
            for _, row in pref_df.iterrows():
                st.markdown(f""":violet[{row['name']}]""")
                st.markdown(f"""Address: {row['formatted_address']}""")
                st.markdown(f"""Rating: {row['rating']}""")
                st.markdown(f"""Distance: Approximately {row['Distance']}\
                        miles away  \n """)
            st.write("  \n ")
        else:
            pass

        #output based on the tool's recommendations
        if google_api_response.empty is False:
            st.header(':violet[Here are some recommendations from us!]')
            for query in queries:
                if query.split(' in')[0] not in PREF:
                    if  'Beaches' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :beach_with_umbrella:""")
                    elif  'Botanical Gardens' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :herb:""")
                    elif  'Cafes' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :cake:""")
                    elif  'Hikes' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :national_park:""")
                    elif  'Indoor Activities' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :house_buildings:""")
                    elif  'Museums' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :classical_building:""")
                    elif  'Outdoor Activities' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :running:""")
                    elif  'Parks' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :deciduous_tree:""")
                    else:
                        st.subheader(f"""**{query.split(' in')[0]}**\
                            :fork_and_knife:""")
                else:
                    continue

                df = google_api_response[google_api_response['Query']==query]
                df = df.head(3)
                for _, row in df.iterrows():
                    st.markdown(f""":violet[{row['name']}]""")
                    st.markdown(f"""Address: {row['formatted_address']}""")
                    st.markdown(f"""Rating: {row['rating']}""")
                    st.markdown(f"""Distance: Approximately {row['Distance']}\
                          miles away  \n """)
                st.write("  \n ")
        else:
            pass
