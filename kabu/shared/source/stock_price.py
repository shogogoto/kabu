"""株価ソース."""

from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf

from kabu.shared.settings import Settings


def get_stock_price(
    code: str,
    start_date: str | date,
    end_date: str | date,
) -> pd.DataFrame:
    """ある検索期間内の特定の銘柄コードの株価を取得する.

    キャッシュ対応.
    """
    s = Settings()
    fname = f"{code}-{start_date}-{end_date}.csv"
    cache_path = Path.cwd() / f"{s.STOCK_PRICE_CACHE_DIR}/{fname}"
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    def _f():
        if cache_path.exists():
            return pd.read_csv(cache_path, index_col="Date", parse_dates=True)

        ticker = yf.Ticker(f"{code}.T")
        df = ticker.history(start=start_date, end=end_date)

        if not df.empty:
            df.to_csv(cache_path)

        return df

    df = _f()
    # yfinanceから取得したデータはタイムゾーンを持つことがあるため、削除する
    df.index = df.index.tz_localize(None)
    return df

