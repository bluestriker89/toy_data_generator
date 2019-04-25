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

Once the prerequisite software is installed, go to the project folder and install the Python libraries using the command:

```sh
pip install --user -r requirements.txt
```
Then, change the `forecastio_api_key` value in `config.yaml` under the `config` folder.

### Configuration

The configurations are found in `config` folder containing the settings used when generating data and logging.

#### config.yaml

This configuration file includes settings to generate baseline, simulated weather data and location list.

#### logging.yaml

This logging configuration file contains the loggin settings.

## Running tests

Dillinger uses a number of open source projects to work properly:

## Execution

To run the software, use the following command:

```sh
cd weather_generator
python run.py --number_simulated_data=<number_simulated_data> --generate_baseline_flag=<generate_baseline_flag>
```
Arguments:





### Todos

 - Write MORE Tests
 - Add Night Mode

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
