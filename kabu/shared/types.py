"""shared for typing."""

from datetime import UTC, date, datetime


def date_from_iso_string(value: str | date) -> date:
    """日付文字列(YYYY-MM-DD)を日付型に変換する."""
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC).date()
        except ValueError:
            msg = f"''{value}'' is not a valid date in YYYY-MM-DD format."
            raise ValueError(msg) from None
    if isinstance(value, date):
        return value
    msg = f"Unsupported type for date conversion: {type(value)}"
    raise TypeError(msg)
