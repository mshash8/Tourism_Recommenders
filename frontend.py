"""
Modeule docstring
    
"""

import pandas as pd
import streamlit as st
import const
import backend


st.set_page_config(layout = "wide")

var = st.empty()

with var.container():
    st.header(":blue[ANITA: Tourism Recommendation System]")
    pref = st.selectbox(':violet[Do you have any particular preference for a\
                        place?]', ('None', 'Beaches', 'Cafes and Restaurants',
                        'Hikes and Trails', 'Indoor Activities', 'Museums', 
                        'Outdoor Activities', 'Parks and Botanical Gardens'))
    date = st.date_input(':violet[When do you wish to visit?]  \nline (To get more\
                            accurate results based on weather predictions, please\
                            enter a date that is not beyond 2-3 days from today.\
                            Dates beyond 8 days from today are invalid!)')
    time = st.time_input(":violet[What time do you wish to visit?]")
    rating = st.number_input(":violet[Minimum rating you want from 1-5]",
                            min_value = 0.0, max_value = 5.0, value = 3.5,
                            step = 0.1)
    price = st.number_input(":violet[Maximum price level] (From 1-5 with 1\
                            being the lowest and 5 being the highest)",
                            min_value = 1, max_value = 5, value = 3, step = 1)
    location = st.text_input(":violet[Enter your location or leave blank to use\
                                your current location] (Permissible characters\
                                are uppercase english letters [A-Z], lowercase\
                                english letters [a-z], digits [0-9], and comma\
                                [,])")
    enter_button = st.button(label='Enter!')

var.container()

if enter_button:

    var.empty()
    return_button = st.button(label='Return')

    backend.check_date_invalid(date, time)
    backend.check_address_characters(location)
    backend.check_address_invalid(location)

    if return_button:
        var.container()
    else:
        api_key = backend.decode_api_key(const.ENCODED_GOOGLE_API_KEY)
        if location == "":
            location = backend.get_user_entered_loc()

        latitude, longitude = backend.get_latitude_and_longitude(location)
        meteostat_api_response = backend.call_meteostat_api(latitude, longitude,
                                                            date, time)

        queries = backend.basic_rules(meteostat_api_response, location)
        PREF = str(pref) + " in " + str(location)
        personal_pref = [PREF]

        google_api_response = backend.call_google_api(const.GOOGLE_MAPS_API,
                                                    queries, api_key,
                                                    'opening_hours.periods', latitude,
                                                    longitude, rating, price)
        if pref != 'None':
            pref_df = backend.call_google_api(const.GOOGLE_MAPS_API,
                                            personal_pref, api_key,
                                            'opening_hours', latitude,
                                            longitude, rating, price)
        else:
            pref_df = pd.DataFrame()

        if google_api_response.empty:
            st.header('Oops! Looks like the weather is not favourable for your\
                    desired date and location :(')
        else:
            if meteostat_api_response == 0:
                st.header(":blue[The weather for your desired date is uncertain.\
                        But don't worry! We got you :)]")
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

        if google_api_response.empty is False:
            st.header(':violet[Here are some recommendations from us!]')
            for query in queries:
                if query.split(' in')[0] in PREF:
                    continue
                else:
                    if  'Beaches' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :beach_with_umbrella:""")
                    elif  'Botanical Gardens' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :herb:""")
                    elif  'Cafes' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :cake:""")
                    elif  'Hikes' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :national_park:""")
                    elif  'Indoor Activities' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :house_buildings:""")
                    elif  'Museums' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :classical_building:""")
                    elif  'Outdoor Activities' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :running:""")
                    elif  'Parks' in query.split(' in')[0]:
                        st.subheader(f"""**{query.split(' in')[0]}** :deciduous_tree:""")
                    else:
                        st.subheader(f"""**{query.split(' in')[0]}** :fork_and_knife:""")

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
