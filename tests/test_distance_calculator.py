import unittest
from services.distance_calculator import calculate_distance
from utils.config_loader import SIMPLE, HAVERSINE, SUCCESS, FAILURE


class TestDistanceCalculator(unittest.TestCase):

    def test_simple_calculation(self):
        """Test calculate_distance using SIMPLE method."""
        user_lat = 52.5200
        user_lon = 13.4050
        venue_lat = 52.5000
        venue_lon = 13.4000
        distance, status, message = calculate_distance(user_lat, user_lon, venue_lat, venue_lon, method=SIMPLE)
        self.assertEqual(status, SUCCESS)
        self.assertGreater(distance, 0)
        self.assertIn("simple Pythagorean theorem", message)

    def test_haversine_calculation(self):
        """Test calculate_distance using HAVERSINE method."""
        user_lat = 52.5200
        user_lon = 13.4050
        venue_lat = 52.5000
        venue_lon = 13.4000
        distance, status, message = calculate_distance(user_lat, user_lon, venue_lat, venue_lon, method=HAVERSINE)
        self.assertEqual(status, SUCCESS)
        self.assertGreater(distance, 0)
        self.assertIn("Haversine formula", message)

    def test_invalid_method(self):
        """Test calculate_distance with an invalid method."""
        user_lat = 52.5200
        user_lon = 13.4050
        venue_lat = 52.5000
        venue_lon = 13.4000
        distance, status, message = calculate_distance(user_lat, user_lon, venue_lat, venue_lon, method=999)
        self.assertEqual(status, FAILURE)
        self.assertEqual(distance, 0)
        self.assertIn("Invalid calculation method", message)

    def test_exception_handling(self):
        """Test calculate_distance with invalid input to trigger an exception."""
        user_lat = "invalid_lat"
        user_lon = 13.4050
        venue_lat = 52.5000
        venue_lon = 13.4000
        distance, status, message = calculate_distance(user_lat, user_lon, venue_lat, venue_lon, method=SIMPLE)
        self.assertEqual(status, FAILURE)
        self.assertEqual(distance, 0)
        self.assertIn("An error occurred", message)


if __name__ == "__main__":
    unittest.main()
