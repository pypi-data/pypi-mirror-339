"""
Menu by ID example for iiko-pkg
"""

import json
import os
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


def get_menu(organization_id):
    """Get menu example"""
    print("\nGetting menu...")
    menu = client.get_menu([organization_id])

    print(f"Menu correlation ID: {menu.correlation_id}")
    print(f"Categories count: {len(menu.product_categories)}")
    print(f"Products count: {len(menu.products)}")
    print(f"Groups count: {len(menu.groups)}")
    print(f"Revision: {menu.revision}")

    # Print full menu response as JSON
    print("\nFull menu response:")
    print_json(menu.model_dump())

    # Return menu
    return menu


def get_external_menus(organization_id):
    """Get external menus example"""
    print("\nGetting external menus...")

    try:
        external_menus = client.get_external_menus([organization_id])
        print_json(external_menus)

        # Return first external menu ID if available
        if external_menus.get("externalMenus") and external_menus["externalMenus"]:
            return external_menus["externalMenus"][0]["id"]

        return None
    except Exception as e:
        print(f"Error getting external menus: {e}")
        return None


def get_menu_by_id(organization_id, menu_id):
    """Get menu by ID example"""
    print(f"\nGetting menu by ID: {menu_id}...")

    try:
        # Make direct API request to get raw response
        data = {
            "organizationIds": [organization_id],
            "externalMenuId": menu_id
        }

        # Use the client's _make_request method to get raw response
        response = client._make_request("POST", "/api/2/menu/by_id", data)

        # Print the raw response
        print("\nMenu by ID response:")
        print_json(response)

        # Access fields directly from the response
        if "id" in response:
            print(f"\nMenu ID: {response['id']}")
            print(f"Menu name: {response['name']}")

            if "itemCategories" in response:
                print(f"Item categories count: {len(response['itemCategories'])}")

                # Print first 3 categories
                if response['itemCategories']:
                    print("\nFirst 3 categories:")
                    for category in response['itemCategories'][:3]:
                        print(f"- {category['name']} (ID: {category['id']})")

                        # Print first 2 items in each category
                        if 'items' in category and category['items']:
                            for item in category['items'][:2]:
                                print(f"  * {item['name']} (SKU: {item['sku']})")

        return response
    except Exception as e:
        print(f"Error getting menu by ID: {e}")
        return None


def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Use the specific external menu ID from the Postman example
    menu_id = "41354"
    print(f"\nUsing external menu ID: {menu_id}")

    # Get menu by ID
    get_menu_by_id(organization_id, menu_id)


if __name__ == "__main__":
    main()
