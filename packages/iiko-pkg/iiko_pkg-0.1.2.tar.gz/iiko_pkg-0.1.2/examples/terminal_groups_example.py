"""
Terminal groups example for iiko-pkg
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

    # Return terminal group IDs
    if terminal_groups.get("terminalGroups") and terminal_groups["terminalGroups"][0].get("items"):
        return [item["id"] for tg in terminal_groups["terminalGroups"] for item in tg["items"]]

    return []

def check_terminal_groups_alive(organization_id, terminal_group_ids):
    """Check terminal groups alive example"""
    print("\nChecking terminal groups alive...")

    if not terminal_group_ids:
        print("No terminal group IDs provided")
        return

    try:
        alive_status = client.check_terminal_groups_alive(
            organization_ids=[organization_id],
            terminal_group_ids=terminal_group_ids
        )
        print_json(alive_status)
        return alive_status
    except Exception as e:
        print(f"Error checking terminal groups alive: {e}")
        return None

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get terminal groups
    terminal_group_ids = get_terminal_groups(organization_id)

    if not terminal_group_ids:
        print("No terminal groups found")
        return

    # Check terminal groups alive
    check_terminal_groups_alive(organization_id, terminal_group_ids)

if __name__ == "__main__":
    main()
