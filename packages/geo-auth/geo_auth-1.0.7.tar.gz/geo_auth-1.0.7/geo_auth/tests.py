from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import MagicMock

class ClientInfoViewTest(APITestCase):

    def setUp(self):
        # Mock the request data you need for the tests
        self.mock_request = MagicMock()

    def test_get_client_ip_auto(self):
        # Mocking the required attributes on the request object
        self.mock_request.ip_address = "102.89.47.71"
        self.mock_request.currency = "NGN"
        self.mock_request.location_data = {
            "country_code": "NG",
            "country": "Nigeria",
            "region": "Lagos",
            "city": "Oshodi",
            "latitude": "6.555040",
            "longitude": "3.343630",
            "zip_code": "102103",
            "timezone": "Africa/Lagos",
            "asn": "29465"
        }
        self.mock_request.country_info = {
            "continent": "AF",
            "capital": "Abuja",
            "languages": "en-NG,ha,yo,ig,ff",
            "geonameId": 2328926,
            "south": 4.27058531900002,
            "isoAlpha3": "NGA",
            "north": 13.885645000000068,
            "fipsCode": "NI",
            "population": "195874740",
            "east": 14.677982000000043,
            "isoNumeric": "566",
            "areaInSqKm": "923768.0",
            "countryCode": "NG",
            "west": 2.663560999000026,
            "countryName": "Nigeria",
            "postalCodeFormat": "######",
            "continentName": "Africa",
            "currencyCode": "NGN"
        }
        self.mock_request.device_info = {
            "device": "Other",
            "browser": "Chrome",
            "os": "Windows",
            "is_mobile": False,
            "is_tablet": False,
            "is_pc": True
        }

        # Call the view directly, passing the mocked request
        response = self.client.get('/api/location/', HTTP_X_FORWARDED_FOR='102.89.47.71')

        # Check if the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the mocked values
        self.assertEqual(response.data['client_ip'], '102.89.47.71')
        self.assertEqual(response.data['location_data']['location']['country_code'], 'NG')
        self.assertEqual(response.data['location_data']['location']['country'], 'Nigeria')
        self.assertEqual(response.data['location_data']['location']['region'], 'Lagos')
        self.assertEqual(response.data['location_data']['location']['city'], 'Oshodi')
        self.assertEqual(response.data['location_data']['location']['latitude'], '6.555040')
        self.assertEqual(response.data['location_data']['location']['longitude'], '3.343630')
        self.assertEqual(response.data['location_data']['location']['zip_code'], '102103')
        self.assertEqual(response.data['location_data']['location']['timezone'], 'Africa/Lagos')
        self.assertEqual(response.data['location_data']['location']['asn'], '29465')
        self.assertEqual(response.data['location_data']['country_info']['continent'], 'AF')
        self.assertEqual(response.data['location_data']['country_info']['capital'], 'Abuja')
        self.assertEqual(response.data['location_data']['country_info']['languages'], 'en-NG,ha,yo,ig,ff')
        self.assertEqual(response.data['location_data']['country_info']['countryName'], 'Nigeria')
        self.assertEqual(response.data['location_data']['country_info']['currencyCode'], 'NGN')
        
    def test_get_client_location_from_ip(self):
        # Mocking the required attributes
        self.mock_request.ip_address = "102.89.47.71"

        # Call the view directly
        response = self.client.get('/api/ip/', HTTP_X_FORWARDED_FOR='102.89.47.71')

        # Check if the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the mocked IP address
        self.assertEqual(response.data['client_ip'], '102.89.47.71')

    def test_get_client_device_info(self):
        # Mocking the required attributes
        self.mock_request.device_info = {
            "device": "Other",
            "browser": "Chrome",
            "os": "Windows",
            "is_mobile": False,
            "is_tablet": False,
            "is_pc": True
        }

        # Call the view directly
        response = self.client.get('/api/device/')

        # Check if the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the mocked device info
        self.assertEqual(response.data['device_info']['device'], 'Other')
        self.assertEqual(response.data['device_info']['browser'], 'Chrome')
        self.assertEqual(response.data['device_info']['os'], 'Windows')
        self.assertEqual(response.data['device_info']['is_mobile'], False)
        self.assertEqual(response.data['device_info']['is_tablet'], False)
        self.assertEqual(response.data['device_info']['is_pc'], True)
