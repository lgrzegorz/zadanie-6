import pytest
from playwright.sync_api import expect

from pages.booking_summary_page import BookingSummaryPage
from pages.confirmation_page import ConfirmationPage
from pages.payment_gateway_page import PaymentGatewayPage
from pages.salon_page import SalonPage
from pages.visit_history_page import VisitHistoryPage


@pytest.mark.smoke
def test_client_can_book_and_pay_for_visit(logged_in_page, booking_data, booking_date, api_as):
    page = logged_in_page
    service = booking_data["service"]
    employee = booking_data["employee"]

    salon = SalonPage(page, booking_data["salon_id"]).open()
    salon.choose_service(service["name"])
    salon.choose_employee(employee["name"])
    salon.choose_date(booking_date)
    slot_time = salon.choose_first_free_slot()
    salon.book()

    summary = BookingSummaryPage(page)
    expect(summary.service_name).to_have_text(service["name"])
    expect(summary.employee_name).to_have_text(employee["name"])
    expect(summary.slot_time).to_contain_text(slot_time)
    expect(summary.price).to_have_text(service["price_label"])
    summary.pay()

    PaymentGatewayPage(page).pay_with_blik(booking_data["blik_code"])

    confirmation = ConfirmationPage(page)
    reservation_id = confirmation.reservation_id()
    api_as("client1").created_reservations.append(reservation_id)
    expect(confirmation.status).to_have_text("Opłacona")

    visit = VisitHistoryPage(page).open().visit(reservation_id)
    expect(visit).to_contain_text(service["name"])
    expect(visit).to_contain_text(slot_time)
    expect(visit).to_contain_text("Opłacona")
