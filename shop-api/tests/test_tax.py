import pytest

from shop.tax import calculate_tax


def test_tax_india():
    assert calculate_tax(100.0, "IN") == 18.0


def test_tax_us():
    assert calculate_tax(100.0, "US") == 8.0


def test_unknown_region_raises():
    with pytest.raises(ValueError):
        calculate_tax(100.0, "UK")
