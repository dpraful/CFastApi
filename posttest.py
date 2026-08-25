import requests
import json


# ==========================================================
# CONFIG
# ==========================================================

URL = "http://100.105.213.12:8000/pixapost/commonpost"


# ==========================================================
# INSERT TEST
# ==========================================================

insert_payload = {
    "groups": {
        "option": "rnpiusersave",
        "flag": 1,

        "username": "testuser",
        "email": "test@example.com",
        "passwordhash": "test_hash_123",

        "fullname": "Test User",
        "dob": "1995-08-09",
        "gender": "Male",
        "phonenumber": "9876543210",

        "profilepicture": None,
        "bio": "Test user from Python API",
        "location": "Thrissur, India",
        "website": "https://example.com",

        "isverified": False,
        "status": "Active"
    }
}


# ==========================================================
# SEND INSERT REQUEST
# ==========================================================

try:

    print("=" * 60)
    print("INSERT USER")
    print("=" * 60)

    response = requests.post(
        URL,
        json=insert_payload,
        timeout=30
    )

    print("HTTP STATUS:", response.status_code)

    print("\nRAW RESPONSE:")
    print(response.text)

    try:

        result = response.json()

        print("\nPRETTY RESPONSE:")
        print(
            json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            )
        )

    except ValueError:

        print("\nResponse is not valid JSON.")


except requests.exceptions.RequestException as e:

    print("\nREQUEST ERROR:")
    print(e)


# ==========================================================
# UPDATE TEST
# ==========================================================
#
# Change this userid to an existing userid in piusers.
#
# ==========================================================

update_payload = {
    "groups": {
        "option": "rnpiusersave",
        "flag": 2,

        "userid": 1,

        "username": "amal123",
        "email": "amal@example.com",
        "passwordhash": "updated_hash_123",

        "fullname": "Amal Kumar Updated",
        "dob": "1995-08-09",
        "gender": "Male",
        "phonenumber": "9876543210",

        "profilepicture": None,
        "bio": "Updated user profile",
        "location": "Thrissur, India",
        "website": "https://amal.dev",

        "isverified": False,
        "status": "Active"
    }
}


# ==========================================================
# SEND UPDATE REQUEST
# ==========================================================

try:

    print("\n")
    print("=" * 60)
    print("UPDATE USER")
    print("=" * 60)

    response = requests.post(
        URL,
        json=update_payload,
        timeout=30
    )

    print("HTTP STATUS:", response.status_code)

    print("\nRAW RESPONSE:")
    print(response.text)

    try:

        result = response.json()

        print("\nPRETTY RESPONSE:")
        print(
            json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            )
        )

    except ValueError:

        print("\nResponse is not valid JSON.")


except requests.exceptions.RequestException as e:

    print("\nREQUEST ERROR:")
    print(e)