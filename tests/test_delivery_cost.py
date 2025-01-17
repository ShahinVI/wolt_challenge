import unittest
from services.delivery_cost import process_total_cost, delivery_order_price
from utils.config_loader import SUCCESS, FAILURE

class TestDeliveryCost(unittest.TestCase):

    def test_process_total_cost_success(self):
        """Test process_total_cost with valid inputs."""
        cart_value = 1500
        distance = 1200
        order_minimum_no_surcharge = 1000
        base_price_delivery_fee = 500
        distance_ranges_dict = [
            {"min": 0, "max": 500, "a": 0, "b": 0},
            {"min": 500, "max": 1000, "a": 100, "b": 0},
            {"min": 1000, "max": 1500, "a": 200, "b": 0},
            {"min": 1500, "max": 2000, "a": 200, "b": 1},
            {"min": 2000, "max": 0, "a": 0, "b": 0},
        ]
        result, status, message = process_total_cost(
            cart_value, distance, order_minimum_no_surcharge, base_price_delivery_fee, distance_ranges_dict
        )
        self.assertEqual(status, SUCCESS)
        self.assertIn("total_price", result)
        self.assertGreater(result["total_price"], 0)

    def test_process_total_cost_out_of_range(self):
        """Test process_total_cost with distance out of range."""
        cart_value = 1500
        distance = 3000
        order_minimum_no_surcharge = 1000
        base_price_delivery_fee = 500
        distance_ranges_dict = [
            {"min": 0, "max": 500, "a": 0, "b": 0},
            {"min": 500, "max": 1000, "a": 100, "b": 0},
            {"min": 1000, "max": 1500, "a": 200, "b": 0},
            {"min": 1500, "max": 2000, "a": 200, "b": 1},
            {"min": 2000, "max": 0, "a": 0, "b": 0},
        ]
        result, status, message = process_total_cost(
            cart_value, distance, order_minimum_no_surcharge, base_price_delivery_fee, distance_ranges_dict
        )
        self.assertEqual(status, FAILURE)
        self.assertEqual(result, {})
        self.assertIn("Delivery is not possible", message)

    def test_delivery_order_price_success(self):
        """Test delivery_order_price with valid inputs."""
        venue_slug = "home-assignment-venue-berlin"
        cart_value = 1500
        user_lat = 52.5003197
        user_lon = 13.4536149
        result, status, message = delivery_order_price(venue_slug, cart_value, user_lat, user_lon)
        self.assertEqual(status, SUCCESS)
        self.assertIn("total_price", result)
        self.assertGreater(result["total_price"], 0)

    def test_delivery_order_price_failure(self):
        """Test delivery_order_price with invalid venue_slug."""
        venue_slug = "invalid-venue"
        cart_value = 1500
        user_lat = 52.5003197
        user_lon = 13.4536149
        result, status, message = delivery_order_price(venue_slug, cart_value, user_lat, user_lon)
        self.assertEqual(status, FAILURE)
        self.assertEqual(result, {})
        self.assertIn("Failed to process venue slug", message)


if __name__ == "__main__":
    unittest.main()
