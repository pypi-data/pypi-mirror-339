"""
Marketing sources example for iiko-pkg
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

def get_marketing_sources(organization_id):
    """Get marketing sources example"""
    print("\nGetting marketing sources...")

    try:
        marketing_sources = client.get_marketing_sources([organization_id])
        print_json(marketing_sources)
        return marketing_sources
    except Exception as e:
        print(f"Error getting marketing sources: {e}")
        return None

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get marketing sources
    get_marketing_sources(organization_id)

if __name__ == "__main__":
    main()
