"""
Code Testing for the Weather Integrated Tourism Recommendation System

This script has a class named TestBackend with several functions inside
it to check the working of the backend code for the tool.

The script requires that 'unittest' and 'datetime' module from the
datetime package be installed within the Python environment this script
is being run in.

This script also imports the backend and const modules from the
recommendation_engine package to call various functions.

"""
import unittest
from datetime import datetime
from Tourism_Recommenders.backend import\
call_google_api, call_meteostat_api, decode_api_key,\
get_latitude_and_longitude, get_user_entered_loc, basic_rules,\
check_date_invalid, check_address_invalid, check_address_characters, haversine
import Tourism_Recommenders.const as const


class TestBackend(unittest.TestCase):
    """
    This class has multiple functions defined under it where each
    function performs a particular test to check the working of the
    overall program. These tests include smoke tests, one-shot tests,
    and edge tests.

    """
    #Smoke Test
    def test_call_google_api(self):
        """
        This function checks if the Google API function runs when it is
        called. This helps find basic and critical issues before moving
        on to the other types of testing.

        """
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
        """
        This function checks if the Meteostat API function runs when it
        is called. This helps find basic and critical issues before
        moving on to the other types of testing.

        """
        latitude = 47.6062
        longitude = 122.3321
        date = "2023-03-12"
        time = "17:02:00"
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time, '%H:%M:%S').time()
        call_meteostat_api(latitude, longitude, date_obj, time_obj)
        self.assertTrue(True)

    def test_decode_api_key(self):
        """
        This function checks if the API key is being decoded when
        called. This helps find basic and critical issues before moving
        on to the other types of testing.

        """
        api_key = const.ENCODED_GOOGLE_API_KEY
        decode_api_key(api_key)
        self.assertTrue(True)

    def test_get_latitude_and_longitude(self):
        """
        This function checks if the function to obtain latitude and
        longitude values runs when called. This helps find basic and
        critical issues before moving on to the other types of testing.

        """
        location = "Seattle"
        get_latitude_and_longitude(location)
        self.assertTrue(True)

    def test_get_user_entered_loc(self):
        """
        This function checks if the function to obtain the user's
        current location runs when called. This helps find basic and
        critical issues before moving on to the other types of testing.

        """
        get_user_entered_loc()
        self.assertTrue(True)

    def test_basic_rules(self):
        """
        This function checks if the function to obtain the search
        queries for the Google API using the weather condition codes
        runs when called. This helps find basic and critical issues
        before moving on to the other types of testing.

        """
        defining_weather = 2
        location = "Seattle"
        basic_rules(defining_weather, location)
        self.assertTrue(True)

    def test_basic_rules_avoid(self):
        """
        This function checks if the function to obtain the search
        queries for the Google API using the weather condition codes
        runs when called. This helps find basic and critical issues
        before moving on to the other types of testing. The expected
        output is []

        """
        defining_weather = 20
        location = "Seattle"
        query = basic_rules(defining_weather, location)
        self.assertEqual(query,[])

    #One-Shot Test
    def test_check_haversine_fn(self):
        """
        This function performs a one-shot test to ensure that the code
        is logically correct. The haversine function computes the
        distance between two coordinates. If the two coordinates are
        equal, the distance must be zero. Thus, the expected output is
        matched against the actual output.

        """
        lat1 = 47.6062
        long1 = 122.3321
        lat2 = 47.6062
        long2 = 122.3321
        dist = haversine(lat1, long1, lat2, long2)
        self.assertAlmostEqual(dist, 0)

    #Edge Tests
    def test_correct_date(self):
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

    def test_address_validity(self):
        """
        This function performs an edge test to check how the program
        works when one goes "off script". This test accounts for the
        case where the entered address is invalid and does not exist
        in the google maps api dataset.

        """
        location_as_string = "Csdgfsdg"
        with self.assertRaises(ValueError):
            check_address_invalid(location_as_string)

    def test_address_char_validity(self):
        """
        This function performs an edge test to check how the program
        works when one goes "off script". This test accounts for the
        case where the entered address has invalid characters i.e.
        anything other than english letters, digits, or commas.
        """
        location_as_string = "2$ Capitol Hill^"
        with self.assertRaises(ValueError):
            check_address_characters(location_as_string)


if __name__ == "__main__":
    unittest.main()
