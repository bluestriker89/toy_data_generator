# Toy Data Generator

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



This is a toy weather data generator that simulates atmosphere, topography, geography and oceanography that evolves over time. It generates measurements at various locations and times, and the program emit data, as in the following:

Location  | Position         | Local Time          | Conditions | Temperature | Pressure | Humidity
--------- | ---------------- | ------------------- | ---------- | -----------:| --------:| --------:
Sydney    | -33.86,151.21,39 | 2015-12-23 16:02:12 | Rain       |       +12.5 |   1010.3 | 98
Melbourne | -37.83,144.98,7  | 2015-12-25 02:30:55 | Snow       |        -5.3 |    998.4 | 52
Adelaide  | -34.92,138.62,48 | 2016-01-04 23:05:37 | Sunny      |       +39.4 |   1114.1 | 11

where

 - Location is an optional label describing one or more positions
 - Position is a comma-separated triple containing latitude, longitude, and
   elevation in metres above sea level
 - Local time is an ISO8601 date time
 - Conditions are either Snow, Rain, or Sunny
 - Temperature is in °C
 - Pressure is in hPa
 - Relative humidity is a %

## Getting Started

### Prerequisites
Make sure you have installed all of the following prerequisites on your machine:
 - Git - [Download & Install Git](https://git-scm.com/downloads). OSX and Linux machines typically have this already installed.
 - Python - [Download & Install Python](https://git-scm.com/downloads). It requires **Python 3.6.5 or above**.
 - Dark Skyp API - [Register & Generate API key](https://darksky.net/dev)

### Installation

Clone the git repository to your local machine using the command

```git
git clone https://github.com/bluestriker89/toy_data_generator.git
```

Once the prerequisite software is installed, go to the project folder and install the Python libraries using the command from the project folder:

```sh
pip install --user -r requirements.txt
```
Then, change the `forecastio_api_key` value in `config.yaml` under the `config` folder.

### Configuration

The configurations are found in `config` folder containing the settings used when generating data and logging.

#### A. config.yaml

This configuration file includes settings to generate baseline, simulated weather data and location list. Below are the top level configuration keys available:

##### 1. forecastio_api_key

This is the Dark Sky API to extract historical weather data.

##### 2. gis

This contains the list of parameters to generate baseline data sets.

Parameter                 | Default  | Description   
------------------------ |--------------| --------------
input_subdirectory | elevation | 
input_file_name | gebco_08_rev_elev_{grid_id}_grey_geo.tif | Elevation file name with `{grid_id}` as arbitrary variable
output_subdirectory | baseline | Output folder subdirectory
output_base_reference_file_name | baseline_gis_reference.csv | Baseline reference data file name
output_base_historical_file_name | baseline_gis_historical.csv | Baseline historical data file name
output_base_aggregate_file_name | baseline_gis_aggregate.csv | Baseline aggregate data file name
sampling_number | 2 | Number of historical baseline sample to be generated
year_start | 2010 | Minimum baseline historical year data to be generated
year_end | 2017 | Maximum baseline historical year data to be generated
latitude_condition | See the `config.yaml` | Condition in the getting the `{grid_id}` latitude file number
longitude_condition | See the `config.yaml` | Condition in the getting the `{grid_id}` longitude file letter

#### B. logging.yaml

This logging configuration file contains the loggin settings.

## Running test cases

To test the software, execute the following command from the project folder:
```sh
cd weather_generator
```

Then, execute the individual test cases using the command:
```sh
python -m unittest tests.data_test
python -m unittest tests.transform_test
```

## Execution

To run the software, execute the following command from the project folder:

```sh
cd weather_generator
python run.py --number_simulated_data=<number_simulated_data> --generate_baseline_flag=<generate_baseline_flag>
```

Arguments:

Parameter                 | Default       | Required   | Description   
------------------------ |--------------| --------------| --------------
\-\-number_simulated_data | N/A| Yes | Number of data points to be generated
\-\-generate_baseline_flag | False | No | Flag if new baseline data is generated

Sample successful execution output:

```sh
2019-04-25 12:30:00,404 - root - INFO - [run.py:49] Running weather data generator with number_simulated_data: 10 and generate_baseline_flag: False.
2019-04-25 12:30:00,405 - root - INFO - [weather_data_generator.py:26] Initialising WeatherDataGen class.
2019-04-25 12:30:00,412 - root - INFO - [weather_data_generator.py:52] Checking if the baseline data set exists.
2019-04-25 12:30:00,413 - root - INFO - [weather_data_generator.py:65] Baseline data sets exists.
2019-04-25 12:30:00,413 - root - INFO - [weather_data_generator.py:68] Reading baseline reference data.
2019-04-25 12:30:00,421 - root - INFO - [weather_data_generator.py:70] Completed reading baseline reference data.
2019-04-25 12:30:00,422 - root - INFO - [weather_data_generator.py:72] Reading baseline aggregate data.
2019-04-25 12:30:00,425 - root - INFO - [weather_data_generator.py:74] Completed reading baseline aggregate data.
2019-04-25 12:30:00,425 - root - INFO - [weather_data_generator.py:76] Initialising output_data data frame.
2019-04-25 12:30:00,430 - root - INFO - [weather_data_generator.py:87] Completed initialising WeatherDataGen class.
2019-04-25 12:30:00,430 - root - INFO - [weather_data_generator.py:231] Running weather data generation.
2019-04-25 12:30:00,430 - root - INFO - [weather_data_generator.py:93] Generating 10 random location(s).
2019-04-25 12:30:00,431 - root - INFO - [weather_data_generator.py:98] Completed generating 10 random location(s).
2019-04-25 12:30:00,432 - root - INFO - [weather_data_generator.py:104] Merging the output data with baseline reference data.
2019-04-25 12:30:00,437 - root - INFO - [weather_data_generator.py:111] Completed merging the output data with baseline reference data.
2019-04-25 12:30:00,437 - root - INFO - [weather_data_generator.py:130] Generating timestamp data for the output data between 1980-01-01 and 2018-12-31.
2019-04-25 12:30:00,441 - root - INFO - [weather_data_generator.py:140] Completed generating timestamp data for the output data.
2019-04-25 12:30:00,441 - root - INFO - [weather_data_generator.py:117] Merging the output data with baseline aggregate data.
2019-04-25 12:30:00,445 - root - INFO - [weather_data_generator.py:124] Completed merging the output data with baseline aggregate data.
2019-04-25 12:30:00,445 - root - INFO - [weather_data_generator.py:149] Initialising weather variable data.
2019-04-25 12:30:00,446 - root - INFO - [weather_data_generator.py:159] Completed initialising weather variable data.
2019-04-25 12:30:00,446 - root - INFO - [weather_data_generator.py:162] Generating weather condition data.
2019-04-25 12:30:00,447 - root - INFO - [weather_data_generator.py:167] Completed updating the output data with the generated weather condition data.
2019-04-25 12:30:00,448 - root - INFO - [weather_data_generator.py:170] Generating temperature data.
2019-04-25 12:30:00,466 - root - INFO - [weather_data_generator.py:176] Completed updating the output data with the generated temperature data.
2019-04-25 12:30:00,466 - root - INFO - [weather_data_generator.py:179] Generating pressure data.
2019-04-25 12:30:00,468 - root - INFO - [weather_data_generator.py:184] Completed updating the output data with the generated pressure data.
2019-04-25 12:30:00,469 - root - INFO - [weather_data_generator.py:187] Generating humidity data.
2019-04-25 12:30:00,470 - root - INFO - [weather_data_generator.py:192] Completed updating the output data with the generated humidity data.
2019-04-25 12:30:00,471 - root - INFO - [weather_data_generator.py:200] Finalising output_data layout.
2019-04-25 12:30:00,473 - root - INFO - [weather_data_generator.py:204] Completed finalising output_data layout.
2019-04-25 12:30:00,474 - root - INFO - [weather_data_generator.py:241] Completed running weather data generation.
2019-04-25 12:30:00,474 - root - INFO - [weather_data_generator.py:217] Saving output_data in C:\toy_data_generator\data\output\simulated_weather_output.csv.
2019-04-25 12:30:00,484 - root - INFO - [weather_data_generator.py:224] Completed saving output_data in C:\toy_data_generator\data\output\simulated_weather_output.csv.
2019-04-25 12:30:00,484 - root - INFO - [run.py:60] Completed running weather data generator in 00:00:00:0.08053994178771973.
```

### Todos

 - Write MORE Tests
 - Add Night Mode

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
