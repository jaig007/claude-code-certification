import pytest

from shop import inventory
from shop.cart import GIFT_WRAP_FEE, Cart
from shop.orders import place_order


@pytest.fixture(autouse=True)
def reset_stock():
    inventory.stock.clear()
    yield
    inventory.stock.clear()


def test_fee_constant():
    assert GIFT_WRAP_FEE == 49


def test_wrapped_item_adds_fee_per_unit():
    c = Cart()
    c.add_item("A", 100, qty=2, gift_wrap=True)
    assert c.gift_wrap_total() == 98
    assert c.subtotal() == 200 + 98


def test_unwrapped_item_adds_no_fee():
    c = Cart()
    c.add_item("A", 100, qty=2)
    assert c.gift_wrap_total() == 0
    assert c.subtotal() == 200


def test_mixed_cart():
    c = Cart()
    c.add_item("A", 100, qty=2, gift_wrap=True)
    c.add_item("B", 10, qty=3)
    assert c.gift_wrap_total() == 98
    assert c.subtotal() == 200 + 30 + 98


def test_empty_cart_subtotal_zero():
    c = Cart()
    assert c.subtotal() == 0
    assert c.gift_wrap_total() == 0


def test_set_gift_wrap_on_and_off():
    c = Cart()
    c.add_item("A", 100, qty=3)
    c.set_gift_wrap("A", True)
    assert c.gift_wrap_total() == 147
    assert c.subtotal() == 300 + 147
    c.set_gift_wrap("A", False)
    assert c.gift_wrap_total() == 0
    assert c.subtotal() == 300


def test_set_gift_wrap_missing_sku_raises_keyerror():
    c = Cart()
    with pytest.raises(KeyError):
        c.set_gift_wrap("NOPE", True)


def test_partial_remove_reduces_fee():
    c = Cart()
    c.add_item("A", 100, qty=3, gift_wrap=True)
    c.remove_item("A", qty=1)
    assert c.gift_wrap_total() == 98
    assert c.subtotal() == 200 + 98


def test_full_remove_drops_fee():
    c = Cart()
    c.add_item("A", 100, qty=3, gift_wrap=True)
    c.remove_item("A")
    assert c.gift_wrap_total() == 0
    assert c.subtotal() == 0


def test_remove_qty_equal_to_line_drops_fee():
    c = Cart()
    c.add_item("A", 100, qty=2, gift_wrap=True)
    c.remove_item("A", qty=2)
    assert c.gift_wrap_total() == 0


def test_readd_with_true_turns_wrap_on_for_whole_line():
    c = Cart()
    c.add_item("A", 100, qty=2)
    c.add_item("A", 100, qty=1, gift_wrap=True)
    assert c.items["A"]["qty"] == 3
    assert c.items["A"]["gift_wrap"] is True
    assert c.gift_wrap_total() == 147


def test_readd_with_false_does_not_turn_wrap_off():
    c = Cart()
    c.add_item("A", 100, qty=2, gift_wrap=True)
    c.add_item("A", 100, qty=1, gift_wrap=False)
    assert c.items["A"]["gift_wrap"] is True
    assert c.gift_wrap_total() == 147


@pytest.mark.parametrize("bad", ["yes", None, 1, 0, 1.0, []])
def test_add_item_invalid_gift_wrap(bad):
    c = Cart()
    with pytest.raises(ValueError) as exc:
        c.add_item("A", 100, gift_wrap=bad)
    assert str(exc.value).startswith("CALC-ERROR:")
    assert "A" not in c.items


@pytest.mark.parametrize("bad", ["yes", None, 1, 0])
def test_set_gift_wrap_invalid_flag(bad):
    c = Cart()
    c.add_item("A", 100)
    with pytest.raises(ValueError) as exc:
        c.set_gift_wrap("A", bad)
    assert str(exc.value).startswith("CALC-ERROR:")
    assert c.items["A"]["gift_wrap"] is False


def test_invalid_gift_wrap_on_readd_does_not_change_qty():
    c = Cart()
    c.add_item("A", 100, qty=1)
    with pytest.raises(ValueError):
        c.add_item("A", 100, qty=5, gift_wrap="yes")
    assert c.items["A"]["qty"] == 1


def test_default_add_item_unchanged():
    c = Cart()
    c.add_item("A", 25.5, qty=2)
    assert c.items["A"]["price"] == 25.5
    assert c.items["A"]["qty"] == 2
    assert c.items["A"]["gift_wrap"] is False
    assert c.subtotal() == 51.0


def test_existing_qty_validation_message_unchanged():
    c = Cart()
    with pytest.raises(ValueError, match="qty must be positive"):
        c.add_item("A", 10, qty=0)


def test_order_subtotal_includes_fee():
    inventory.set_stock("A", 10)
    c = Cart()
    c.add_item("A", 100, qty=2, gift_wrap=True)
    order = place_order(c, "IN")
    assert order["subtotal"] == 200 + 98
    assert order["tax"] == round(298 * 0.18, 2)
    assert order["total"] == round(298 + order["tax"], 2)
    assert order["items"]["A"]["gift_wrap"] is True


def test_order_without_wrap_unchanged():
    inventory.set_stock("A", 10)
    c = Cart()
    c.add_item("A", 100, qty=2)
    order = place_order(c, "US")
    assert order["subtotal"] == 200


def test_bulk_discount_does_not_reduce_fee():
    # Compare the same cart with and without wrap: the difference must be
    # exactly the full fee, whatever the bulk discount does to the items.
    inventory.set_stock("A", 100)
    plain = Cart()
    plain.add_item("A", 100, qty=10)
    wrapped = Cart()
    wrapped.add_item("A", 100, qty=10, gift_wrap=True)
    base = place_order(plain, "US")["subtotal"]
    with_fee = place_order(wrapped, "US")["subtotal"]
    assert with_fee - base == pytest.approx(490)
