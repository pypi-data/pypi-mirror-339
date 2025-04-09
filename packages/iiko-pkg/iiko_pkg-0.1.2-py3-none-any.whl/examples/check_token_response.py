"""
Check token response for iiko-pkg
"""
import os

import requests
import json

# Use the provided API key
API_KEY = os.environ.get("IIKO_API_KEY", "")


def main():
    """Main function"""
    # Make request to get token
    response = requests.post(
        "https://api-ru.iiko.services/api/1/access_token",
        json={"apiLogin": API_KEY},
        timeout=10
    )

    # Print response
    print("Response status code:", response.status_code)
    print("Response headers:", response.headers)
    print("Response content:", response.content.decode())

    # Parse response
    try:
        data = response.json()
        print("\nParsed response:")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print("Error parsing response:", e)


if __name__ == "__main__":
    main()
