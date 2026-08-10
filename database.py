import os
import sys
import pyodbc
from dotenv import load_dotenv


# ==========================================================
# Load .env
# ==========================================================

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))


# ==========================================================
# Helper
# ==========================================================

def get_env(key):
    value = os.getenv(key)

    if value is None or value.strip() == "":
        raise Exception(f"{key} not found in .env")

    return value


# ==========================================================
# Database Configuration
# ==========================================================

CONNECTION_STRING = (
    f"DRIVER={{{get_env('DB_DRIVER')}}};"
    f"SERVER={get_env('DB_SERVER')};"
    f"DATABASE={get_env('DB_NAME')};"
    f"UID={get_env('DB_USER')};"
    f"PWD={get_env('DB_PASSWORD')};"
)


# ==========================================================
# API Configuration
# ==========================================================

API_KEY_CODE = get_env("API_KEY_CODE")


# ==========================================================
# Server Configuration
# ==========================================================

HOST = get_env("HOST")

PORT = int(get_env("PORT"))

GETPORT = int(get_env("GETPORT"))

POSTPORT = int(get_env("POSTPORT"))

MGETPORT = int(
    os.getenv("MGETPORT", "8003")
)
MPOSTPORT = int(
    os.getenv("MPOSTPORT", "8004")
)

MEDIAPATH = os.getenv(
    "MEDIAPATH",
    r"F:\Media"
)

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = get_env("LOG_LEVEL")

DEBUG = get_env("DEBUG").lower() == "true"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():
    return pyodbc.connect(CONNECTION_STRING)
