# Toy Data Generator

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

### Installation

Once the prerequisite software is installed, go to the project folder and install the Python libraries.

```python
pip install --user -r requirements.txt
```

### Configuration

The configurations are found in `conf` folder and this contains the settings required


