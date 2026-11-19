import re

from pages.base_page import BasePage

URL_PATTERN = re.compile(r"/reservations/(\d+)/confirmation")


class ConfirmationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.status = page.get_by_test_id("reservation-status")

    def reservation_id(self):
        self.page.wait_for_url(URL_PATTERN)
        return int(URL_PATTERN.search(self.page.url).group(1))
