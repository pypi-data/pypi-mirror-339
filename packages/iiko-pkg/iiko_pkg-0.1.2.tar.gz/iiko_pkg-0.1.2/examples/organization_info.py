"""
Organization info example for iiko-pkg
"""

import os
from iiko_pkg import IikoClient

# Get API key from environment variable
API_KEY = os.environ.get("IIKO_API_KEY", "")


def main():
    """Main function"""
    # Initialize client
    client = IikoClient(api_key=API_KEY)

    # Get organizations
    organizations = client.get_organizations(return_additional_info=True)
    print(f"Found {len(organizations.organizations)} organizations")

    # Print organization details
    for org in organizations.organizations:
        print(f"\nOrganization: {org.name}")
        print(f"ID: {org.id}")
        print(f"Country: {org.country}")
        print(f"Address: {org.restaurant_address}")
        print(f"Coordinates: {org.latitude}, {org.longitude}")
        print(f"Timezone: {org.timezone}")
        print(f"Currency: {org.currency}")
        print(f"Is active: {org.is_active}")
        print(f"Is delivery enabled: {org.is_delivery_enabled}")

        # Get terminal groups for this organization
        terminal_groups = client.get_terminal_groups([org.id])

        if "terminalGroups" in terminal_groups and terminal_groups["terminalGroups"]:
            print("\nTerminal groups:")
            for tg in terminal_groups["terminalGroups"]:
                if "items" in tg:
                    for item in tg["items"]:
                        print(f"- {item['name']} (ID: {item['id']})")


if __name__ == "__main__":
    main()
