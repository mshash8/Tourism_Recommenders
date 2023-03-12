import unittest
import backend as backend


class TestBackend(unittest.TestCase):
    def test_call_google_api_smoke_test(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        query = "Tourist places to visit in Seattle"
        api_key = 'AIzaSyDvXY6zrSDLbP_uNCc7UV1zWqobtkk0l7A'
        fields = 'opening_hours'
        google_api_response = backend.call_google_api(url, query, api_key, fields)
        self.assertTrue(True)

if __name__ == "__main__":
   unittest.main()