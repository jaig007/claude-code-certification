import pytest

from shop.cart import Cart


def test_add_item_and_subtotal():
    cart = Cart()
    cart.add_item("A1", 10.0, 2)
    cart.add_item("B2", 5.5)
    assert cart.subtotal() == 25.5


def test_add_same_item_accumulates_qty():
    cart = Cart()
    cart.add_item("A1", 10.0, 1)
    cart.add_item("A1", 10.0, 3)
    assert cart.items["A1"]["qty"] == 4


def test_remove_item_partial_and_full():
    cart = Cart()
    cart.add_item("A1", 10.0, 3)
    cart.remove_item("A1", 1)
    assert cart.subtotal() == 20.0
    cart.remove_item("A1")
    assert cart.subtotal() == 0


def test_remove_missing_item_raises():
    with pytest.raises(KeyError):
        Cart().remove_item("nope")


def test_add_non_positive_qty_raises():
    with pytest.raises(ValueError):
        Cart().add_item("A1", 10.0, 0)
