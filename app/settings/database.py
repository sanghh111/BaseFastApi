import os

POSTGRES_CONFIG = {
    "host": os.getenv(f"POSTGRES_HOST"),
    "port": os.getenv(f"POSTGRES_PORT"),
    "username": os.getenv(f"POSTGRES_USERNAME"),
    "password": os.getenv(f"POSTGRES_PASSWORD"),
    "service_name": os.getenv(f"POSTGRES_SERVICE_NAME")
}
