"""
Menu detailed example for iiko-pkg
"""

import json
from iiko_pkg import IikoClient

# Use the provided API key
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
    
    # Print all organizations
    print("\nOrganizations:")
    for org in organizations.organizations:
        print(f"- {org.name} (ID: {org.id})")
        
    # Return first organization ID for other examples
    if organizations.organizations:
        return organizations.organizations[0].id
    
    return None

def get_menu(organization_id):
    """Get menu example"""
    print("\nGetting menu...")
    menu = client.get_menu([organization_id])
    
    print(f"Menu correlation ID: {menu.correlation_id}")
    print(f"Categories count: {len(menu.product_categories)}")
    print(f"Products count: {len(menu.products)}")
    print(f"Groups count: {len(menu.groups)}")
    print(f"Sizes count: {len(menu.sizes)}")
    print(f"Revision: {menu.revision}")
    
    # Print categories
    if menu.product_categories:
        print("\nCategories:")
        for category in menu.product_categories:
            print(f"- {category.name} (ID: {category.id})")
    else:
        print("\nNo categories found")
    
    # Print products
    if menu.products:
        print("\nProducts:")
        for product in menu.products:
            print(f"- {product.name} (ID: {product.id}, Price: {product.price})")
    else:
        print("\nNo products found")
    
    # Print groups
    if menu.groups:
        print("\nGroups:")
        for group in menu.groups:
            print(f"- {group.name} (ID: {group.id})")
    else:
        print("\nNo groups found")
    
    # Print sizes
    if menu.sizes:
        print("\nSizes:")
        for size in menu.sizes:
            print(f"- {size.name} (ID: {size.id})")
    else:
        print("\nNo sizes found")
    
    return menu

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()
    
    if not organization_id:
        print("No organizations found")
        return
    
    # Get menu
    get_menu(organization_id)

if __name__ == "__main__":
    main()
