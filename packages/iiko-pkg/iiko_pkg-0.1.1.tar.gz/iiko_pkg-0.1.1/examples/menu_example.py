"""
Menu example for iiko-pkg
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

def get_menu(organization_id):
    """Get menu example"""
    print("\nGetting menu...")
    menu = client.get_menu([organization_id])

    print(f"Menu correlation ID: {menu.correlation_id}")
    print(f"Categories count: {len(menu.product_categories)}")
    print(f"Products count: {len(menu.products)}")
    print(f"Groups count: {len(menu.groups)}")

    # Print categories
    if menu.product_categories:
        print("\nCategories:")
        for category in menu.product_categories:
            print(f"- {category.name} (ID: {category.id})")

    # Print first 5 products
    if menu.products:
        print("\nFirst 5 products:")
        for product in menu.products[:5]:
            print(f"- {product.name} (ID: {product.id}, Price: {product.price})")

    return menu

def get_stop_lists(organization_id):
    """Get stop lists example"""
    print("\nGetting stop lists...")
    stop_lists = client.get_stop_lists([organization_id])
    print_json(stop_lists)

    return stop_lists

def print_product_details(product):
    """Print product details"""
    print(f"\nProduct details for: {product.name}")
    print(f"ID: {product.id}")
    print(f"Price: {product.price}")
    print(f"Category ID: {product.category_id}")

    if product.description:
        print(f"Description: {product.description}")

    if product.additional_info:
        print(f"Additional info: {product.additional_info}")

    if product.code:
        print(f"Code: {product.code}")

    if product.article_number:
        print(f"Article number: {product.article_number}")

    print(f"Is deleted: {product.is_deleted}")
    print(f"Is hidden: {product.is_hidden}")
    print(f"Is included in menu: {product.is_included_in_menu}")

    if product.tags:
        print(f"Tags: {', '.join(product.tags)}")

    if product.sizes:
        print("\nSizes:")
        for size in product.sizes:
            print(f"- {size.name} (ID: {size.id}, Priority: {size.priority}, Default: {size.is_default})")

    if product.modifiers:
        print("\nModifiers:")
        for modifier in product.modifiers:
            print(f"- {modifier.name} (ID: {modifier.id}, Price: {modifier.price})")
            print(f"  Min: {modifier.min_amount}, Max: {modifier.max_amount}, Default: {modifier.default_amount}")

    if product.modifier_groups:
        print("\nModifier groups:")
        for group in product.modifier_groups:
            print(f"- {group.name} (ID: {group.id})")
            if group.modifiers:
                for modifier in group.modifiers:
                    print(f"  - {modifier.name} (ID: {modifier.id}, Price: {modifier.price})")

    if product.image_urls:
        print("\nImage URLs:")
        for url in product.image_urls:
            print(f"- {url}")

    # Nutritional information
    nutritional_info = []
    if product.weight is not None:
        nutritional_info.append(f"Weight: {product.weight} {product.measure_unit or ''}")
    if product.energy_value is not None:
        nutritional_info.append(f"Energy: {product.energy_value} {product.energy_unit or ''}")
    if product.protein is not None:
        nutritional_info.append(f"Protein: {product.protein}g")
    if product.fat is not None:
        nutritional_info.append(f"Fat: {product.fat}g")
    if product.carbohydrate is not None:
        nutritional_info.append(f"Carbohydrate: {product.carbohydrate}g")
    if product.fiber is not None:
        nutritional_info.append(f"Fiber: {product.fiber}g")

    if nutritional_info:
        print("\nNutritional information:")
        for info in nutritional_info:
            print(f"- {info}")

    # Dietary information
    dietary_info = []
    if product.organic:
        dietary_info.append("Organic")
    if product.vegetarian:
        dietary_info.append("Vegetarian")
    if product.gluten_free:
        dietary_info.append("Gluten free")
    if product.lactose_free:
        dietary_info.append("Lactose free")
    if product.spicy:
        dietary_info.append("Spicy")

    if dietary_info:
        print("\nDietary information:")
        for info in dietary_info:
            print(f"- {info}")

    if product.allergens:
        print("\nAllergens:")
        for allergen in product.allergens:
            print(f"- {allergen}")

def main():
    """Main function"""
    # Get organizations
    organization_id = get_organizations()

    if not organization_id:
        print("No organizations found")
        return

    # Get menu
    menu = get_menu(organization_id)

    if not menu:
        print("No menu found")
        return

    # Get stop lists
    stop_lists = get_stop_lists(organization_id)

    # Print details for first product
    if menu.products:
        print_product_details(menu.products[0])

if __name__ == "__main__":
    main()
