# Standard Python Library
import yaml

# Custom Python Library
from common.utils import get_config

class LoggingConfig:
    
    """This class reads the logging YAML configuration file.
    """
    
    # Retrieve the loggin.yaml data.
    logging_config = get_config(file_name="logging.yaml")

