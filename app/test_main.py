import datetime

import pytest

from app.main import outdated_products


@pytest.fixture
def today(monkeypatch: pytest.MonkeyPatch) -> datetime.date:
    current_date = datetime.date(2022, 2, 2)

    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return current_date

    monkeypatch.setattr(datetime, "date", MockDate)
    return current_date


def test_returns_only_products_expired_before_today(
    today: datetime.date,
) -> None:
    products = [
        {
            "name": "salmon",
            "expiration_date": today + datetime.timedelta(days=8),
            "price": 600,
        },
        {
            "name": "chicken",
            "expiration_date": today + datetime.timedelta(days=3),
            "price": 120,
        },
        {
            "name": "duck",
            "expiration_date": today - datetime.timedelta(days=1),
            "price": 160,
        },
    ]

    assert outdated_products(products) == ["duck"]


def test_product_expiring_today_is_not_outdated(today: datetime.date) -> None:
    products = [{"name": "milk", "expiration_date": today, "price": 50}]

    assert outdated_products(products) == []


def test_products_expired_yesterday_are_outdated(
    today: datetime.date,
) -> None:
    products = [{
        "name": "bread",
        "expiration_date": today - datetime.timedelta(days=1),
        "price": 30,
    }]

    assert outdated_products(products) == ["bread"]


def test_empty_products_returns_empty_list() -> None:
    assert outdated_products([]) == []


def test_preserves_input_order_and_duplicate_names(
    today: datetime.date,
) -> None:
    products = [
        {
            "name": "milk",
            "expiration_date": today - datetime.timedelta(days=3),
            "price": 50,
        },
        {
            "name": "cheese",
            "expiration_date": today + datetime.timedelta(days=2),
            "price": 80,
        },
        {
            "name": "milk",
            "expiration_date": today - datetime.timedelta(days=1),
            "price": 55,
        },
    ]

    assert outdated_products(products) == ["milk", "milk"]
