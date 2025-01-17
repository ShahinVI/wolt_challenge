from utils.config_loader import SUCCESS, FAILURE
from typing import Tuple


def validate_venue_slug(venue_slug: str) -> Tuple[bool, str]:
    """Validates the venue slug."""
    if not venue_slug or not isinstance(venue_slug, str):
        return False, "Invalid venue_slug: It must be a non-empty string."
    return True, ""


def validate_cart_value(cart_value: int) -> Tuple[bool, str]:
    """Validates the cart value."""
    if not isinstance(cart_value, int) or cart_value < 0:
        return False, "Invalid cart value: It must be a non-negative integer."
    return True, ""


def validate_coordinates(user_lat: float, user_lon: float) -> Tuple[bool, str]:
    """Validates user latitude and longitude."""
    if not (-90 <= user_lat <= 90):
        return False, f"Invalid latitude: {user_lat}. It must be between -90 and 90."
    if not (-180 <= user_lon <= 180):
        return False, f"Invalid longitude: {user_lon}. It must be between -180 and 180."
    return True, ""


def validate_inputs(venue_slug: str, cart_value: int, user_lat: float, user_lon: float) -> Tuple[int, str]:
    """
    Validates all inputs.
    Combines individual validation functions for convenience.
    """
    is_valid, error_message = validate_venue_slug(venue_slug)
    if not is_valid:
        return FAILURE, error_message

    is_valid, error_message = validate_cart_value(cart_value)
    if not is_valid:
        return FAILURE, error_message

    is_valid, error_message = validate_coordinates(user_lat, user_lon)
    if not is_valid:
        return FAILURE, error_message

    return SUCCESS, ""
