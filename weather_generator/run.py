# Standard Python Library
import argparse
import logging.config
import time

# Custom Python Library
from common.config import LoggingConfig
from generator.weather_data_generator import WeatherDataGen

# Load logging.yaml file
logging.config.dictConfig(LoggingConfig.logging_config)

if __name__ == "__main__":
    """This is the main class that runs the rest of the
    weather data generator pipeline.
    """
    
    # Initialise the argument parser.
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--number_simulated_data"
       ,help = "The number weather data to be generated."
       ,type = int
       ,required = True 
    )
    
    parser.add_argument(
        "--generate_baseline_flag"
       ,help = "This flags whether to generate a baseline data sets. If the baseline data sets already exists, it will overwrite the data."
       ,type = str
       ,default = "False"
    )
    
    # Parse the input arguments.
    args = parser.parse_args()
    arguments = args.__dict__
    
    number_simulated_data=arguments.pop("number_simulated_data")
    
    if arguments.pop("generate_baseline_flag").lower() in ("yes", "true", "t", "y", "1"):
        generate_baseline_flag = True
    else:
        generate_baseline_flag = False
    
    # Start the data pipeline execution.
    start_time = time.time()
    
    logging.info("Running weather data generator with number_simulated_data: {} and generate_baseline_flag: {}.".format(number_simulated_data, generate_baseline_flag))
    
    wdg = WeatherDataGen(number_simulated_data=number_simulated_data
                        ,generate_baseline_flag=generate_baseline_flag)
    wdg.generate()
    
    # Save the output_data in a csv file.
    wdg.save_output()
    
    elapsed_time = time.time() - start_time
    
    logging.info("Completed running weather data generator in {}.".format(time.strftime("%H:%M:%S:{}".format(elapsed_time%1000), time.gmtime(elapsed_time))))
    
    




