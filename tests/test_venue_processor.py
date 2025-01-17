import unittest
from services.venue_processor import (
    process_venue_slug,
    location_api_link_return,
    extract_static_coordinates,
    extract_delivery_specs,
)
from utils.config_loader import SUCCESS, FAILURE


class TestVenueProcessor(unittest.TestCase):

    def test_process_venue_slug_valid(self):
        """Test process_venue_slug with a valid venue_slug."""
        venue_slug = "home-assignment-venue-berlin"
        venue_country, status, message = process_venue_slug(venue_slug)
        self.assertEqual(status, SUCCESS)
        self.assertEqual(venue_country, "DE")
        self.assertIn("Extracted country code", message)

    def test_process_venue_slug_invalid(self):
        """Test process_venue_slug with an invalid venue_slug."""
        venue_slug = "home-assignment-venue-unknown"
        venue_country, status, message = process_venue_slug(venue_slug)
        self.assertEqual(status, FAILURE)
        self.assertEqual(venue_country, "")
        self.assertIn("Invalid venue city", message)

    def test_location_api_link_return_valid(self):
        """Test location_api_link_return with a valid venue_country."""
        venue_country = "DE"
        static_link, dynamic_link, status, message = location_api_link_return(venue_country)
        self.assertEqual(status, SUCCESS)
        self.assertIn("berlin", static_link)
        self.assertIn("berlin", dynamic_link)
        self.assertIn("Retrieved API links", message)

    def test_location_api_link_return_invalid(self):
        """Test location_api_link_return with an invalid venue_country."""
        venue_country = "XX"
        static_link, dynamic_link, status, message = location_api_link_return(venue_country)
        self.assertEqual(status, FAILURE)
        self.assertEqual(static_link, "")
        self.assertEqual(dynamic_link, "")
        self.assertIn("Invalid venue country code", message)

    def test_extract_static_coordinates_valid(self):
        """Test extract_static_coordinates with valid static data."""
        static_data = {
            "venue_raw": {
                "location": {"coordinates": [13.4536149, 52.5003197]}
            }
        }
        lon, lat, status, message = extract_static_coordinates(static_data)
        self.assertEqual(status, SUCCESS)
        self.assertEqual(lon, 13.4536149)
        self.assertEqual(lat, 52.5003197)
        self.assertIn("Successfully extracted coordinates", message)

    def test_extract_static_coordinates_invalid(self):
        """Test extract_static_coordinates with missing keys."""
        static_data = {"venue_raw": {"location": {}}}
        lon, lat, status, message = extract_static_coordinates(static_data)
        self.assertEqual(status, FAILURE)
        self.assertEqual(lon, 0.0)
        self.assertEqual(lat, 0.0)
        self.assertIn("Key error", message)

    def test_extract_delivery_specs_valid(self):
        """Test extract_delivery_specs with valid dynamic data."""
        dynamic_data = {
            "venue_raw": {
                "delivery_specs": {
                    "order_minimum_no_surcharge": 1000,
                    "delivery_pricing": {
                        "base_price": 190,
                        "distance_ranges": [
                            {"min": 0, "max": 500, "a": 0, "b": 0},
                            {"min": 500, "max": 1000, "a": 100, "b": 0},
                            {"min": 1000, "max": 1500, "a": 200, "b": 0},
                            {"min": 1500, "max": 2000, "a": 200, "b": 1},
                            {"min": 2000, "max": 0, "a": 0, "b": 0},
                        ],
                    },
                }
            }
        }
        order_min, base_price, distance_ranges, status, message = extract_delivery_specs(dynamic_data)
        self.assertEqual(status, SUCCESS)
        self.assertEqual(order_min, 1000)
        self.assertEqual(base_price, 190)
        self.assertEqual(len(distance_ranges), 5)
        self.assertIn("Successfully extracted delivery specifications", message)

    def test_extract_delivery_specs_invalid(self):
        """Test extract_delivery_specs with missing keys."""
        dynamic_data = {"venue_raw": {}}
        order_min, base_price, distance_ranges, status, message = extract_delivery_specs(dynamic_data)
        self.assertEqual(status, FAILURE)
        self.assertEqual(order_min, 0)
        self.assertEqual(base_price, 0)
        self.assertEqual(distance_ranges, [])
        self.assertIn("Key error", message)


if __name__ == "__main__":
    unittest.main()
