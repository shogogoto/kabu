"""repo test."""

from kabu.features.undervalued_search.repo import search_undervalued_stock


def test_search_undervalued_stock():
    """割安期間検索."""
    res = search_undervalued_stock(
        code="8473",
        underval_target_rate=0.05,
        end_yyyymmdd="2023-01-01",
        past_months=12,
    )
