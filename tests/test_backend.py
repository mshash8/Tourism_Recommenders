'''
This is the unit test file for the code.
'''
import unittest
from datetime import datetime
from Tourism_Recommenders.backend import call_google_api, call_meteostat_api, decode_api_key, \
get_latitude_and_longitude, get_user_entered_loc, basic_rules, check_date_invalid, \
check_address_invalid, check_address_characters, haversine
import Tourism_Recommenders.const as const


class TestBackend(unittest.TestCase):
    '''
    Class to conduct unit tests for the backend functions
    '''
    def test_call_google_api(self):
        '''
        tests the working of the call_google_api function
        '''
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        query = "Tourist places to visit in Seattle"
        api_key = 'AIzaSyDvXY6zrSDLbP_uNCc7UV1zWqobtkk0l7A'
        fields = 'opening_hours'
        lat = 47.6062
        longi = 122.3321
        rating = 3
        price = 2
        call_google_api(url, query, api_key, fields, lat, longi, rating, price)
        self.assertTrue(True)


    def test_call_meteostat_api(self):
        '''
        tests the working of the call_meteostat_api function
        '''
        latitude = 47.6062
        longitude = 122.3321
        date = "2023-03-12"
        time = "17:02:00"
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time, '%H:%M:%S').time()
        call_meteostat_api(latitude, longitude, date_obj, time_obj)
        self.assertTrue(True)

    def test_decode_api_key(self):
        '''
        tests the working of the decode_api_key function
        '''
        api_key = const.ENCODED_GOOGLE_API_KEY
        decode_api_key(api_key)
        self.assertTrue(True)


    def test_get_latitude_and_longitude(self):
        '''
        tests the working of the get_latitude_and_longitude function
        '''
        location = "Seattle"
        get_latitude_and_longitude(location)
        self.assertTrue(True)

    def test_get_user_entered_loc(self):
        '''
        tests the working of the get_user_entered_loc function
        '''
        get_user_entered_loc()
        self.assertTrue(True)

    def test_basic_rules(self):
        '''
        tests the working of the basic_rules function
        '''
        defining_weather = 2
        location = "Seattle"
        basic_rules(defining_weather, location)
        self.assertTrue(True)

    #Edge Tests
    def test_edge_correct_date(self):
        """
        This function performs an edge test to check how the program
        works when one goes "off script". This test accounts for the
        case where the entered date and time belongs to a past date or
        the entered date is beyond 8 days from the current date.

        """
        date = "2023-03-10"
        time = "17:02:00"
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time, '%H:%M:%S').time()
        with self.assertRaises(ValueError):
            check_date_invalid(date_obj, time_obj)

    def test_edge_address_validity(self):
        """
        This function performs an edge test to check how the program
        works when one goes "off script". This test accounts for the
        case where the entered address is invalid and does not exist
        in the google maps api dataset.

        """
        location_as_string = "Csdgfsdg"
        with self.assertRaises(ValueError):
            check_address_invalid(location_as_string)

    def test_edge_address_char_validity(self):
        """
        This function performs an edge test to check how the program
        works when one goes "off script". This test accounts for the
        case where the entered address has invalid characters i.e.
        anything other than english letters, digits, or commas.
        """
        location_as_string = "2$ Capitol Hill^"
        with self.assertRaises(ValueError):
            check_address_characters(location_as_string)

    def test_check_haversine_fn(self):
        '''
        Should return 0 as both the locations are the same.
        '''
        lat1 = 47.6062
        long1 = 122.3321
        lat2 = 47.6062
        long2 = 122.3321
        dist = haversine(lat1, long1, lat2, long2)
        self.assertAlmostEqual(dist, 0)

if __name__ == "__main__":
    unittest.main()