from typing import Tuple, Dict, Any, List
from bisect import bisect_right

from utils.config_loader import O_1, O_Log_n, O_n, SUCCESS, FAILURE, logging, METHOD_RANGE_PARSING
from utils.validator import validate_inputs

from services.venue_processor import process_venue_slug, location_api_link_return, extract_delivery_specs, extract_static_coordinates
from services.distance_calculator import calculate_distance
from services.api_client import get_request

def process_total_cost(
    cart_value: int,
    distance: int,
    order_minimum_no_surcharge: int,
    base_price_delivery_fee: int,
    distance_ranges_dict: List[Dict[str, Any]],
    method: str = METHOD_RANGE_PARSING
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
        # Ensure distance_ranges_dict is in correct order
        distance_ranges_dict = sorted(
            distance_ranges_dict,
            key=lambda x: (x['max'] == 0, x['max'])
        )

        delivery_error=f"Delivery is not possible. Distance is out of delivery range. You should be within {distance_ranges_dict[-2]["max"]} meters"
        if method == O_n:
            """
            Determine delivery fee components based on distance ranges
            the following is an implementation which will be bad if dictionary is really big. 
            in reality I do not think this would be the case.
            however I am going to research a way to improve this.
            """
            for dist_range in distance_ranges_dict:
                if dist_range["max"] == 0:
                    message = delivery_error
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
                message = delivery_error
                logging.warning(message)
                return {}, FAILURE, message
            a = dist_range["a"]
            b = dist_range["b"]
        
        elif method == O_Log_n:
            # I found something called binary search
            max_values = [r['max'] for r in distance_ranges_dict]
            index = bisect_right(max_values, distance)
            if index == len(max_values):
                message = delivery_error
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