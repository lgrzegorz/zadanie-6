import pytest

pytestmark = pytest.mark.api


def free_slots(api, booking_data, day):
    response = api.get_free_slots(
        booking_data["salon_id"],
        booking_data["employee"]["id"],
        booking_data["service"]["id"],
        day,
    )
    assert response.status_code == 200
    return [slot["start"] for slot in response.json()]


def test_create_reservation(api_as, booking_data, booking_date):
    api = api_as("client1")
    slots = free_slots(api, booking_data, booking_date)
    assert slots, f"Brak wolnych terminów w dniu {booking_date}"
    start = slots[0]

    response = api.create_reservation(
        booking_data["salon_id"],
        booking_data["employee"]["id"],
        booking_data["service"]["id"],
        start,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "zablokowana"
    assert body["start"] == start
    assert body["serviceId"] == booking_data["service"]["id"]
    assert body["price"] == booking_data["service"]["price"]
    assert start not in free_slots(api, booking_data, booking_date)
