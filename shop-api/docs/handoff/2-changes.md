# Changes: Gift wrapping (Rs 49 per unit)

## shop/cart.py
- Added constant `GIFT_WRAP_FEE = 49`.
- Added helper `_check_gift_wrap(flag)`: raises `ValueError("CALC-ERROR: gift_wrap must be True or False")` for non-bool values.
- `Cart.add_item(sku, price, qty=1, gift_wrap=False)`: validates `gift_wrap`, stores `"gift_wrap"` in the item dict. Re-adding an existing sku with `gift_wrap=True` turns wrap on for the whole line; `False` never turns it off.
- New `Cart.set_gift_wrap(sku, flag)`: raises `KeyError(sku)` if missing, validates flag, sets it.
- New `Cart.gift_wrap_total()`: sum of 49 * qty for wrapped items.
- `Cart.subtotal()`: now adds `gift_wrap_total()` before rounding to 2.

## shop/orders.py
- `place_order`: order subtotal now = discounted item sum + `cart.gift_wrap_total()` (fee not discounted, added before tax). Tax logic untouched.

## Deviations from the plan
- None in behavior. The plan's open question (taxing the wrap fee) was not resolved; I followed the stated assumption (fee goes in before tax, so it is taxed as part of subtotal).
- The plan's "Tests to add" (tests/test_cart_gift_wrap.py) was not implemented: the task covered only cart.py and orders.py.
- I could not run `python -m pytest -q` (no shell available), so the code is not test-verified. I only checked that tests/test_cart.py makes no exact-dict comparisons on items.
