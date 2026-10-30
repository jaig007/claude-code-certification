# Test results: Gift wrapping

## Tests added
New file tests/test_cart_gift_wrap.py (no existing test file edited, no shop/ code edited). 28 test cases (parametrized), covering:
- Fee constant is 49; wrapped qty 2 adds 98; unwrapped adds 0; mixed cart; empty cart is 0.
- set_gift_wrap on and off; missing sku raises KeyError.
- Partial remove reduces fee; full remove and qty-equal remove drop it.
- Re-add with True turns wrap on for whole line; re-add with False does not turn it off.
- Invalid gift_wrap ("yes", None, 1, 0, 1.0, []) raises ValueError starting with "CALC-ERROR:" from add_item and set_gift_wrap; state unchanged after rejection.
- Default add_item behaviour unchanged; existing "qty must be positive" message unchanged.
- Orders: subtotal includes the fee (and is taxed, per the implementer's assumption); no-wrap order unchanged; fee not reduced by bulk discount (wrapped minus unwrapped subtotal is exactly 490 for qty 10).

## Pytest summary line
`5 failed, 41 passed in 0.30s`  (command: python -m pytest -q)

All tests in tests/test_cart_gift_wrap.py pass. All existing test_cart.py and test_tax.py tests pass.

## Failures (all pre-existing, none from gift wrap)
1. tests/test_inventory.py::test_reserve_more_than_available_raises and ::test_stock_never_negative: inventory.reserve never checks stock, so it goes negative (-2) and does not raise ValueError. Bug in shop/inventory.py.
2. tests/test_pricing.py::test_apply_discount_ten_percent (190.0 vs 180.0), ::test_apply_discount_quarter_off (55.0 vs 60.0), ::test_bulk_discount_at_threshold (190.0 vs 180.0): apply_discount does `price - percent` (subtracts the number) instead of `price * (1 - percent/100)`. Bug in shop/pricing.py.

## Notes
- Because of the apply_discount bug, my bulk-discount test compares wrapped vs unwrapped carts instead of hard-coding a discounted amount, so it stays valid once that bug is fixed.
- Pytest printed paths under D:\claude-code-certification\design-pattern\shop-api, so the project dir appears to be reachable via a link or alias. Harmless but worth knowing.
- Open item from the plan still unresolved: whether the wrap fee should be taxed. Currently it is taxed.
- The task text named the file 3-test-report.md in one place and 3-test-results.md in another; I wrote 3-test-results.md.
