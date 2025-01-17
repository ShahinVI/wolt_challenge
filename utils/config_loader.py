import yaml
import logging

def load_config(config_path: str = "config/config.yaml") -> dict:
    """Loads configuration from the YAML file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

# Initialize configuration
config = load_config()

# Extract configurations
LOGGING_CONFIG = config["logging"]
CONSTANTS = config["constants"]

countries_api = config["countries_api"]
cities_acronym = config["cities_acronym"]

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[logging.StreamHandler()]
)

# Constants
SUCCESS = CONSTANTS["SUCCESS"]
FAILURE = CONSTANTS["FAILURE"]
SIMPLE = CONSTANTS["SIMPLE"]
HAVERSINE = CONSTANTS["HAVERSINE"]
O_1 = CONSTANTS["O_1"]
O_n = CONSTANTS["O_n"]
O_Log_n = CONSTANTS["O_Log_n"]