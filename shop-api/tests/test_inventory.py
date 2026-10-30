import pytest

from shop import inventory


@pytest.fixture(autouse=True)
def reset_stock():
    inventory.stock.clear()
    yield
    inventory.stock.clear()


def test_reserve_reduces_stock():
    inventory.set_stock("A1", 10)
    assert inventory.reserve("A1", 3) == 7


def test_release_increases_stock():
    inventory.set_stock("A1", 5)
    assert inventory.release("A1", 2) == 7


def test_reserve_more_than_available_raises():
    inventory.set_stock("A1", 2)
    with pytest.raises(ValueError):
        inventory.reserve("A1", 5)


def test_stock_never_negative():
    inventory.set_stock("A1", 1)
    try:
        inventory.reserve("A1", 3)
    except ValueError:
        pass
    assert inventory.stock["A1"] >= 0
