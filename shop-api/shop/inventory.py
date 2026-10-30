stock = {}


def set_stock(sku, qty):
    stock[sku] = qty


def reserve(sku, qty):
    if qty <= 0:
        raise ValueError("qty must be positive")
    stock[sku] = stock.get(sku, 0) - qty
    return stock[sku]


def release(sku, qty):
    if qty <= 0:
        raise ValueError("qty must be positive")
    stock[sku] = stock.get(sku, 0) + qty
    return stock[sku]
