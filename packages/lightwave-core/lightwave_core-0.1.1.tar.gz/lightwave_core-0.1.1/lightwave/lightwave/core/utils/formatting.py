"""Common formatting utilities."""

from datetime import datetime


def format_date(
    date_obj: datetime | str | None,
    format_str: str = "%Y-%m-%d",
) -> str | None:
    """Format a date object or ISO date string to a specific format.

    Args:
        date_obj: A datetime object, ISO date string, or None
        format_str: The desired output format string

    Returns:
        A formatted date string or None if input is None
    """
    if date_obj is None:
        return None

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace("Z", "+00:00"))
        except ValueError:
            return None

    return date_obj.strftime(format_str)


def format_currency(
    amount: float | int | None,
    currency: str = "USD",
    locale: str = "en_US",
) -> str | None:
    """Format a numeric amount as currency.

    Args:
        amount: The amount to format
        currency: Three-letter currency code
        locale: Locale string for formatting

    Returns:
        A formatted currency string or None if input is None
    """
    if amount is None:
        return None

    # Simple implementation - in a real project you might use babel or other libraries
    if locale.startswith("en"):
        return f"${amount:,.2f} {currency}" if currency != "USD" else f"${amount:,.2f}"

    # Add more locale handling as needed
    return f"{amount:,.2f} {currency}"
