from pages.base_page import BasePage


class VisitHistoryPage(BasePage):
    path = "/account/visits"

    def visit(self, reservation_id):
        return self.page.get_by_test_id(f"visit-{reservation_id}")
