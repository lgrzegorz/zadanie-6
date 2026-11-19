from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page):
        super().__init__(page)
        self.email_input = page.get_by_test_id("login-email")
        self.password_input = page.get_by_test_id("login-password")
        self.submit_button = page.get_by_role("button", name="Zaloguj się")
        self.error_message = page.get_by_test_id("login-error")

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
