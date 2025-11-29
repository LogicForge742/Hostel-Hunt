import requests
import json
import time

# Deployed backend URL
API_BASE_URL = 'https://hostel-hunt-11.onrender.com'

def test_landlord_registration():
    """Test registering as a landlord using the deployed API"""

    # Generate unique email to avoid conflicts
    timestamp = int(time.time())
    test_email = f"test_landlord_{timestamp}@example.com"

    # Test data for landlord registration
    registration_data = {
        "name": "Test Landlord",
        "email": test_email,
        "password": "TestPass123!",
        "phone_number": "0712345678",
        "role": "landlord"
    }

    print("Testing landlord registration on deployed API...")
    print(f"API URL: {API_BASE_URL}/auth/register")
    print(f"Test data: {json.dumps(registration_data, indent=2)}")

    try:
        # Make the registration request
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=registration_data,
            headers={'Content-Type': 'application/json'}
        )

        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 201:
            response_data = response.json()
            print("✅ Registration successful!")
            print(f"Response: {json.dumps(response_data, indent=2)}")

            # Verify the response structure
            if 'message' in response_data and response_data['message'] == 'Registration successful':
                print("✅ Success message correct")
            else:
                print("❌ Success message missing or incorrect")

            if 'user' in response_data:
                user = response_data['user']
                print("✅ User data returned")
                if user.get('role') == 'landlord':
                    print("✅ User role is landlord")
                else:
                    print("❌ User role is not landlord")
            else:
                print("❌ User data missing")

            if 'access_token' in response_data and 'refresh_token' in response_data:
                print("✅ Tokens returned")
            else:
                print("❌ Tokens missing")

        elif response.status_code == 400:
            error_data = response.json()
            print("❌ Registration failed with validation error:")
            print(f"Error: {json.dumps(error_data, indent=2)}")

        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse response JSON: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    test_landlord_registration()
