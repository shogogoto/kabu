"""外部情報源."""

from pathlib import Path

import pandas as pd
import yfinance as yf

from kabu.features.undervalued_search.domain import EPS
from kabu.shared.source.jquants import get_statements_cached


def get_eps_from_yfinance(code: str) -> list[EPS]:
    """yfinanceのEPSを取得する."""
    ticker = yf.Ticker(f"{code}.T")
    eps_series = ticker.quarterly_financials.loc["Basic EPS"]
    return [EPS(report_date=k.date(), value=v) for k, v in eps_series.items()]


def get_eps_from_csv(path: Path) -> list[EPS]:
    """決算発表日,EPSの列のcsvからEPSを取得する.

    CSVにヘッダーがないことを想定し、1列目を決算発表日, 2列目をEPSとして読み込む.
    """
    df = pd.read_csv(path, header=None, names=["決算発表日", "EPS"])
    return [
        EPS(report_date=row["決算発表日"], value=row["EPS"]) for _, row in df.iterrows()
    ]


def get_eps_from_jquants(
    code: str,
    start_dt="20230613",
    end_dt="20250613",
) -> list[EPS]:
    """jquantsのEPSを取得する."""
    if len(code) == 4:
        code = f"{code}0"

    df = get_statements_cached(code, start_dt, end_dt)
    return [
        EPS(report_date=row["DisclosedDate"], value=row["EarningsPerShare"])
        for _, row in df.iterrows()
    ]
