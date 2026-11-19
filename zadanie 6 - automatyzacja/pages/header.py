class Header:
    def __init__(self, page):
        self.user_menu = page.get_by_test_id("user-menu")
        self.logout_button = page.get_by_role("button", name="Wyloguj")
