import requests
import os


# ==========================================================
# CONFIGURATION
# ==========================================================

URL = "http://127.0.0.1:8004/commonmpost"

FILE_PATH = r"C:\Users\PRAFUL\Pictures\consultant.jpg"


# ==========================================================
# CHECK FILE
# ==========================================================

if not os.path.isfile(FILE_PATH):

    print("File not found:")
    print(FILE_PATH)
    exit()


# ==========================================================
# UPLOAD FILE
# ==========================================================

try:

    with open(FILE_PATH, "rb") as file:

        files = {
            "file": (
                os.path.basename(FILE_PATH),
                file
            )
        }

        response = requests.post(
            URL,
            files=files
        )


    # ======================================================
    # RESPONSE
    # ======================================================

    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)


except requests.exceptions.RequestException as e:

    print("Request failed:")
    print(e)
