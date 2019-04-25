# Standard Python Library
import calendar
import datetime
import logging.config
import numpy as np
import os
import pandas as pd
import random
from dateutil import tz

# Custom Python Library
from common.config import LoggingConfig
from generator.generate_baseline_data import get_gis_historical_data, aggregate_gis_historical_data
from common.utils import get_file_path, get_config, get_city

# Load logging.yaml file
logging.config.dictConfig(LoggingConfig.logging_config)

class WeatherDataGen(object):
    """This class generates the weather data based on the baseline
    historical data.
    """

    def __init__(self, number_simulated_data, generate_baseline_flag=False):

        logging.info("Initialising WeatherDataGen class.")
        
        # Determine that number_simulated_data is more than 0.
        if number_simulated_data<1:
            logging.error("The number of simulated data is less than 1. Value: {}.".format(number_simulated_data))
            raise ValueError
        
        # Retrieve configuration data.
        self.config_data = get_config()
        self.__number_simulated_data = number_simulated_data
        self.__generate_baseline_flag = generate_baseline_flag
        self.__locations = [get_city(loc) for loc in self.config_data["location"]]
        self.__output_cols = self.config_data["simulation"]["output_columns"]
        self.__date_start_orig = self.config_data["simulation"]["date_start"]
        self.__date_end_orig = self.config_data["simulation"]["date_end"]
        self.__date_start = datetime.datetime.combine(self.__date_start_orig, datetime.time.min).timestamp()
        self.__date_end = datetime.datetime.combine(self.__date_end_orig, datetime.time.min).timestamp()
        
        # Get the baseline reference and aggregate file path.
        self.__output_base_reference_file_path = get_file_path(folder_name="data"
                                                ,subdirectory=self.config_data["gis"]["output_subdirectory"]
                                                ,file_name=self.config_data["gis"]["output_base_reference_file_name"])
        self.__output_base_aggregate_file_path = get_file_path(folder_name="data"
                                                ,subdirectory=self.config_data["gis"]["output_subdirectory"]
                                                ,file_name=self.config_data["gis"]["output_base_aggregate_file_name"])
        
        logging.info("Checking if the baseline data set exists.")
        
        # Checking if the baseline data set exists.
        if self.__generate_baseline_flag:
            get_gis_historical_data()
            aggregate_gis_historical_data()
            
        elif not os.path.exists(self.__output_base_reference_file_path) or not os.path.exists(self.__output_base_aggregate_file_path):
            logging.info("Baseline data set does not exists. Generating baseline data.")
            get_gis_historical_data()
            aggregate_gis_historical_data()
        
        else:
            logging.info("Baseline data sets exists.")
        
        # Reading baseline data sets.
        logging.info("Reading baseline reference data.")
        self.__reference_data = pd.read_csv(self.__output_base_reference_file_path)
        logging.info("Completed reading baseline reference data.")
        
        logging.info("Reading baseline aggregate data.")
        self.__aggregate_data = pd.read_csv(self.__output_base_aggregate_file_path)
        logging.info("Completed reading baseline aggregate data.")
        
        logging.info("Initialising output_data data frame.")
        
        # Check if the location in the config file reconfiles with the baseline data.
        if len(set(self.__reference_data["Location"]).difference(set(self.__locations)))!=0:
            logging.info("Baseline data set does not exists. Generating baseline data.")
            get_gis_historical_data()
            aggregate_gis_historical_data()
        
        # Initialising output_data dataframe.
        self.output_data = pd.DataFrame(columns=self.__output_cols)
        
        logging.info("Completed initialising WeatherDataGen class.")
        
    def __generate_location(self):
        """This function generates n random location to be simulated.
        """
        
        logging.info("Generating {} random location(s).".format(self.__number_simulated_data))
        
        # Randomly generate location list.
        self.output_data["Location"] = np.random.choice(self.__locations, self.__number_simulated_data)
        
        logging.info("Completed generating {} random location(s).".format(self.__number_simulated_data))
    
    def __merge_ref_data(self):
        """This function merges the output data with baseline reference data.
        """
        
        logging.info("Merging the output data with baseline reference data.")
        
        # Merging the output data with baseline reference data.
        self.output_data = pd.merge(self.output_data.drop(["Position"], axis=1)
                                   ,self.__reference_data
                                   ,how="inner", on="Location")
        
        logging.info("Completed merging the output data with baseline reference data.")
                                   
    def __merge_aggregate_data(self):
        """This function merges the output data with baseline aggregate data.
        """
        
        logging.info("Merging the output data with baseline aggregate data.")
        
        # Merging the output data with baseline aggregate data.
        self.output_data = pd.merge(self.output_data
                                   ,self.__aggregate_data
                                   ,how="inner", on=["Location", "Month"])
        
        logging.info("Completed merging the output data with baseline aggregate data.")
        
    def __generate_timestamp(self):
        """This function generates random timestamp in ISO8601 format.
        """
        
        logging.info("Generating timestamp data for the output data between {} and {}.".format(self.__date_start_orig, self.__date_end_orig))
        
        # Randomly generate timestamp data.
        temp_tz = np.random.randint(self.__date_start, self.__date_end, size=self.__number_simulated_data)
        temp_tz = pd.to_datetime(temp_tz, unit="s", utc=True).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Updating the output data with the timestamp.
        self.output_data["Local Time"] = temp_tz
        self.output_data["Month"] = pd.to_datetime(self.output_data["Local Time"], utc=True).dt.month
        
        logging.info("Completed generating timestamp data for the output data.")
        
    def __generate_weather_variables(self):
        """This function generates the weather variables and updates
        output_data variable.
        """

        # Initialiase weather variable data.
        
        logging.info("Initialising weather variable data.")
        
        condition_value = self.config_data["simulation"]["condition"]
        condition_dict = dict(zip(np.arange(1,len(condition_value)+1),condition_value))
        conditions = np.random.randint(1, len(condition_value), size=self.__number_simulated_data)
        
        temperature = np.random.uniform(low=0.0, high=1.0, size=self.__number_simulated_data)
        pressure = np.random.uniform(low=0.0, high=1.0, size=self.__number_simulated_data).round(1)
        humidity = np.random.uniform(low=0.0, high=1.0, size=self.__number_simulated_data)

        logging.info("Completed initialising weather variable data.")

        # Generating weather condition data and updating the output data dataframe.
        logging.info("Generating weather condition data.")
        
        self.output_data["Conditions"] = conditions
        self.output_data["Conditions"] = self.output_data.Conditions.map(condition_dict)

        logging.info("Completed updating the output data with the generated weather condition data.")

        # Generating temperature data and updating the output data dataframe.
        logging.info("Generating temperature data.")
        
        self.output_data["Temperature"] = self.output_data["T_avg_min"] + self.output_data["T_avg_range"] * temperature
        self.output_data["Temperature"] = self.output_data["Temperature"].round(1)
        self.output_data.loc[self.output_data["Temperature"]>0, "Temperature"] = "+" + self.output_data[self.output_data["Temperature"]>0]["Temperature"].astype(str)

        logging.info("Completed updating the output data with the generated temperature data.")
        
        # Generating pressure data and updating the output data dataframe.
        logging.info("Generating pressure data.")
        
        self.output_data["Pressure"] = self.output_data["P_min"] + self.output_data["P_range"] * pressure
        self.output_data["Pressure"] = self.output_data["Pressure"].round(1)

        logging.info("Completed updating the output data with the generated pressure data.")
        
        # Generating humidity data and updating the output data dataframe.
        logging.info("Generating humidity data.")
        
        self.output_data["Humidity"] = self.output_data["H_min"] + self.output_data["H_range"] * humidity
        self.output_data["Humidity"] = self.output_data["Humidity"].astype("int")

        logging.info("Completed updating the output data with the generated humidity data.")
        
    def __finalise_output(self):
        """This function cleanses the output_data layout.
        """

        # Finalising output_data layout.
        
        logging.info("Finalising output_data layout.")
        
        self.output_data = self.output_data[self.__output_cols]
        
        logging.info("Completed finalising output_data layout.")
        
    def save_output(self):
        """This function saves the output_data in the data folder.
        """

        # Initialise variable
        file_path = get_file_path(folder_name="data"
                                 ,subdirectory=self.config_data["simulation"]["output_subdirectory"]
                                 ,file_name=self.config_data["simulation"]["output_data"])
        
        # Saving output_data in a csv file.
        
        logging.info("Saving output_data in {}.".format(file_path))
        
        self.output_data.to_csv(file_path
                        ,sep=self.config_data["simulation"]["output_delimiter"]
                        ,header=self.config_data["simulation"]["output_header"]
                        ,index=False)
        
        logging.info("Completed saving output_data in {}.".format(file_path))

    def generate(self):
        """This function runs the simulated weather data and save in 
        the output_data dataframe.
        """
    
        logging.info("Running weather data generation.")
        
        # Running the private methods to simulated weather data.
        self.__generate_location()
        self.__merge_ref_data()
        self.__generate_timestamp()
        self.__merge_aggregate_data()
        self.__generate_weather_variables()
        self.__finalise_output()
        
        logging.info("Completed running weather data generation.")

