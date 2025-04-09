"""
Tests for iiko_pkg.constants
"""

import unittest

from iiko_pkg.constants import API_BASE_URL, ENDPOINTS, OrderStatus, DeliveryStatus, PaymentType


class TestConstants(unittest.TestCase):
    """Test constants"""

    def test_api_base_url(self):
        """Test API_BASE_URL constant"""
        self.assertEqual(API_BASE_URL, "https://api-ru.iiko.services")

    def test_endpoints(self):
        """Test ENDPOINTS constant"""
        self.assertIsInstance(ENDPOINTS, dict)
        self.assertIn("token", ENDPOINTS)
        self.assertIn("organizations", ENDPOINTS)
        self.assertIn("terminal_groups", ENDPOINTS)
        self.assertIn("nomenclature", ENDPOINTS)
        self.assertIn("menu", ENDPOINTS)
        self.assertIn("menu_by_id", ENDPOINTS)
        self.assertIn("stop_lists", ENDPOINTS)
        self.assertIn("order_create", ENDPOINTS)
        self.assertIn("order_by_id", ENDPOINTS)
        self.assertIn("delivery_create", ENDPOINTS)
        self.assertIn("delivery_by_id", ENDPOINTS)
        self.assertIn("payment_types", ENDPOINTS)
        self.assertIn("order_types", ENDPOINTS)
        self.assertIn("discounts", ENDPOINTS)
        self.assertIn("cancel_causes", ENDPOINTS)
        self.assertIn("regions", ENDPOINTS)
        self.assertIn("cities", ENDPOINTS)
        self.assertIn("streets_by_city", ENDPOINTS)
        self.assertIn("couriers", ENDPOINTS)
        self.assertIn("couriers_active_location", ENDPOINTS)
        self.assertIn("marketing_sources", ENDPOINTS)
        self.assertIn("customer_info", ENDPOINTS)
        self.assertIn("customer_create_or_update", ENDPOINTS)

    def test_order_status(self):
        """Test OrderStatus class"""
        self.assertEqual(OrderStatus.NEW, "New")
        self.assertEqual(OrderStatus.BILL, "Bill")
        self.assertEqual(OrderStatus.CLOSED, "Closed")
        self.assertEqual(OrderStatus.CANCELLED, "Cancelled")

    def test_delivery_status(self):
        """Test DeliveryStatus class"""
        self.assertEqual(DeliveryStatus.NEW, "New")
        self.assertEqual(DeliveryStatus.WAITING, "Waiting")
        self.assertEqual(DeliveryStatus.ON_WAY, "OnWay")
        self.assertEqual(DeliveryStatus.DELIVERED, "Delivered")
        self.assertEqual(DeliveryStatus.CLOSED, "Closed")
        self.assertEqual(DeliveryStatus.CANCELLED, "Cancelled")

    def test_payment_type(self):
        """Test PaymentType class"""
        self.assertEqual(PaymentType.CASH, "Cash")
        self.assertEqual(PaymentType.CARD, "Card")
        self.assertEqual(PaymentType.CREDIT, "Credit")
        self.assertEqual(PaymentType.GIFT_CARD, "GiftCard")
        self.assertEqual(PaymentType.EXTERNAL, "External")


if __name__ == "__main__":
    unittest.main()
