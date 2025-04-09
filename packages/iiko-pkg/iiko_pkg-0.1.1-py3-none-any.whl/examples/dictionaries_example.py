"""
Dictionaries example for iiko-pkg
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

def get_payment_types(organization_id):
    """Get payment types example"""
    print("\nGetting payment types...")

    try:
        payment_types = client.get_payment_types([organization_id])
        print_json(payment_types)
        return payment_types
    except Exception as e:
        print(f"Error getting payment types: {e}")
        return None

def get_order_types(organization_id):
    """Get order types example"""
    print("\nGetting order types...")

    try:
        order_types = client.get_order_types([organization_id])
        print_json(order_types)
        return order_types
    except Exception as e:
        print(f"Error getting order types: {e}")
        return None

def get_discounts(organization_id):
    """Get discounts example"""
    print("\nGetting discounts...")

    try:
        discounts = client.get_discounts([organization_id])
        print_json(discounts)
        return discounts
    except Exception as e:
        print(f"Error getting discounts: {e}")
        return None

def get_cancel_causes(organization_id):
    """Get cancel causes example"""
    print("\nGetting cancel causes...")

    try:
        cancel_causes = client.get_cancel_causes([organization_id])
        print_json(cancel_causes)
        return cancel_causes
    except Exception as e:
        print(f"Error getting cancel causes: {e}")
        return None

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get payment types
    get_payment_types(organization_id)

    # Get order types
    get_order_types(organization_id)

    # Get discounts
    get_discounts(organization_id)

    # Get cancel causes
    get_cancel_causes(organization_id)

if __name__ == "__main__":
    main()
