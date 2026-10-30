# Plan: Gift wrapping on Cart (Rs 49 per unit)

## Findings
- shop/cart.py: Cart.items = {sku: {"price", "qty"}}. subtotal() = sum(price*qty), rounded to 2.
- shop/orders.py (lines 17-18) computes its OWN subtotal via bulk_discount and ignores Cart.subtotal(). It copies item dicts, so a new key flows through, but wrap fees would be missed there.
- Existing tests in tests/test_cart.py must keep passing unchanged (never edit tests/).

## Files to change
1. shop/cart.py
   - Add module constant GIFT_WRAP_FEE = 49.
   - add_item(sku, price, qty=1, gift_wrap=False): store "gift_wrap" in the item dict.
   - New set_gift_wrap(sku, flag: bool): toggle for an existing item.
   - New helper gift_wrap_total(): sum(49 * qty) for wrapped items.
   - subtotal(): add gift_wrap_total() to the existing sum, then round.
2. shop/orders.py: add the wrap fee to the order subtotal (Cart.gift_wrap_total()). Decision needed: wrap fee is NOT discounted by bulk_discount and is added before tax. Confirm with the requester whether it should be taxed.

## API changes
- add_item gains optional keyword gift_wrap (default False), backward compatible.
- New: Cart.set_gift_wrap(sku, flag), Cart.gift_wrap_total().
- Item dict gains a "gift_wrap" key.

## Edge cases
- Re-adding an existing sku with a different gift_wrap value: decide the rule (suggest: new True turns it on for the whole line; document it). Currently price is also ignored on re-add.
- Per-item flag applies to all units of the line (fee = 49 * qty). Partial remove_item reduces the fee automatically; full removal drops it.
- Non-bool gift_wrap (e.g. "yes", None): reject with ValueError.
- set_gift_wrap on a missing sku: KeyError(sku), same as remove_item.
- Error messages for NEW errors must start with "CALC-ERROR:" (e.g. "CALC-ERROR: gift_wrap must be True or False"). Do not change existing messages, since tests may match them.
- Float rounding: fee is an int, so keep the final round(..., 2).
- Empty cart: subtotal stays 0.

## Tests to add (new file tests/test_cart_gift_wrap.py; do not edit existing test files)
- Wrapped item qty 2 adds 98 to subtotal; unwrapped adds 0.
- Mixed cart (one wrapped, one not).
- set_gift_wrap toggles on and off; missing sku raises KeyError.
- Partial and full remove updates the fee.
- Re-add with gift_wrap behavior.
- Invalid gift_wrap raises ValueError whose message starts with "CALC-ERROR:".
- Default add_item(...) behavior unchanged.
- orders: order subtotal includes the wrap fee, and bulk discount does not reduce it.

## Verify
python -m pytest -q
