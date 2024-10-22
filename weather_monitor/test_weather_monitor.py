import unittest
from unittest.mock import patch
import weather_monitor
import os

class TestWeatherMonitor(unittest.TestCase):

    def setUp(self):
        # Reset the WEATHER_DATA and DAILY_SUMMARIES before each test
        weather_monitor.WEATHER_DATA = []
        weather_monitor.DAILY_SUMMARIES = []

    @patch('weather_monitor.requests.get')
    def test_fetch_weather_data_success(self, mock_get):
        # Mocking a successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'main': {
                'temp': 300,  # Kelvin
                'feels_like': 305  # Kelvin
            },
            'weather': [{'main': 'Clear'}],
            'dt': 1609459200  # Example timestamp
        }
        
        weather_monitor.fetch_weather_data('Delhi')
        
        self.assertEqual(len(weather_monitor.WEATHER_DATA), 1)
        self.assertEqual(weather_monitor.WEATHER_DATA[0]['city'], 'Delhi')
        self.assertAlmostEqual(weather_monitor.WEATHER_DATA[0]['temperature'], 26.85, places=2)  # 300K to Celsius
        self.assertAlmostEqual(weather_monitor.WEATHER_DATA[0]['feels_like'], 31.85, places=2)  # 305K to Celsius
        self.assertEqual(weather_monitor.WEATHER_DATA[0]['weather_condition'], 'Clear')

    @patch('weather_monitor.requests.get')
    def test_fetch_weather_data_failure(self, mock_get):
        # Mocking a failed API response
        mock_get.return_value.status_code = 404
        
        weather_monitor.fetch_weather_data('Delhi')
        
        self.assertEqual(len(weather_monitor.WEATHER_DATA), 0)  # Data should not be added

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(weather_monitor.kelvin_to_celsius(273.15), 0, places=2)
        self.assertAlmostEqual(weather_monitor.kelvin_to_celsius(300), 26.85, places=2)

    def test_process_daily_summary(self):
        # Preparing mock data
        weather_monitor.WEATHER_DATA = [
            {'city': 'Delhi', 'temperature': 30, 'weather_condition': 'Clear'},
            {'city': 'Delhi', 'temperature': 32, 'weather_condition': 'Clear'},
            {'city': 'Mumbai', 'temperature': 28, 'weather_condition': 'Rain'},
            {'city': 'Mumbai', 'temperature': 29, 'weather_condition': 'Rain'},
            {'city': 'Chennai', 'temperature': 35, 'weather_condition': 'Sunny'},
        ]

        weather_monitor.process_daily_summary()
        
        self.assertEqual(len(weather_monitor.DAILY_SUMMARIES), 1)
        daily_summary = weather_monitor.DAILY_SUMMARIES[0]
        self.assertAlmostEqual(daily_summary['Delhi']['avg_temp'], 31, places=2)
        self.assertEqual(daily_summary['Mumbai']['dominant_weather'], 'Rain')
        self.assertEqual(daily_summary['Chennai']['max_temp'], 35)

    @patch('weather_monitor.plt.savefig')
    def test_visualize_data(self, mock_savefig):
        # Preparing mock data
        weather_monitor.DAILY_SUMMARIES = [{
            'Delhi': {
                'avg_temp': 31,
                'max_temp': 32,
                'min_temp': 30,
                'summary_time': '2024-10-19'
            }
        }]
        
        weather_monitor.visualize_data()
        
        # Check if the savefig was called
        self.assertTrue(mock_savefig.called)

    @patch('builtins.print')
    def test_check_alert_thresholds(self, mock_print):
        weather_monitor.WEATHER_DATA = [
            {'city': 'Delhi', 'temperature': 36},
            {'city': 'Mumbai', 'temperature': 34}
        ]

        weather_monitor.check_alert_thresholds()
        mock_print.assert_called_once_with('ALERT: High temperature in Delhi! Current temperature: 36°C')

    def test_reset_data(self):
        weather_monitor.WEATHER_DATA = [{'city': 'Delhi', 'temperature': 30}]
        weather_monitor.reset_data()
        self.assertEqual(weather_monitor.WEATHER_DATA, [])

if __name__ == '__main__':
    # Clean up any generated files
    for city in weather_monitor.CITY_LIST:
        filename = f"{city}_summary_2024-10-19.png"
        if os.path.exists(filename):
            os.remove(filename)

    unittest.main()
