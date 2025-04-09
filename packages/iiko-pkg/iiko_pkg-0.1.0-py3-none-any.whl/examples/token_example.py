"""
Token example for iiko-pkg
"""

import os
from datetime import datetime
from iiko_pkg import IikoClient

# Get API key from environment variable
API_KEY = os.environ.get("IIKO_API_KEY", "")

def main():
    """Main function"""
    # Initialize client
    client = IikoClient(api_key=API_KEY)

    # Get token
    token = client.get_token()

    # Print token info
    print(f"Token: {token.token}")
    print(f"Expire seconds: {token.expire_seconds}")
    print(f"Created at: {token.created_at}")
    print(f"Is expired: {token.is_expired()}")

    # Check if token is valid
    if not token.is_expired():
        print("\nToken is valid")
    else:
        print("\nToken is expired")

        # Get new token
        print("Getting new token...")
        new_token = client.get_token()

        # Print new token info
        print(f"New token: {new_token.token}")
        print(f"New expire seconds: {new_token.expire_seconds}")
        print(f"New created at: {new_token.created_at}")
        print(f"New is expired: {new_token.is_expired()}")

if __name__ == "__main__":
    main()
