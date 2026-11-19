import re

import pytest
from playwright.sync_api import expect

from data import load
from pages.header import Header
from pages.login_page import LoginPage

INVALID_LOGINS = load("users.json")["invalid"]


@pytest.mark.smoke
def test_login_with_valid_credentials(page, users):
    user = users["valid"]["client1"]

    LoginPage(page).open().login(user["email"], user["password"])

    expect(page).not_to_have_url(re.compile(r"/login"))
    expect(Header(page).user_menu).to_contain_text(user["name"])


@pytest.mark.parametrize("case", INVALID_LOGINS, ids=[c["case"] for c in INVALID_LOGINS])
def test_login_with_invalid_credentials(page, case):
    login_page = LoginPage(page).open()

    login_page.login(case["email"], case["password"])

    expect(login_page.error_message).to_have_text(case["error"])
    expect(page).to_have_url(re.compile(r"/login"))
