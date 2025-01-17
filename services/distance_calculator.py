import math
from typing import Tuple

from utils.config_loader import SIMPLE, HAVERSINE, SUCCESS, FAILURE, logging

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