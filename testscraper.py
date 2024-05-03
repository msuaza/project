import unittest
import requests
from script import fetch_weather_page

class TestWebScraping(unittest.TestCase):
    def test_fetch_weather_page(self):
        url = "https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168"
        content = fetch_weather_page(url)
        self.assertIn('Current conditions at', content)

    def test_api_response(self):
        response = requests.get("https://weather-api-3oom.onrender.com/temperature_trends")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/png')

if __name__ == '__main__':
    unittest.main()
