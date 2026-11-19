from concurrent.futures import ThreadPoolExecutor

import pytest

pytestmark = pytest.mark.api


def book(api, booking_data, start):
    return api.create_reservation(
        booking_data["salon_id"],
        booking_data["employee"]["id"],
        booking_data["service"]["id"],
        start,
    )


def free_slots(api, booking_data, day):
    response = api.get_free_slots(
        booking_data["salon_id"],
        booking_data["employee"]["id"],
        booking_data["service"]["id"],
        day,
    )
    assert response.status_code == 200
    return [slot["start"] for slot in response.json()]


@pytest.fixture
def free_slot(api_as, booking_data, booking_date):
    slots = free_slots(api_as("client1"), booking_data, booking_date)
    assert slots, f"Brak wolnych terminów w dniu {booking_date}"
    return slots[0]


def test_create_reservation(api_as, booking_data, booking_date, free_slot):
    api = api_as("client1")

    response = book(api, booking_data, free_slot)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "zablokowana"
    assert body["start"] == free_slot
    assert body["serviceId"] == booking_data["service"]["id"]
    assert body["price"] == booking_data["service"]["price"]
    assert free_slot not in free_slots(api, booking_data, booking_date)


def test_slot_taken_by_another_client_returns_conflict(api_as, booking_data, free_slot):
    first = book(api_as("client1"), booking_data, free_slot)
    second = book(api_as("client2"), booking_data, free_slot)

    assert first.status_code == 201
    assert second.status_code == 409


def test_parallel_requests_for_same_slot(api_as, booking_data, free_slot):
    clients = [api_as("client1"), api_as("client2")]

    with ThreadPoolExecutor(max_workers=len(clients)) as pool:
        responses = list(pool.map(lambda client: book(client, booking_data, free_slot), clients))

    statuses = sorted(r.status_code for r in responses)
    assert statuses == [201, 409]
