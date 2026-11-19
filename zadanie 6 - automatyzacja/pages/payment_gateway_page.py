from pages.base_page import BasePage


class PaymentGatewayPage(BasePage):
    """Strona bramki płatności w trybie sandbox."""

    def __init__(self, page):
        super().__init__(page)
        self.blik_option = page.get_by_test_id("method-blik")
        self.blik_code_input = page.get_by_test_id("blik-code")
        self.confirm_button = page.get_by_role("button", name="Potwierdź płatność")

    def pay_with_blik(self, code):
        self.blik_option.click()
        self.blik_code_input.fill(code)
        self.confirm_button.click()
