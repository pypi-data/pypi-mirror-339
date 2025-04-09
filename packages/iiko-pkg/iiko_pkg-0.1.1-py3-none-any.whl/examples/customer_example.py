"""
Customer example for iiko-pkg
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

def get_customer_info(organization_id, phone="+1234567890"):
    """Get customer info example"""
    print(f"\nGetting customer info for phone: {phone}...")

    try:
        customer_info = client.get_customer_info(
            organization_id=organization_id,
            phone=phone
        )
        print_json(customer_info)
        return customer_info
    except Exception as e:
        print(f"Error getting customer info: {e}")
        return None

def create_or_update_customer(organization_id, phone="+1234567890"):
    """Create or update customer example"""
    print(f"\nCreating or updating customer with phone: {phone}...")

    customer_data = {
        "name": "John Doe",
        "surname": "Smith",
        "phone": phone,
        "email": "john.doe@example.com",
        "birthday": "1990-01-01",
        "sex": "Male",
        "comment": "Test customer",
        "address": {
            "city": "Moscow",
            "street": "Tverskaya",
            "house": "1",
            "apartment": "10",
            "entrance": "1",
            "floor": "1",
            "comment": "Test address"
        }
    }

    try:
        customer = client.create_or_update_customer(
            organization_id=organization_id,
            customer=customer_data
        )
        print_json(customer)
        return customer
    except Exception as e:
        print(f"Error creating or updating customer: {e}")
        return None

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Generate a unique phone number for testing
    import random
    phone = f"+7{random.randint(1000000000, 9999999999)}"

    # Create or update customer
    customer = create_or_update_customer(organization_id, phone)

    if not customer:
        print("Failed to create or update customer")
        return

    # Get customer info
    get_customer_info(organization_id, phone)

if __name__ == "__main__":
    main()
