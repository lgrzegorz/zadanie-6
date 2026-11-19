import requests


class BookingApi:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.created_reservations = []

    def _url(self, path):
        return f"{self.base_url}{path}"

    def login(self, email, password):
        response = self.session.post(
            self._url("/auth/login"),
            json={"email": email, "password": password},
            timeout=10,
        )
        response.raise_for_status()
        self.session.headers["Authorization"] = f"Bearer {response.json()['token']}"

    def get_free_slots(self, salon_id, employee_id, service_id, day):
        return self.session.get(
            self._url(f"/salons/{salon_id}/slots"),
            params={"employeeId": employee_id, "serviceId": service_id, "date": day.isoformat()},
            timeout=10,
        )

    def create_reservation(self, salon_id, employee_id, service_id, start):
        response = self.session.post(
            self._url("/reservations"),
            json={
                "salonId": salon_id,
                "employeeId": employee_id,
                "serviceId": service_id,
                "start": start,
            },
            timeout=10,
        )
        if response.status_code == 201:
            self.created_reservations.append(response.json()["id"])
        return response

    def get_reservation(self, reservation_id):
        return self.session.get(self._url(f"/reservations/{reservation_id}"), timeout=10)

    def cancel_reservation(self, reservation_id):
        return self.session.post(self._url(f"/reservations/{reservation_id}/cancel"), timeout=10)

    def cancel_created_reservations(self):
        for reservation_id in self.created_reservations:
            self.cancel_reservation(reservation_id)
        self.created_reservations.clear()
