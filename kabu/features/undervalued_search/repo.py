"""repo."""

import yfinance as yf

from .domain import EPS


def get_eps_from_yfinance(code: str) -> list[EPS]:
    """yfinanceのEPSを取得する."""
    ticker = yf.Ticker(f"{code}.T")
    eps_series = ticker.quarterly_financials.loc["Basic EPS"]
    return [EPS(report_date=k.date(), value=v) for k, v in eps_series.items()]
