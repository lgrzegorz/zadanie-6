from pages.base_page import BasePage


class SalonPage(BasePage):
    def __init__(self, page, salon_id):
        super().__init__(page)
        self.path = f"/salons/{salon_id}"
        self.services = page.get_by_test_id("service-list")
        self.employees = page.get_by_test_id("employee-list")
        self.free_slots = page.get_by_test_id("free-slot")
        self.book_button = page.get_by_role("button", name="Zarezerwuj")

    def choose_service(self, name):
        self.services.get_by_text(name, exact=True).click()

    def choose_employee(self, name):
        self.employees.get_by_text(name, exact=True).click()

    def choose_date(self, day):
        self.page.get_by_test_id(f"calendar-day-{day.isoformat()}").click()

    def choose_first_free_slot(self):
        slot = self.free_slots.first
        slot_time = slot.inner_text().strip()
        slot.click()
        return slot_time

    def book(self):
        self.book_button.click()
