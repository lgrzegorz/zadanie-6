from datetime import date, timedelta

import pytest

from api_client.booking_api import BookingApi
from config import API_URL, TEST_PASSWORD
from data import load
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def users():
    data = load("users.json")
    for user in data["valid"].values():
        user["password"] = TEST_PASSWORD
    return data


@pytest.fixture(scope="session")
def booking_data():
    return load("booking.json")


@pytest.fixture
def booking_date():
    # tydzień do przodu, żeby nie trafić na reguły anulowania 24 h
    return date.today() + timedelta(days=7)


@pytest.fixture
def api_as(users):
    clients = []

    def login_as(user_key):
        user = users["valid"][user_key]
        client = BookingApi(API_URL)
        client.login(user["email"], user["password"])
        clients.append(client)
        return client

    yield login_as

    for client in clients:
        client.cancel_created_reservations()


@pytest.fixture
def logged_in_page(page, users):
    user = users["valid"]["client1"]
    LoginPage(page).open().login(user["email"], user["password"])
    return page
