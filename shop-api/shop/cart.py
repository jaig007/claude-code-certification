GIFT_WRAP_FEE = 49


def _check_gift_wrap(flag):
    if not isinstance(flag, bool):
        raise ValueError("CALC-ERROR: gift_wrap must be True or False")


class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, sku, price, qty=1, gift_wrap=False):
        if qty <= 0:
            raise ValueError("qty must be positive")
        _check_gift_wrap(gift_wrap)
        if sku in self.items:
            self.items[sku]["qty"] += qty
            # Re-adding with gift_wrap=True turns wrap on for the whole line;
            # gift_wrap=False never turns it off (use set_gift_wrap).
            if gift_wrap:
                self.items[sku]["gift_wrap"] = True
        else:
            self.items[sku] = {"price": price, "qty": qty, "gift_wrap": gift_wrap}

    def set_gift_wrap(self, sku, flag):
        if sku not in self.items:
            raise KeyError(sku)
        _check_gift_wrap(flag)
        self.items[sku]["gift_wrap"] = flag

    def gift_wrap_total(self):
        return sum(
            GIFT_WRAP_FEE * i["qty"] for i in self.items.values() if i.get("gift_wrap")
        )

    def remove_item(self, sku, qty=None):
        if sku not in self.items:
            raise KeyError(sku)
        if qty is None or qty >= self.items[sku]["qty"]:
            del self.items[sku]
        else:
            self.items[sku]["qty"] -= qty

    def subtotal(self):
        base = sum(i["price"] * i["qty"] for i in self.items.values())
        return round(base + self.gift_wrap_total(), 2)
