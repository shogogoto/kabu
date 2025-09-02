"""test."""

from pprint import pp

import pandas as pd
import yfinance as yf


def test_get_info():
    """動作確認用."""
    df = pd.read_csv("data_j.csv")
    # 最初のコードをサンプルとして使用します
    code = df["コード"][0]

    # yfinance用にティッカーコードを整形します (例: 1301 -> 1301.T)
    ticker_code = f"{code}.T"

    ticker = yf.Ticker(ticker_code)

    pp(ticker.info)

    # ticker.info からEPSを取得します
    eps = ticker.info.get("trailingEps", "データなし")

    print(f"コード: {code}")
    print(f"yfinanceティッカー: {ticker_code}")
    print(f"EPS: {eps}")
