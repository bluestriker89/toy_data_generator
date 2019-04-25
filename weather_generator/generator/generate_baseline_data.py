# Standard Python Library
import calendar
import datetime
import forecastio
import logging.config
import pandas as pd
import random
import rasterio as rio
from faker import Faker
from geopy.geocoders import Nominatim

# Custom Python Library
from common.config import LoggingConfig
from common.utils import get_file_path, get_config, get_city

# Load logging.yaml file
logging.config.dictConfig(LoggingConfig.logging_config)

def get_elevation_data(lat, lon):
    """This function returns the elevation based on tif files located
    in the ./data/elevation/*.tif folder using rasterio library.

    Parameters
    ----------
    lat : float
        The latitude of the location.
    lon : float
        The longitude of the location.

    Returns
    -------
    elev : int
         This is the elevation based on supplied coordinates.
    """
    
    logging.info("Getting elevation data for the coordinate ({}, {}).".format(lat, lon))
    
    # Initialising function variables
    grid_lat = None
    grid_lon = None
    coord = (lon, lat)
    config_data = get_config()["gis"]
    elev_file_name = config_data["input_file_name"]
    
    logging.info("Determining the appropriate tif file for the coordinate ({}, {}).".format(lat, lon))
    
    # Determine location's latitude data from the image
    # grid. Valid values are 1 and 2.
    for key, value in config_data["latitude_condition"].items():
        
        if value["min_lat"] <= lat <= value["max_lat"]:
             grid_lat = value["grid_lat"]

    # Determine location's longitude data from the image
    # grid. Valid values are A, B, C and D.
    for key, value in config_data["longitude_condition"].items():
        
        if value["min_lon"] <= lon <= value["max_lon"]:
             grid_lon = value["grid_lon"]

    # Determine that there is a valid grid_lat and grid_lon data.
    if grid_lat is None or grid_lon is None:
        logging.error("Invalid coordinate ({}, {}). Please check the value!".format(lat, lon))
        raise ValueError

    grid_id = "".join([grid_lon, grid_lat])
    file_name = elev_file_name.format(grid_id=grid_id)

    # Retrieve the elevation tif file path based on grid_id.
    elev_file_path = get_file_path(folder_name="data"
                                  ,subdirectory=config_data["input_subdirectory"]
                                  ,file_name=file_name)
                                  
    logging.info("Retrieving elevation data for the coordinate ({}, {}) is in {} file.".format(lat, lon, file_name))

    # Retrieve the elevation data found in elev_file_path.
    with rio.open(elev_file_path) as file:
        elevs = file.sample((coord, coord))
        elev = next(elevs)[0]

    logging.info("Completed retrieving elevation data for the coordinate ({}, {}). Elevation value: {}.".format(lat, lon, elev))
    
    return elev

def get_gis_historical_data():
    """This function retrieves the baseline historical weather data
    supplied in 'location key' of config.yaml. It uses Dark Sky API to
    retrieve historical weather data such as temperature, humidity and
    pressure.
    """
    logging.info("Generating baseline reference and historical weather data.")
    
    # Initialising function variables
    fake = Faker()
    geolocator = Nominatim()
    config_data = get_config()
    locations = config_data["location"]
    
    # Check if there are no duplicate locations in the config.yaml file.
    if len(locations) != len(set(locations)):
        logging.error("Duplicate location found. Please check config.yaml file.")
        raise ValueError
    
    # Initialise pandas dataframe column name for baseline reference
    # and historical data.
    df_ref = pd.DataFrame(columns=["Location", "Latitude"
                              ,"Longitude", "Elevation"
                              ,"Timezone"])
    df_hist = pd.DataFrame(columns=["Location", "Date"
                              ,"Month", "Temperature_Min"
                              ,"Temperature_Max", "Humidity"
                              ,"Pressure"])
    
    # Generate weather data for each location.
    for idx, loc in enumerate(locations):
        
        logging.info("Retrieving geolocation data for {}.".format(loc))
        
        # Retrieving geolocation data from geopy library.
        loc_data = geolocator.geocode(loc)
        
        logging.info("Check if the location {} is valid.".format(loc))
        if loc_data is None:
            logging.error("Invalid location value supplied ({}). Please check config.yaml file.".format(loc))
            raise ValueError
        logging.info("The location {} is valid.".format(loc))
        
        city = get_city(loc)
        lat = loc_data.latitude
        lon = loc_data.longitude
        
        # Retrieving elevation data for the location.
        elev = get_elevation_data(lat, lon)
        
        for month in range(1, 13):
            
            logging.info("Retrieving {} weather data for month {}.".format(loc, month))
            
            for sample in range(config_data["gis"]["sampling_number"]):
                
                temp_min = None
                temp_max = None
                humidity = None
                pressure = None
                
                while temp_min is None or temp_max is None or humidity is None or pressure is None:
                    
                    year = random.randint(config_data["gis"]["year_start"], config_data["gis"]["year_end"])

                    _, last_day = calendar.monthrange(year, month)

                    datetime_start = datetime.datetime(year, month, 1)
                    datetime_end = datetime.datetime(year, month, last_day)

                    date_gen = fake.date_time_between_dates(datetime_start=datetime_start
                                                           ,datetime_end=datetime_end)

                    forecast = forecastio.load_forecast(config_data["forecastio_api_key"]
                                                       ,lat
                                                       ,lon
                                                       ,time=date_gen
                                                       ,units="si")

                    historical_data = forecast.json["daily"]["data"][0]
                    
                    timezone = forecast.json.get("timezone", None)
                    temp_min =  historical_data.get("temperatureMin", None)
                    temp_max =  historical_data.get("temperatureMax", None)
                    humidity =  historical_data.get("humidity", None) * 100
                    pressure =  historical_data.get("pressure", None)
                    
                df_temp_hist = pd.Series(dict(zip(df_hist.columns
                                                 ,[city, date_gen
                                                 ,date_gen.month, temp_min
                                                 ,temp_max, humidity
                                                 ,pressure])))
                
                df_hist = df_hist.append(df_temp_hist, ignore_index=True)
        
        df_temp_ref = pd.Series(dict(zip(df_ref.columns
                                        ,[city, lat
                                        ,lon, elev
                                        ,timezone])))
        df_ref = df_ref.append(df_temp_ref, ignore_index=True)
    
    logging.info("Generating position to consolidate latitude, longitude and elevation data")
    df_pos = df_ref[["Latitude", "Longitude", "Elevation"]].round(2)
    df_pos["Elevation"] = df_pos["Elevation"].astype(int) 
    df_ref["Position"] = df_pos.astype(str).apply(lambda x: ",".join(x), axis=1)
    
    logging.info("Saving baseline reference data.")
    df_ref.to_csv(get_file_path(folder_name="data"
                                ,subdirectory=config_data["gis"]["output_subdirectory"]
                                ,file_name=config_data["gis"]["output_base_reference_file_name"])
                 ,index=False)
    logging.info("Completed saving baseline reference data.")

    logging.info("Saving baseline historical data.")
    df_hist.to_csv(get_file_path(folder_name="data"
                                ,subdirectory=config_data["gis"]["output_subdirectory"]
                                ,file_name=config_data["gis"]["output_base_historical_file_name"])
                  ,index=False)
    logging.info("Completed saving baseline historical data.")

def aggregate_gis_historical_data():
    """This function aggregates baseline historical data by location and month
    for the weather parameters:
    - Temperature: Mean for minimum and maximum temperature
    - Humidity: Minimum and maximum humidity
    - Pressure: Minimum and maximum pressure
    """
    
    logging.info("Processing historical weather data aggregation.")
    
    # Initialising function variables
    config_data = get_config()
    
    # Initialise pandas dataframe column name for baseline reference
    # and historical data.
    hist_file_path = get_file_path(folder_name="data"
                                  ,subdirectory=config_data["gis"]["output_subdirectory"]
                                  ,file_name=config_data["gis"]["output_base_historical_file_name"])

    # Define group by columns.
    group_by_cols = ["Location", "Month"]

    # Define aggregate columns.
    aggregate_cols = {"Temperature_Min": "mean"
                     ,"Temperature_Max": "mean"
                     ,"Humidity": ["min", "max"]
                     ,"Pressure": ["min", "max"]}

    logging.info("Reading historical weather data.")
    
    # Read baseline historical data.
    df = pd.read_csv(hist_file_path)
    
    logging.info("Completed reading historical weather data.")
    
    logging.info("Aggregating historical weather data.")
    df_aggregate = df.groupby(group_by_cols, as_index=False).aggregate(aggregate_cols)
    df_aggregate.columns = ["".join(name) for name in df_aggregate.columns.ravel()]
    df_aggregate.rename(columns={"Temperature_Minmean": "T_avg_min"
                                ,"Temperature_Maxmean": "T_avg_max"
                                ,"Humiditymin": "H_min"
                                ,"Humiditymax": "H_max"
                                ,"Pressuremin": "P_min"
                                ,"Pressuremax": "P_max"}
                       ,inplace=True)
    df_aggregate ["T_avg_range"] = df_aggregate ["T_avg_max"] - df_aggregate ["T_avg_min"]
    df_aggregate ["H_range"] = df_aggregate ["H_max"] - df_aggregate ["H_min"]
    df_aggregate ["P_range"] = df_aggregate ["P_max"] - df_aggregate ["P_min"]

    logging.info("Saving baseline aggregate data.")
    df_aggregate.to_csv(get_file_path(folder_name="data"
                                 ,subdirectory=config_data["gis"]["output_subdirectory"]
                                 ,file_name=config_data["gis"]["output_base_aggregate_file_name"])
                       ,index=False)
    logging.info("Completed saving baseline aggregate data.")







