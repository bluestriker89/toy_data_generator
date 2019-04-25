# Standard Python Library
import os
import yaml

def get_file_path(file_name, folder_name="data", subdirectory=""):
    """Generate the absolute file path of a file including 1 level of subdirectory.

    Parameters
    ----------
    file_name : string
        The file name including extension name.
    folder_name : string, default is 'data'
        The folder name within the project structure.
    subdirectory : string, default is ''
        The subdirectory folder name within the folder name specified.

    Returns
    -------
    file_path : string
    """
    
    # Get the absolute path of the current working directory.
    project_path = os.path.abspath(os.path.join(os.curdir, os.pardir))
    
    # Get the full file path based on the input parameters.
    file_path = os.path.join(project_path, folder_name, subdirectory,file_name)

    return file_path
    
def get_config(file_name="config.yaml", format="yaml"):
    """Returns the configuration file data.

    Parameters
    ----------
    file_name : string, default t 'config.yaml'
        The configuration file name.
    format : string, default t 'config.yaml'
        The configuration file format.

    Returns
    -------
    config_data : yaml or other format
    """
    
    # Get the configuration file path.
    config_file_path = get_file_path(folder_name="config", file_name=file_name)
    
    if format=="yaml":
        with open(config_file_path) as config:
            # Load the YAML file.
            config_data = yaml.safe_load(config)

    return config_data
 
def get_city(loc):
    """Return the city name of the location data.

    Parameters
    ----------
    loc : string
        The location name including country e.g. 'Sydney, Australia'.

    Returns
    -------
    city : string
    """
    
    # Retrieving city data.    
    return loc[:loc.find(',')]
