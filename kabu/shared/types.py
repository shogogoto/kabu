"""shared for typing."""

from datetime import date, datetime


def date_from_iso_string(value: str | date) -> date:
    """日付文字列(YYYY-MM-DD or ISO 8601)を日付型に変換する."""
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError as e:
            msg = f"Invalid date format for '{value}'"
            raise ValueError(msg) from e
    if isinstance(value, date):
        return value
    msg = f"Unsupported type for date conversion: {type(value)}"
    raise TypeError(msg)
