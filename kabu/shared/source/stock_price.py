"""株価ソース."""

import yfinance as yf


def get_stock_price(code: str, start_date: str, end_date: str):
    """ある検索期間内の特定の銘柄コードの株価を取得する."""
    ticker = yf.Ticker(f"{code}.T")
    return ticker.history(start=start_date, end=end_date)
