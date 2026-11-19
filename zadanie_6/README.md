# zadanie_6

Testy automatyczne aplikacji do rezerwacji wizyt (zadanie rekrutacyjne, zadanie 6).

Aplikacja nie istnieje, więc adresy, endpointy, selektory i dane testowe są umowne. Po podstawieniu prawdziwych wartości testy powinny dać się uruchomić bez zmian w strukturze.

## Technologie

- Python 3.12
- pytest
- Playwright (pytest-playwright) do testów UI
- requests do testów API

## Struktura projektu

```
zadanie_6/
├── api_client/
│   └── booking_api.py        # klient API: logowanie, wolne terminy, rezerwacje
├── data/
│   ├── users.json            # konto testowe (hasło jest w .env)
│   └── booking.json          # salon, pracownik, usługa, kod BLIK z sandboxa
├── pages/                    # Page Objecty
│   ├── base_page.py
│   ├── header.py
│   ├── login_page.py
│   ├── salon_page.py
│   ├── booking_summary_page.py
│   ├── payment_gateway_page.py
│   ├── confirmation_page.py
│   └── visit_history_page.py
├── tests/
│   ├── ui/
│   │   ├── test_login.py
│   │   └── test_booking.py
│   └── api/
│       └── test_reservations_api.py
├── conftest.py               # fixtures: dane testowe, logowanie, klient API, sprzątanie
├── config.py                 # adres API i hasło z pliku .env lub zmiennych środowiskowych
├── .env.example              # wzór pliku .env
├── pytest.ini
└── requirements.txt
```

## Testy

- `tests/ui/test_login.py` - logowanie poprawnymi danymi.
- `tests/ui/test_booking.py` - rezerwacja wizyty z płatnością BLIK w sandboxie i sprawdzenie wizyty w historii.
- `tests/api/test_reservations_api.py` - utworzenie rezerwacji przez endpoint i sprawdzenie, że termin zniknął z wolnych.


## Uruchomienie

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

Adres API i hasło do kont testowych są w pliku `.env`, którego nie ma w repozytorium. Trzeba go utworzyć na podstawie `.env.example`:

```bash
cp .env.example .env             # Windows: copy .env.example .env
```

i uzupełnić `TEST_PASSWORD`. Bez hasła testy się nie uruchomią. W CI te same wartości są ustawione jako sekrety repozytorium.

Domyślny adres aplikacji jest w `pytest.ini` (`base_url`). Można go nadpisać parametrem `--base-url`.

```bash
pytest                              # wszystkie testy
pytest -m smoke                     # tylko smoke
pytest -m api                       # tylko API
pytest tests/ui --headed            # UI z widoczną przeglądarką
pytest --browser webkit             # inna przeglądarka
pytest --base-url https://inny-adres.example
```

Przy błędzie zapisuje się zrzut ekranu i trace Playwrighta w katalogu `test-results/`. Trace można otworzyć poleceniem `playwright show-trace test-results/.../trace.zip`.

## Założenia

- Elementy na stronie mają atrybuty `data-testid`, a przyciski są wyszukiwane po roli i tekście.
- API używa tokenu (Bearer) zwracanego przez `POST /auth/login`.
- Na STAGING jest salon testowy z pracownikiem i usługą z `booking.json`, a bramka płatności działa w trybie sandbox.
- Każdy test tworzy swoje rezerwacje na termin tydzień do przodu i anuluje je po zakończeniu (fixture `api_as`), żeby testy nie zostawiały danych i nie blokowały sobie terminów.

## CI

W `.github/workflows/tests.yml` jest pipeline dla GitHub Actions. Uruchamia testy przy każdym pushu i pull requeście, a przy błędzie zapisuje wyniki jako artefakt. Adresy i hasło są w sekretach repozytorium.
