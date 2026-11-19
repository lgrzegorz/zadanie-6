from pages.base_page import BasePage


class BookingSummaryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.service_name = page.get_by_test_id("summary-service")
        self.employee_name = page.get_by_test_id("summary-employee")
        self.slot_time = page.get_by_test_id("summary-time")
        self.price = page.get_by_test_id("summary-price")
        self.pay_button = page.get_by_role("button", name="Zapłać")

    def pay(self):
        self.pay_button.click()
