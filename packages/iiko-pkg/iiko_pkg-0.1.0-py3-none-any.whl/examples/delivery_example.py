"""
Delivery example for iiko-pkg
"""

import os
import json
from datetime import datetime, timedelta
from iiko_pkg import IikoClient

# Get API key from environment variable
API_KEY = os.environ.get("IIKO_API_KEY", "")

# Initialize client
client = IikoClient(api_key=API_KEY)

def print_json(data):
    """Print data as formatted JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def get_organizations():
    """Get organizations example"""
    print("Getting organizations...")
    organizations = client.get_organizations()
    print(f"Found {len(organizations.organizations)} organizations")

    # Print first organization
    if organizations.organizations:
        print("\nFirst organization:")
        org = organizations.organizations[0]
        print(f"ID: {org.id}")
        print(f"Name: {org.name}")
        print(f"Address: {org.restaurant_address}")

        # Return first organization ID for other examples
        return org.id

    return None

def get_terminal_groups(organization_id):
    """Get terminal groups example"""
    print("\nGetting terminal groups...")
    terminal_groups = client.get_terminal_groups([organization_id])
    print_json(terminal_groups)

    # Return first terminal group ID for other examples
    if terminal_groups.get("terminalGroups") and terminal_groups["terminalGroups"][0].get("items"):
        return terminal_groups["terminalGroups"][0]["items"][0]["id"]

    return None

def get_order_types(organization_id):
    """Get order types example"""
    print("\nGetting order types...")
    order_types = client.get_order_types([organization_id])
    print_json(order_types)

    # Return first delivery order type ID
    if order_types.get("orderTypes") and order_types["orderTypes"][0].get("items"):
        for order_type in order_types["orderTypes"][0]["items"]:
            if order_type.get("orderServiceType") == "DeliveryByCourier":
                return order_type["id"]

    return None

def get_payment_types(organization_id):
    """Get payment types example"""
    print("\nGetting payment types...")
    payment_types = client.get_payment_types([organization_id])
    print_json(payment_types)

    # Return first cash payment type ID
    if payment_types.get("paymentTypes"):
        for payment_type in payment_types["paymentTypes"]:
            if payment_type.get("paymentTypeKind") == "Cash":
                return payment_type["id"]

    return None

def create_delivery_example(organization_id, terminal_group_id, order_type_id, payment_type_id):
    """Create delivery example"""
    print("\nCreating delivery...")

    # First get menu to find product IDs
    menu = client.get_menu([organization_id])

    if not menu.products:
        print("No products found in menu")
        return

    # Use first product from menu
    product = menu.products[0]

    # Create delivery
    delivery_time = datetime.now() + timedelta(hours=1)

    delivery_data = {
        "orderServiceType": "DeliveryByCourier",
        "orderTypeId": order_type_id,
        "deliveryPoint": {
            "address": {
                "city": "Moscow",
                "street": "Tverskaya",
                "house": "1",
                "apartment": "10"
            },
            "comment": "Delivery comment"
        },
        "items": [
            {
                "productId": product.id,
                "amount": 1
            }
        ],
        "payments": [
            {
                "paymentTypeId": payment_type_id,
                "sum": product.price,
                "isPrepay": False
            }
        ],
        "phone": "+1234567890",
        "customer": {
            "name": "John Doe",
            "comment": "Customer comment"
        },
        "deliveryDate": delivery_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    }

    try:
        delivery_response = client.create_delivery(
            organization_id=organization_id,
            terminal_group_id=terminal_group_id,
            delivery=delivery_data
        )

        print(f"Delivery created with ID: {delivery_response.delivery_id}")
        return delivery_response.delivery_id
    except Exception as e:
        print(f"Error creating delivery: {e}")
        return None

def get_delivery_by_id(organization_id, delivery_id):
    """Get delivery by ID example"""
    print("\nGetting delivery by ID...")

    try:
        delivery = client.get_delivery_by_id([organization_id], [delivery_id])
        print_json(delivery.model_dump())
        return delivery
    except Exception as e:
        print(f"Error getting delivery: {e}")
        return None

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get terminal groups
    terminal_group_id = get_terminal_groups(organization_id)

    if not terminal_group_id:
        print("No terminal groups found")
        return

    # Get order types
    order_type_id = get_order_types(organization_id)

    if not order_type_id:
        print("No delivery order types found")
        return

    # Get payment types
    payment_type_id = get_payment_types(organization_id)

    if not payment_type_id:
        print("No cash payment types found")
        return

    # Create delivery example
    delivery_id = create_delivery_example(
        organization_id,
        terminal_group_id,
        order_type_id,
        payment_type_id
    )

    if not delivery_id:
        print("Failed to create delivery")
        return

    # Get delivery by ID
    get_delivery_by_id(organization_id, delivery_id)

if __name__ == "__main__":
    main()
