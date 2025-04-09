"""
Quick test for iiko-pkg
"""

import os
from iiko_pkg import IikoClient

# Get API key from environment variable
API_KEY = os.environ.get("IIKO_API_KEY", "")


def main():
    """Main function"""
    # Initialize client
    client = IikoClient(api_key=API_KEY)

    # Get token
    token = client.get_token()
    print(f"Token: {token.token}")
    print(f"Expire seconds: {token.expire_seconds}")
    print(f"Created at: {token.created_at}")
    print(f"Is expired: {token.is_expired()}")

    # Get organizations
    organizations = client.get_organizations()
    print(f"\nFound {len(organizations.organizations)} organizations")

    if organizations.organizations:
        org = organizations.organizations[0]
        print(f"First organization: {org.name} (ID: {org.id})")

        # Get terminal groups
        terminal_groups = client.get_terminal_groups([org.id])
        print(f"\nTerminal groups: {terminal_groups}")

        # Get menu
        menu = client.get_menu([org.id])
        print(f"\nMenu correlation ID: {menu.correlation_id}")
        print(f"Categories: {len(menu.product_categories)}")
        print(f"Products: {len(menu.products)}")
        print(f"Groups: {len(menu.groups)}")

        if menu.products:
            print(f"\nFirst product: {menu.products[0].name}")
            print(f"Price: {menu.products[0].price}")


if __name__ == "__main__":
    main()
