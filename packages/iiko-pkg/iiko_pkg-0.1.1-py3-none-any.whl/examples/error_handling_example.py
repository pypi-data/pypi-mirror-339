"""
Error handling example for iiko-pkg
"""

import os
from iiko_pkg import IikoClient
from iiko_pkg.exceptions import AuthenticationError, ApiError, NetworkError, ValidationError

# Get API key from environment variable
API_KEY = os.environ.get("IIKO_API_KEY", "")

def authentication_error_example():
    """Authentication error example"""
    print("\nAuthentication error example...")

    # Initialize client with invalid API key
    client = IikoClient(api_key="invalid_api_key")

    try:
        # Try to get organizations
        organizations = client.get_organizations()
        print(f"Found {len(organizations.organizations)} organizations")
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except ApiError as e:
        print(f"API error {e.status_code}: {e.error_message}")
    except NetworkError as e:
        print(f"Network error: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def api_error_example():
    """API error example"""
    print("\nAPI error example...")

    # Initialize client with valid API key
    client = IikoClient(api_key=API_KEY)

    try:
        # Try to get order by invalid ID
        order = client.get_order_by_id(
            organization_ids=["invalid_organization_id"],
            order_ids=["invalid_order_id"]
        )
        print(f"Order: {order}")
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except ApiError as e:
        print(f"API error {e.status_code}: {e.error_message}")
    except NetworkError as e:
        print(f"Network error: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def network_error_example():
    """Network error example"""
    print("\nNetwork error example...")

    # Initialize client with invalid base URL
    client = IikoClient(api_key=API_KEY, base_url="https://invalid-url.example.com")

    try:
        # Try to get organizations
        organizations = client.get_organizations()
        print(f"Found {len(organizations.organizations)} organizations")
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except ApiError as e:
        print(f"API error {e.status_code}: {e.error_message}")
    except NetworkError as e:
        print(f"Network error: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def validation_error_example():
    """Validation error example"""
    print("\nValidation error example...")

    # Initialize client with valid API key
    client = IikoClient(api_key=API_KEY)

    try:
        # Get organizations
        organizations = client.get_organizations()

        if not organizations.organizations:
            print("No organizations found")
            return

        # Try to create order with invalid data
        order_response = client.create_order(
            organization_id=organizations.organizations[0].id,
            terminal_group_id="invalid_terminal_group_id",
            order={
                "items": [
                    {
                        "productId": "invalid_product_id",
                        "amount": 1
                    }
                ]
            }
        )
        print(f"Order created with ID: {order_response.order_id}")
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except ApiError as e:
        print(f"API error {e.status_code}: {e.error_message}")
    except NetworkError as e:
        print(f"Network error: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    """Main function"""
    print("Error handling examples")

    # Authentication error example
    authentication_error_example()

    # API error example
    api_error_example()

    # Network error example
    network_error_example()

    # Validation error example
    validation_error_example()

if __name__ == "__main__":
    main()
