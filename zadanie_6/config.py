import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://staging.booking-app.example/api")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
