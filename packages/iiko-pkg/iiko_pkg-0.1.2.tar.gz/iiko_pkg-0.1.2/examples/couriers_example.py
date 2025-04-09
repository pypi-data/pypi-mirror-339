"""
Couriers example for iiko-pkg
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

def get_couriers(organization_id):
    """Get couriers example"""
    print("\nGetting couriers...")

    try:
        couriers = client.get_couriers([organization_id])
        print_json(couriers)

        # Return courier IDs
        if couriers.get("employees") and couriers["employees"][0].get("items"):
            return [item["id"] for employee in couriers["employees"] for item in employee["items"]]

        return []
    except Exception as e:
        print(f"Error getting couriers: {e}")
        return []

def get_couriers_active_location(organization_id):
    """Get couriers active location example"""
    print("\nGetting couriers active location...")

    try:
        active_locations = client.get_couriers_active_location([organization_id])
        print_json(active_locations)
        return active_locations
    except Exception as e:
        print(f"Error getting couriers active location: {e}")
        return None

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get couriers
    courier_ids = get_couriers(organization_id)

    if not courier_ids:
        print("No couriers found")

    # Get couriers active location
    get_couriers_active_location(organization_id)

if __name__ == "__main__":
    main()
