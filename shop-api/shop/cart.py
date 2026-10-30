class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, sku, price, qty=1):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if sku in self.items:
            self.items[sku]["qty"] += qty
        else:
            self.items[sku] = {"price": price, "qty": qty}

    def remove_item(self, sku, qty=None):
        if sku not in self.items:
            raise KeyError(sku)
        if qty is None or qty >= self.items[sku]["qty"]:
            del self.items[sku]
        else:
            self.items[sku]["qty"] -= qty

    def subtotal(self):
        return round(sum(i["price"] * i["qty"] for i in self.items.values()), 2)
