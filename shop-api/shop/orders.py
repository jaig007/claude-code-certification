from shop import inventory
from shop.pricing import bulk_discount
from shop.tax import calculate_tax


def place_order(cart, region):
    reserved = []
    try:
        for sku, item in cart.items.items():
            inventory.reserve(sku, item["qty"])
            reserved.append((sku, item["qty"]))
    except ValueError:
        for sku, qty in reserved:
            inventory.release(sku, qty)
        raise

    subtotal = round(
        sum(bulk_discount(i["qty"], i["price"]) for i in cart.items.values()), 2
    )
    tax = calculate_tax(subtotal, region)
    return {
        "items": {sku: dict(i) for sku, i in cart.items.items()},
        "subtotal": subtotal,
        "tax": tax,
        "total": round(subtotal + tax, 2),
        "region": region,
    }
