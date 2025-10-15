import requests

# URL for the account delete endpoint
url = "http://127.0.0.1:8000/user_delete_account"  # Match with the Django URL

# Headers including the token
headers = {
    "Token": "9be162176aeb78d14f3d2e9a71d6dfd043b36367",  # Replace with your actual token
}

try:
    # Send the POST request to delete the account
    response = requests.post(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print(f"Failed to delete account. Status Code: {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
