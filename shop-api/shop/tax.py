TAX_RATES = {"IN": 0.18, "US": 0.08}


def calculate_tax(amount, region):
    if region not in TAX_RATES:
        raise ValueError(f"unsupported region: {region}")
    return round(amount * TAX_RATES[region], 2)
