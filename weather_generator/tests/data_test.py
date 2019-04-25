# Standard Python Library
import unittest
import datetime
import pandas as pd

# Custom Python Library
from generator.weather_data_generator import WeatherDataGen
from common.utils import get_file_path, get_config, get_city

class DataTestCase(unittest.TestCase):

    def setUp(self):

        self.config_data = get_config()
        self.number_simulated_data = 100
        self.date_start = datetime.datetime.combine(self.config_data["simulation"]["date_start"], datetime.time.min).timestamp()
        self.date_end = datetime.datetime.combine(self.config_data["simulation"]["date_end"], datetime.time.min).timestamp()
        self.output_base_reference_file_path = get_file_path(folder_name="data"
                                                ,subdirectory=self.config_data["gis"]["output_subdirectory"]
                                                ,file_name=self.config_data["gis"]["output_base_reference_file_name"])
        self.output_base_historical_file_path = get_file_path(folder_name="data"
                                                ,subdirectory=self.config_data["gis"]["output_subdirectory"]
                                                ,file_name=self.config_data["gis"]["output_base_historical_file_name"])
        self.output_base_aggregate_file_path = get_file_path(folder_name="data"
                                                ,subdirectory=self.config_data["gis"]["output_subdirectory"]
                                                ,file_name=self.config_data["gis"]["output_base_aggregate_file_name"])
        self.generator = WeatherDataGen(number_simulated_data=self.number_simulated_data)
        self.reference_data = pd.read_csv(self.output_base_reference_file_path)
        self.historical_data = pd.read_csv(self.output_base_historical_file_path)
        self.aggregate_data = pd.read_csv(self.output_base_aggregate_file_path)
        self.locations = [get_city(loc) for loc in self.config_data["location"]]
        self.output_cols = self.config_data["simulation"]["output_columns"]
        self.generator = WeatherDataGen(number_simulated_data=self.number_simulated_data)
        self.generator.generate()

    def test_number_reference_data(self):
        """Checks if the number of reference data is the same as the
        number of locations in the config.yaml. This also tests for duplicate.
        """
        self.assertEqual(len(set(self.config_data["location"])), self.reference_data.shape[0])

    def test_number_historical_data(self):
        """Checks if the number of historical data is the same as the
        'number of locations * sample number * 12' in the config.yaml.
        """
        self.assertEqual(len(self.config_data["location"])*self.config_data["gis"]["sampling_number"]*12
                        ,self.historical_data.shape[0])

    def test_number_simulated_data(self):
        """Checks if the number of historical data is the same as the
        number_simulated_data.
        """
        self.assertEqual(self.number_simulated_data, self.generator.output_data.shape[0])

    def test_min_latitude(self):
        """Checks if the minimum latitude is not less than -90.
        """
        self.assertGreater(self.reference_data["Latitude"].min(), -90)

    def test_max_latitude(self):
        """Checks if the maximum latitude is not more than 90.
        """
        self.assertLess(self.reference_data["Latitude"].max(), 90)

    def test_min_longitude(self):
        """Checks if the minimum longitude is not less than -180.
        """
        self.assertGreater(self.reference_data["Longitude"].min(), -180)

    def test_max_longitude(self):
        """Checks if the maximum longitude is not more than 180.
        """
        self.assertLess(self.reference_data["Longitude"].max(), 180)

    def test_min_elevation(self):
        """Checks if the minimum elevation is not less than 0.
        """
        self.assertGreaterEqual(self.reference_data["Longitude"].min(), 0)

    def test_min_humidity(self):
        """Checks if the minimum humidity is not less than 0.
        """
        self.assertGreaterEqual(self.historical_data["Humidity"].min(), 0)

    def test_max_humidity(self):
        """Checks if the maximum humidity is not more than 100.
        """
        self.assertLessEqual(self.historical_data["Humidity"].max(), 100)

    def test_conditions(self):
        """Checks if the generated conditions have valid values.
        """
        
        valid_conditions = set(self.config_data["simulation"]["condition"])
        simulated_data = set(self.generator.output_data["Conditions"])

        self.assertTrue(set(simulated_data).difference(valid_conditions) == set())

    def test_min_temperature(self):
        """Checks if the minimum temperature is not less than −273.15.
        This is based on the absolute temperature in deg Celsius.
        """
        
        temperature = self.generator.output_data["Temperature"].astype(float).min()
        
        self.assertGreaterEqual(temperature, -273.15)

    def test_max_temperature(self):
        """Checks if the maximum temperature is not more than 58.
        This is based on the highest recorded temperature found in Libya.
        Reference:
        http://coolcosmos.ipac.caltech.edu/ask/63-What-are-the-highest-and-lowest-temperatures-on-Earth-
        """
        temperature = self.generator.output_data["Temperature"].astype(float).max()
        
        self.assertLessEqual(temperature, 58)

    def test_local_time_iso8601_format(self):
        """Checks if the local time is in ISO8601 format.
        """
        
        for value in self.generator.output_data["Local Time"]:
            self.assertTrue(datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ"))

if __name__ == '__main__':
    unittest.main()