# Standard Python Library
import datetime
import os
import pandas as pd
import unittest

# Custom Python Library
from generator.generate_baseline_data import get_elevation_data
from generator.weather_data_generator import WeatherDataGen
from common.utils import get_file_path, get_config, get_city

class TransformTestCase(unittest.TestCase):

    def setUp(self):

        self.config_data = get_config()

    def test_get_file_path_no_subdirectory(self):
        """Checks if the test_get_file_path can construct correct file path
        without subdirectory.
        """
        
        file_path = get_file_path(file_name="config.yaml", folder_name="config")
        
        self.assertTrue(os.path.exists(file_path))

    def test_get_file_path_with_subdirectory(self):
        """Checks if the test_get_file_path can construct correct file path
        with subdirectory.
        """
        
        file_path = get_file_path(file_name="gebco_08_rev_elev_A1_grey_geo.tif"
                                 ,folder_name="data"
                                 ,subdirectory="elevation")
        
        self.assertTrue(os.path.exists(file_path))

    def test_get_city(self):
        """Checks if the get_city method is able to extract the
        city name.
        """
        self.assertTrue(get_city("Sydney, Australia")=="Sydney")

    def test_get_elevation_data(self):
        """Checks if the get_elevation_data method is able to extract the
        elevation for Adelaide, Australia (-34.9281805,138.5999312).
        """
        self.assertEqual(get_elevation_data(-34.9281805,138.5999312), 2)

    def test_weather_data_generator_generate(self):
        """Checks if the generate method can generate 10 data points.
        """
        wdg = WeatherDataGen(number_simulated_data=10)
        wdg.generate()
        
        self.assertEqual(len(wdg.output_data), 10)


    def test_weather_data_generator_save_output(self):
        """Checks if the save_output method generate the csv file.
        """
        file_path = get_file_path(file_name=self.config_data["simulation"]["output_data"]
                                 ,folder_name="data"
                                 ,subdirectory="output")
                                 
        if os.path.exists(file_path):
          os.remove(file_path)

        wdg = WeatherDataGen(number_simulated_data=10)
        wdg.generate()
        wdg.save_output()
        
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()