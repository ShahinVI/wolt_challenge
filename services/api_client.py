import requests
import logging
from typing import Tuple, Dict, Any
from utils.config_loader import SUCCESS,FAILURE

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
