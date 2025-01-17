from typing import Tuple, List, Dict

from utils.config_loader import logging, SUCCESS, FAILURE, cities_acronym, countries_api 

def process_venue_slug(
    venue_slug: str
) -> Tuple[str, int, str]: 
    """
    Processes a venue slug to determine the corresponding country.

    Parameters:
        venue_slug (str): The unique identifier for the venue.

    Returns:
        Tuple:
            - venue_country (str or None): The country code if the venue_slug is valid, None otherwise.
            - status_code (int): SUCCESS (200) or FAILURE (400).
    """
    try:
        logging.info(f"Processing venue slug: {venue_slug}")
        venue_city = venue_slug.split("-")[-1]

        if venue_city.lower() not in cities_acronym.keys():
            message = f"Invalid venue city extracted from slug: {venue_city}"
            logging.warning(message)
            return "", FAILURE, message
        
        venue_country = cities_acronym[venue_city.lower()]
        message = f"Extracted country code '{venue_country}' for venue city '{venue_city}'."
        logging.info(message)
        return venue_country, SUCCESS, message
    
    except Exception as e:
        message = f"An error occurred while processing venue_slug '{venue_slug}': {e}"
        logging.error(message)
        return "", FAILURE, message
    
def location_api_link_return(
    venue_country: str
) -> Tuple[str, str, int, str]:
    """
    Returns the API links for the static and dynamic data of a given country.

    Parameters:
        venue_country (str): The country code for the venue.

    Returns:
        Tuple:
            - str: The static API link, or None if invalid.
            - str: The dynamic API link, or None if invalid.
            - int: SUCCESS (200) or FAILURE (400).
            - str: A descriptive message about the result.
    """
    try:
        if venue_country not in countries_api.keys():
            message = f"Invalid venue country code: {venue_country}"
            logging.warning(message)
            return "", "", FAILURE, message
        
        #retrieveing API Links
        dict_country_api = countries_api[venue_country]
        static_link = dict_country_api["static"]
        dynamic_link = dict_country_api["dynamic"]

        message = f"Retrieved API links for country code '{venue_country}'."
        logging.info(message)
        return static_link, dynamic_link, SUCCESS, message

    except Exception as e:
        message = f"An error occurred while retrieving API links for country '{venue_country}': {e}"
        logging.error(message)
        return "", "", FAILURE, message

def extract_static_coordinates(
    static_data: dict
) -> Tuple[float, float, int, str]:
    """
    Extracts the longitude and latitude from the static data.

    Parameters:
        static_data (dict): The static data containing the venue information.

    Returns:
        Tuple:
            - float: The longitude of the venue.
            - float: The latitude of the venue.
            - int: SUCCESS (200) or FAILURE (400).
            - str: A descriptive message about the result.
    """
    try:

        coordinates = static_data["venue_raw"]["location"]["coordinates"]
        coordinates_lon = coordinates[0]
        coordinates_lat = coordinates[1]

        message = "Successfully extracted coordinates from static data."
        logging.info(message)
        return coordinates_lon, coordinates_lat, SUCCESS, message

    except KeyError as e:
        message = f"Key error while accessing static data: {e}"
        logging.warning(message)
        return 0.0, 0.0, FAILURE, message

    except TypeError as e:
        message = f"Type error while processing static data: {e}"
        logging.warning(message)
        return 0.0, 0.0, FAILURE, message

    except Exception as e:
        message = f"An unexpected error occurred: {e}"
        logging.error(message)
        return 0.0, 0.0, FAILURE, message

    
def extract_delivery_specs(
    dynamic_data: dict
) -> Tuple[int, int, List[Dict[str, float]], int, str]:
    """
    Extracts the delivery specifications from the dynamic data.

    Parameters:
        dynamic_data (dict): The dynamic data containing delivery specifications.

    Returns:
        Tuple:
            - int: The minimum order value to avoid the small order surcharge.
            - int: The base price for delivery fee.
            - List[Dict[str, float]]: A list of dictionaries representing distance ranges for delivery pricing.
            - int: SUCCESS (200) or FAILURE (400).
            - str: A descriptive message about the result.
    """
    try:
        # Extract relevant fields from the dynamic data
        order_minimum_no_surcharge = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
        base_price_delivery_fee = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
        distance_ranges_dict = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]

        message = "Successfully extracted delivery specifications from dynamic data."
        logging.info(message)
        return order_minimum_no_surcharge, base_price_delivery_fee, distance_ranges_dict, SUCCESS, message

    except KeyError as e:
        message = f"Key error while accessing delivery specifications: {e}"
        logging.warning(message)
        return 0, 0, [], FAILURE, message

    except TypeError as e:
        message = f"Type error while processing delivery specifications: {e}"
        logging.warning(message)
        return 0, 0, [], FAILURE, message

    except Exception as e:
        message = f"An unexpected error occurred: {e}"
        logging.error(message)
        return 0, 0, [], FAILURE, message