import requests
import math
import logging
from typing import Tuple, Dict, Any, List
from bisect import bisect_right
import yaml

# Load config.yaml
def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

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



def get_request(
    url: str
) -> Tuple[Dict[Any, Any], int, str]:
    """
    Sends a GET request to the specified URL

    Parameters:
        url (str): The URL to send for the GET request
    
    Returns:
        tuple: (data, status_code, message)
            - data (dict or None): Parsed JSON response if successful, None otherwise.
            - status_code (int): SUCCESS (200) or FAILURE (400).
            - message (str): A descriptive success or error message
    """
    try:
        logging.info(f"Sending GET request to URL: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            logging.info(f"Request to {url} succeeded with status code: {response.status_code}")
            return response.json(), SUCCESS, "Request successful"
        else:
            logging.warning(f"Request to {url} failed with status code: {response.status_code}")
            return {}, FAILURE, f"Request failed with status code: {response.status_code}"

    except requests.exceptions.Timeout:
        logging.error(f"Request to {url} timed out.")
        return {}, FAILURE, "Request timed out"

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while requesting {url}: {e}")
        return {}, FAILURE, f"Request error: {e}"

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

def calculate_distance(
    user_lat: float, 
    user_lon: float, 
    venue_lat: float, 
    venue_lon: float, 
    method: int = SIMPLE
) -> Tuple[int, int, str]:
    """
    Calculates the distance between two geographic points using the specified method.

    Parameters:
        user_lat (float): Latitude of the user.
        user_lon (float): Longitude of the user.
        venue_lat (float): Latitude of the venue.
        venue_lon (float): Longitude of the venue.
        method (int): Method to calculate distance:
                      - 0 (SIMPLE): Uses the Pythagorean theorem for simplicity.
                      - 1 (HAVERSINE): Uses the Haversine formula for more accuracy.

    Returns:
        Tuple:
            - int: The calculated distance in meters.
            - int: SUCCESS (200) or FAILURE (400).
            - str: A descriptive message about the result.
    """
    try:
        if method == HAVERSINE:
            # Haversine calculation for earth curvature
            user_lat, user_lon, venue_lat, venue_lon = map(math.radians, [user_lat, user_lon, venue_lat, venue_lon])
            delta_lat = venue_lat - user_lat
            delta_lon = venue_lon - user_lon
            a = math.sin(delta_lat / 2) ** 2 + math.cos(user_lat) * math.cos(venue_lat) * math.sin(delta_lon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            R = 6371 * 1000  # Radius of Earth in meters
            distance_m = R * c  # Distance in meters

            message = "Distance calculated using Haversine formula."
            logging.info(message)
            return round(distance_m), SUCCESS, message

        elif method == SIMPLE:
            # Pythagorean theorem for simplicity
            km_per_degree_lat = 111.32
            km_per_degree_lon = 111.32

            delta_lat = venue_lat - user_lat
            delta_lon = venue_lon - user_lon

            y_distance = delta_lat * km_per_degree_lat
            x_distance = delta_lon * km_per_degree_lon * math.cos(math.radians(user_lat))

            distance_km = math.sqrt(x_distance ** 2 + y_distance ** 2)
            distance_m = distance_km * 1000

            message = "Distance calculated using the simple Pythagorean theorem."
            logging.info(message)
            return round(distance_m), SUCCESS, message

        else:
            message = f"Invalid calculation method: {method}. Use 0 (SIMPLE) or 1 (HAVERSINE)."
            logging.error(message)
            return 0, FAILURE, message

    except Exception as e:
        message = f"An error occurred during distance calculation: {e}"
        logging.error(message)
        return 0, FAILURE, message


def process_total_cost(
    cart_value: int,
    distance: int,
    order_minimum_no_surcharge: int,
    base_price_delivery_fee: int,
    distance_ranges_dict: List[Dict[str, Any]],
    method: str = O_Log_n
) -> Tuple[Dict[str, Any], int, str]:
    """
    Processes the total cost of the order, including the delivery fee, small order surcharge, and total price.

    Parameters:
        cart_value (int): Total value of the items in the cart.
        distance (int): Distance between the user and the venue in meters.
        order_minimum_no_surcharge (int): Minimum cart value to avoid the small order surcharge.
        base_price_delivery_fee (int): Base price for the delivery fee.
        distance_ranges_dict (List[Dict[str, Any]]): Distance ranges for calculating delivery fee.

    Returns:
        Tuple:
            - Dict[str, Any]: The response containing total price, delivery fee breakdown, and other details.
            - int: SUCCESS (200) or FAILURE (400).
            - str: A descriptive message about the result.
    """
    try:
        # Initialing variables for delivery fee calculation
        a = 0
        b = 0
        
        if method == O_n:
            """
            Determine delivery fee components based on distance ranges
            the following is an implementation which will be bad if dictionary is really big. 
            in reality I do not think this would be the case.
            however I am going to research a way to improve this.
            """
            for dist_range in distance_ranges_dict:
                if dist_range["max"] == 0:
                    message = "Delivery is not possible for distances exceeding the defined maximum."
                    logging.warning(message)
                    return {}, FAILURE, message
                temp_distance = distance - dist_range["max"]
                if temp_distance <= 0:
                    a = dist_range["a"]
                    b = dist_range["b"]
                    break
        
        elif method == O_1:
            """
             found it
             we can preprocess it and save it all in a look up table
             if the data is static we can just record all possible distances 
             and save them in a dictonary.
             loop through ranges and save for each meter the a and b of it.
             so each morning we precalculate the distances and ranges of everything.
             but the space complexity will be very high here
            """
            max_distance = max(r['max'] for r in distance_ranges_dict)
            lookup_table = [None] * (max_distance + 1)
            for r in distance_ranges_dict:
                for d in range(r['min'], r['max'] + 1):
                    lookup_table[d] = {'a': r['a'], 'b': r['b']}
            dist_range = lookup_table[distance] if distance <= max_distance else None
            if dist_range is None:
                message = "Delivery is not possible for distances exceeding the defined maximum."
                logging.warning(message)
                return {}, FAILURE, message
            a = dist_range["a"]
            b = dist_range["b"]
        
        elif method == O_Log_n:
            # I found something called binary search
            max_values = [r['max'] for r in distance_ranges_dict]
            index = bisect_right(max_values, distance)
            if index == len(max_values):
                message = "Delivery is not possible for distances exceeding the defined maximum."
                logging.warning(message)
                return {}, FAILURE, message
            else:
                dist_range = distance_ranges_dict[index - 1]
                a = dist_range["a"]
                b = dist_range["b"]

        # Calculate total price and fee breakdown
        small_order_surcharge = max(0, order_minimum_no_surcharge - cart_value)
        delivery_fee = a + (b * distance) / 10 + base_price_delivery_fee
        total_price = cart_value + small_order_surcharge + delivery_fee

        # Construct the endpoint response
        endpoint_response = {
            "total_price": int(total_price),
            "small_order_surcharge": int(small_order_surcharge),
            "cart_value": int(cart_value),
            "delivery": {
                "fee": int(delivery_fee),
                "distance": int(distance),
            }
        }

        message = "Successfully calculated total cost."
        logging.info(message)
        return endpoint_response, SUCCESS, message

    except KeyError as e:
        message = f"Key error while processing distance ranges: {e}"
        logging.warning(message)
        return {}, FAILURE, message

    except TypeError as e:
        message = f"Type error while processing inputs: {e}"
        logging.warning(message)
        return {}, FAILURE, message

    except Exception as e:
        message = f"An unexpected error occurred: {e}"
        logging.error(message)
        return {}, FAILURE, message

def validate_inputs(venue_slug: str, cart_value: int, user_lat: float, user_lon: float) -> Tuple[bool, str]:
    if not venue_slug or not isinstance(venue_slug, str):
        return FAILURE, "Invalid venue_slug"
    if cart_value < 0:
        return FAILURE, "Cart value must be non-negative"
    if not (-90 <= user_lat <= 90) or not (-180 <= user_lon <= 180):
        return FAILURE, "Invalid latitude or longitude values"
    return SUCCESS, ""


def delivery_order_price(
    venue_slug: str, cart_value: int, user_lat: float, user_lon: float
) -> Tuple[Dict[str, Any], int, str]:
    """
    Calculates the delivery order price, including total cost and breakdown.

    Parameters:
        venue_slug (str): The unique identifier for the venue.
        cart_value (int): The total value of the items in the shopping cart.
        user_lat (float): The latitude of the user's location.
        user_lon (float): The longitude of the user's location.

    Returns:
        Tuple:
            - Dict[str, Any]: The response containing the price breakdown.
            - int: SUCCESS (200) or FAILURE (400).
            - str: A descriptive message.
    """
    try:
        # pre processing: validation
        success_code, error_message = validate_inputs(venue_slug, cart_value, user_lat, user_lon)
        if success_code == FAILURE:
            return {}, FAILURE, error_message

        # Step 1: Process venue slug to determine country
        venue_country, success_code, message = process_venue_slug(venue_slug)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to process venue slug: {message}"

        # Step 2: Get API links for the venue's country
        static_api_link, dynamic_api_link, success_code, message = location_api_link_return(venue_country)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to retrieve API links: {message}"

        # Step 3: Fetch static data
        static_data, success_code, message = get_request(static_api_link)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to fetch static data: {message}"

        # Step 4: Fetch dynamic data
        dynamic_data, success_code, message = get_request(dynamic_api_link)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to fetch dynamic data: {message}"

        # Step 5: Extract coordinates from static data
        venue_lon, venue_lat, success_code, message = extract_static_coordinates(static_data)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to extract venue coordinates: {message}"

        # Step 6: Extract delivery specs from dynamic data
        order_minimum_no_surcharge, base_price_delivery_fee, distance_ranges_dict, success_code, message = extract_delivery_specs(dynamic_data)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to extract delivery specifications: {message}"

        # Step 7: Calculate distance between user and venue
        distance, success_code, message = calculate_distance(user_lat, user_lon, venue_lat, venue_lon)
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to calculate distance: {message}"

        # Step 8: Calculate total cost
        endpoint_response, success_code, message = process_total_cost(
            cart_value, distance, order_minimum_no_surcharge, base_price_delivery_fee, distance_ranges_dict
        )
        if success_code == FAILURE:
            return {}, FAILURE, f"Failed to calculate total cost: {message}"

        # Success
        return endpoint_response, SUCCESS, "Successfully calculated delivery order price."

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return {}, FAILURE, f"An unexpected error occurred: {e}"

def main(): 
    entry_call="curl http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
    
    venue_slug="home-assignment-venue-helsinki"
    cart_value=1000
    user_lat=60.17094
    user_lon=24.93087
    
    endpoint_response, SUCCESS, message_code = delivery_order_price(venue_slug,cart_value,user_lat,user_lon)
    print(SUCCESS,endpoint_response, message_code)


if __name__ == "__main__":
    main()
