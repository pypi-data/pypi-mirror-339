"""
Basic usage examples for iiko-pkg
"""

import os
import json
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


def get_menu(organization_id):
    """Get menu example"""
    print("\nGetting menu...")
    menu = client.get_menu([organization_id])

    print(f"Menu correlation ID: {menu.correlation_id}")
    print(f"Categories count: {len(menu.product_categories)}")
    print(f"Products count: {len(menu.products)}")
    print(f"Groups count: {len(menu.groups)}")

    # Print first 5 products
    if menu.products:
        print("\nFirst 5 products:")
        for product in menu.products[:5]:
            print(f"- {product.name} (ID: {product.id}, Price: {product.price})")


def get_payment_types(organization_id):
    """Get payment types example"""
    print("\nGetting payment types...")
    payment_types = client.get_payment_types([organization_id])
    print_json(payment_types)


def get_order_types(organization_id):
    """Get order types example"""
    print("\nGetting order types...")
    order_types = client.get_order_types([organization_id])
    print_json(order_types)


def create_order_example(organization_id, terminal_group_id):
    """Create order example"""
    print("\nCreating order...")

    # First get menu to find product IDs
    menu = client.get_menu([organization_id])

    if not menu.products:
        print("No products found in menu")
        return

    # Use first product from menu
    product = menu.products[0]

    # Create order
    order_data = {
        "items": [
            {
                "productId": product.id,
                "amount": 1
            }
        ],
        "phone": "+1234567890",
        "customer": {
            "name": "John Doe"
        }
    }

    try:
        order_response = client.create_order(
            organization_id=organization_id,
            terminal_group_id=terminal_group_id,
            order=order_data
        )

        print(f"Order created with ID: {order_response.order_id}")
        return order_response.order_id
    except Exception as e:
        print(f"Error creating order: {e}")
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

    # Get menu
    get_menu(organization_id)

    # Get payment types
    get_payment_types(organization_id)

    # Get order types
    get_order_types(organization_id)

    # Create order example
    create_order_example(organization_id, terminal_group_id)


if __name__ == "__main__":
    main()
