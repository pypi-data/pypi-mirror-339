"""
Helper functions for Payler SDK.
"""

from decimal import Decimal


def format_amount_for_payler(amount: Decimal) -> int:
    """
    Format amount for Payler API (multiplies by 100 and rounds).

    In Payler API, amounts must be passed in the smallest units of currency
    (cents, pennies, etc.), so we multiply by 100 and round.

    Args:
        amount: Amount in the main units of currency (rubles, dollars, etc.)

    Returns:
        int: Amount in the smallest units of currency (cents, pennies)
    """
    return int(round(amount * 100))
