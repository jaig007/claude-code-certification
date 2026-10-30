def apply_discount(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price - percent, 2)


def bulk_discount(qty, price):
    """10% off the line total when buying 10 or more units."""
    total = qty * price
    if qty >= 10:
        return apply_discount(total, 10)
    return round(total, 2)
