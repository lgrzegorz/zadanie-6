import re

import pytest
from playwright.sync_api import expect

from pages.header import Header
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_valid_credentials(page, users):
    user = users["client1"]

    LoginPage(page).open().login(user["email"], user["password"])

    expect(page).not_to_have_url(re.compile(r"/login"))
    expect(Header(page).user_menu).to_contain_text(user["name"])
