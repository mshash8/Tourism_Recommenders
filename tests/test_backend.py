import unittest
from Tourism_Recommenders.backend import *


class TestBackend(unittest.TestCase):
    def test_call_google_api_smoke_test(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        query = "Tourist places to visit in Seattle"
        api_key = 'AIzaSyDvXY6zrSDLbP_uNCc7UV1zWqobtkk0l7A'
        fields = 'opening_hours'
        google_api_response = call_google_api(url, query, api_key, fields)
        self.assertTrue(True)

    def test_call_meteostat_api(self):
        latitude = 47.6062
        longitude = 122.3321
        date = "2023-03-12" 
        time = "17:02:00"
        meteostat_response = call_meteostat_api(latitude, longitude, date, time)
        self.assertTrue(True)

    def test_decode_api_key(self):
        api_key = const.ENCODED_GOOGLE_API_KEY 
        decoded_key = decode_api_key(api_key)
        self.assertTrue(True) 

    def test_get_latitude_and_longitude(self):
        location = "Seattle"
        get_latitude_and_longitude(location)
        self.assertTrue(True)

    def test_get_user_entered_loc(self):
        location_as_string = "Capitol Hill"
        loc = get_user_entered_loc(location_as_string)
        self.assertTrue(True)

    def test_get_current_loc(self):
        loc = get_current_loc()
        self.assertTrue(True) 

    def test_basic_rules(self):
        defining_weather = 2
        location = "Seattle"
        query = basic_rules(defining_weather, location)
        self.assertTrue(True) 

    #test to see whether exception is raised when date given is BEFORE current date
    def test_correct_date(self):
        latitude = 47.6062
        longitude = 122.3321
        date = "2023-03-10" 
        time = "17:02:00"
        with self.assertRaises(ValueError):
            call_meteostat_api(latitude, longitude, date, time)

    #test to see whether missing data is taken care of
    def test_for_missing_data(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        query = "Tourist places to visit in Seattle" ##PUT MISSING DATA QUERY
        api_key = 'AIzaSyDvXY6zrSDLbP_uNCc7UV1zWqobtkk0l7A'
        fields = 'opening_hours,price'
        google_api_response = call_google_api(url, query, api_key, fields)
        self.assertTrue(True) 

    def test_address_validity(self):
        location_as_string = "Csdgfsdg"
        with self.assertRaises(ValueError):
            loc = get_user_entered_loc(location_as_string)

    def test_address_char_validity(self):
        location_as_string = "2$ Capitol Hill^"
        with self.assertRaises(ValueError):
            loc = get_user_entered_loc(location_as_string)

if __name__ == "__main__":
   unittest.main()
