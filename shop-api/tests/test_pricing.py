import pytest

from shop.pricing import apply_discount, bulk_discount


def test_zero_discount_returns_price():
    assert apply_discount(250.0, 0) == 250.0


def test_apply_discount_ten_percent():
    assert apply_discount(200.0, 10) == 180.0


def test_apply_discount_quarter_off():
    assert apply_discount(80.0, 25) == 60.0


def test_invalid_percent_raises():
    with pytest.raises(ValueError):
        apply_discount(100.0, 120)


def test_bulk_discount_below_threshold():
    assert bulk_discount(5, 20.0) == 100.0


def test_bulk_discount_at_threshold():
    assert bulk_discount(10, 20.0) == 180.0
