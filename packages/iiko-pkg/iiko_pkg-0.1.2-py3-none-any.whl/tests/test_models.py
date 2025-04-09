"""
Tests for iiko_pkg.models
"""

import unittest
from datetime import datetime

from iiko_pkg.models.auth import TokenResponse
from iiko_pkg.models.organizations import Organization, OrganizationsResponse
from iiko_pkg.models.menu import Menu, MenuResponse, Product, ProductCategory
from iiko_pkg.models.orders import Order, OrderResponse, OrderItem
from iiko_pkg.models.delivery import Delivery, DeliveryResponse
from iiko_pkg.models.common import Address, Customer, Coordinates


class TestModels(unittest.TestCase):
    """Test models"""

    def test_token_response(self):
        """Test TokenResponse model"""
        token = TokenResponse(
            token="test_token",
            expire_seconds=3600,
            created_at=datetime.now()
        )
        
        self.assertEqual(token.token, "test_token")
        self.assertEqual(token.expire_seconds, 3600)
        self.assertIsNotNone(token.created_at)
        self.assertFalse(token.is_expired())

    def test_organization(self):
        """Test Organization model"""
        org = Organization(
            id="test_id",
            name="Test Organization",
            country="Test Country",
            restaurant_address="Test Address",
            latitude=1.0,
            longitude=2.0
        )
        
        self.assertEqual(org.id, "test_id")
        self.assertEqual(org.name, "Test Organization")
        self.assertEqual(org.country, "Test Country")
        self.assertEqual(org.restaurant_address, "Test Address")
        self.assertEqual(org.latitude, 1.0)
        self.assertEqual(org.longitude, 2.0)

    def test_organizations_response(self):
        """Test OrganizationsResponse model"""
        org1 = Organization(
            id="test_id_1",
            name="Test Organization 1",
            country="Test Country 1",
            restaurant_address="Test Address 1",
            latitude=1.0,
            longitude=2.0
        )
        
        org2 = Organization(
            id="test_id_2",
            name="Test Organization 2",
            country="Test Country 2",
            restaurant_address="Test Address 2",
            latitude=3.0,
            longitude=4.0
        )
        
        response = OrganizationsResponse(
            organizations=[org1, org2]
        )
        
        self.assertEqual(len(response.organizations), 2)
        self.assertEqual(response.organizations[0].id, "test_id_1")
        self.assertEqual(response.organizations[1].id, "test_id_2")

    def test_product(self):
        """Test Product model"""
        product = Product(
            id="test_id",
            name="Test Product",
            price=100.0,
            category_id="test_category_id",
            is_deleted=False,
            is_hidden=False,
            is_included_in_menu=True,
            order=1
        )
        
        self.assertEqual(product.id, "test_id")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.category_id, "test_category_id")
        self.assertFalse(product.is_deleted)
        self.assertFalse(product.is_hidden)
        self.assertTrue(product.is_included_in_menu)
        self.assertEqual(product.order, 1)

    def test_product_category(self):
        """Test ProductCategory model"""
        category = ProductCategory(
            id="test_id",
            name="Test Category",
            is_deleted=False,
            is_hidden=False,
            is_included_in_menu=True,
            order=1
        )
        
        self.assertEqual(category.id, "test_id")
        self.assertEqual(category.name, "Test Category")
        self.assertFalse(category.is_deleted)
        self.assertFalse(category.is_hidden)
        self.assertTrue(category.is_included_in_menu)
        self.assertEqual(category.order, 1)

    def test_menu(self):
        """Test Menu model"""
        menu = Menu(
            id="test_id",
            name="Test Menu",
            categories=[],
            products=[],
            groups=[],
            version="1.0",
            organization_id="test_organization_id"
        )
        
        self.assertEqual(menu.id, "test_id")
        self.assertEqual(menu.name, "Test Menu")
        self.assertEqual(menu.categories, [])
        self.assertEqual(menu.products, [])
        self.assertEqual(menu.groups, [])
        self.assertEqual(menu.version, "1.0")
        self.assertEqual(menu.organization_id, "test_organization_id")

    def test_menu_response(self):
        """Test MenuResponse model"""
        menu = Menu(
            id="test_id",
            name="Test Menu",
            categories=[],
            products=[],
            groups=[],
            version="1.0",
            organization_id="test_organization_id"
        )
        
        response = MenuResponse(
            menus=[menu]
        )
        
        self.assertEqual(len(response.menus), 1)
        self.assertEqual(response.menus[0].id, "test_id")

    def test_order_item(self):
        """Test OrderItem model"""
        item = OrderItem(
            product_id="test_product_id",
            amount=1.0
        )
        
        self.assertEqual(item.product_id, "test_product_id")
        self.assertEqual(item.amount, 1.0)

    def test_order(self):
        """Test Order model"""
        order = Order(
            organization_id="test_organization_id",
            terminal_group_id="test_terminal_group_id",
            order_items=[
                OrderItem(
                    product_id="test_product_id",
                    amount=1.0
                )
            ]
        )
        
        self.assertEqual(order.organization_id, "test_organization_id")
        self.assertEqual(order.terminal_group_id, "test_terminal_group_id")
        self.assertEqual(len(order.order_items), 1)
        self.assertEqual(order.order_items[0].product_id, "test_product_id")

    def test_order_response(self):
        """Test OrderResponse model"""
        response = OrderResponse(
            order_id="test_order_id"
        )
        
        self.assertEqual(response.order_id, "test_order_id")

    def test_delivery(self):
        """Test Delivery model"""
        delivery = Delivery(
            organization_id="test_organization_id",
            terminal_group_id="test_terminal_group_id"
        )
        
        self.assertEqual(delivery.organization_id, "test_organization_id")
        self.assertEqual(delivery.terminal_group_id, "test_terminal_group_id")

    def test_delivery_response(self):
        """Test DeliveryResponse model"""
        response = DeliveryResponse(
            delivery_id="test_delivery_id"
        )
        
        self.assertEqual(response.delivery_id, "test_delivery_id")

    def test_address(self):
        """Test Address model"""
        address = Address(
            city="Test City",
            street="Test Street",
            house="Test House"
        )
        
        self.assertEqual(address.city, "Test City")
        self.assertEqual(address.street, "Test Street")
        self.assertEqual(address.house, "Test House")

    def test_customer(self):
        """Test Customer model"""
        customer = Customer(
            name="Test Customer",
            phone="Test Phone"
        )
        
        self.assertEqual(customer.name, "Test Customer")
        self.assertEqual(customer.phone, "Test Phone")

    def test_coordinates(self):
        """Test Coordinates model"""
        coordinates = Coordinates(
            latitude=1.0,
            longitude=2.0
        )
        
        self.assertEqual(coordinates.latitude, 1.0)
        self.assertEqual(coordinates.longitude, 2.0)


if __name__ == "__main__":
    unittest.main()
