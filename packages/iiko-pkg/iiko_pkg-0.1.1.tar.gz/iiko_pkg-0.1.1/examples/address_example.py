"""
Address example for iiko-pkg
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


def get_regions(organization_id):
    """Get regions example"""
    print("\nGetting regions...")

    try:
        regions = client.get_regions([organization_id])
        print_json(regions)

        # Return first region ID
        if regions.get("regions"):
            return regions["regions"][0]["id"]

        return None
    except Exception as e:
        print(f"Error getting regions: {e}")
        return None


def get_cities(organization_id, region_id=None):
    """Get cities example"""
    print("\nGetting cities...")

    try:
        cities = client.get_cities(
            organization_ids=[organization_id],
            region_ids=[region_id] if region_id else None
        )
        print_json(cities)

        # Return first city ID
        if cities.get("cities") and cities["cities"][0].get("items"):
            return cities["cities"][0]["items"][0]["id"]

        return None
    except Exception as e:
        print(f"Error getting cities: {e}")
        return None


def get_streets_by_city(organization_id, city_id):
    """Get streets by city example"""
    print("\nGetting streets by city...")

    if not city_id:
        print("No city ID provided")
        return None

    try:
        streets = client.get_streets_by_city(
            organization_id=organization_id,
            city_id=city_id
        )
        print_json(streets)
        return streets
    except Exception as e:
        print(f"Error getting streets: {e}")
        return None


def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get regions
    region_id = get_regions(organization_id)

    # Get cities
    city_id = get_cities(organization_id, region_id)

    if not city_id:
        print("No cities found")
        return

    # Get streets by city
    get_streets_by_city(organization_id, city_id)


if __name__ == "__main__":
    main()
