"""
Check menu response for iiko-pkg
"""

import requests
import json

# Use the provided API key
API_KEY = os.environ.get("IIKO_API_KEY", "")

def main():
    """Main function"""
    # First get token
    token_response = requests.post(
        "https://api-ru.iiko.services/api/1/access_token",
        json={"apiLogin": API_KEY}
    )
    
    token_data = token_response.json()
    token = token_data["token"]
    
    # Get organizations
    org_response = requests.post(
        "https://api-ru.iiko.services/api/1/organizations",
        headers={"Authorization": f"Bearer {token}"},
        json={"returnAdditionalInfo": False, "includeDisabled": False}
    )
    
    org_data = org_response.json()
    org_id = org_data["organizations"][0]["id"]
    
    # Make request to get menu
    menu_response = requests.post(
        "https://api-ru.iiko.services/api/1/nomenclature",
        headers={"Authorization": f"Bearer {token}"},
        json={"organizationId": org_id}
    )
    
    # Print response
    print("Response status code:", menu_response.status_code)
    print("Response headers:", menu_response.headers)
    
    # Parse response
    try:
        data = menu_response.json()
        print("\nParsed response keys:", list(data.keys()))
        print("\nFirst few keys in the response:")
        for key in list(data.keys())[:5]:
            print(f"- {key}")
    except Exception as e:
        print("Error parsing response:", e)

if __name__ == "__main__":
    main()
