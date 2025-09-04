"""kabu."""

import operator

import jquantsapi
import pandas as pd
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData

from kabu.settings import Settings


def get_stock_price(code: str, start_date: str, end_date: str):
    """ある検索期間内の特定の銘柄コードの株価を取得する."""
    ticker = yf.Ticker(f"{code}.T")
    return ticker.history(start=start_date, end=end_date)


def get_eps(code: str, start_date: str, end_date: str):
    """ある検索期間内の特定の銘柄コードのEPSを取得する.

    yfinanceの仕様により、直近4四半期分のデータのみ取得可能です.

    Args:
        code (str): 銘柄コード.
        start_date (str): 検索開始日 (YYYY-MM-DD).
        end_date (str): 検索終了日 (YYYY-MM-DD).

    Returns:
        list[tuple[pd.Timestamp, float]]: 四半期の日付とEPSのペアのリスト.

    """
    ticker = yf.Ticker(f"{code}.T")

    # 四半期ごとの財務諸表を取得
    quarterly_financials = ticker.quarterly_financials

    print(f"{quarterly_financials}")

    if quarterly_financials.empty or "Basic EPS" not in quarterly_financials.index:
        return []

    # EPSのデータを抽出
    eps_data = quarterly_financials.loc["Basic EPS"]

    # 不要な列を削除し、日付とEPSのペアに変換
    eps_data = eps_data.dropna()
    eps_list = sorted(eps_data.items(), key=operator.itemgetter(0))

    # start_dateとend_dateをdatetimeオブジェクトに変換
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # 期間でフィルタリング
    return [(date, eps) for date, eps in eps_list if start <= date <= end]


def get_eps_by_alpha_vantage(
    code: str,
    start_date: str | None = None,
    end_date: str | None = None,
):
    """Alpha Vantageを使用して、特定の銘柄コードの長期的な四半期EPSを取得する."""
    # (This function is currently not fully implemented)
    symbol = f"{code}.TO"
    api_key = Settings().ALPHA_VANTAGE_API_KEY
    fd = FundamentalData(key=api_key, output_format="pandas")
    # res = fd.get_earnings_quarterly(symbol=symbol)
    res = fd.get_earnings_annual(symbol="IBM")
    print(f"{res}")


def get_eps_by_jquants(
    code: str,
    start_date: str,
) -> pd.DataFrame:
    """J-Quants APIを使用して、特定の銘柄コードの長期的なEPSを取得する.

    Args:
        code (str): 銘柄コード.
        start_date (str | None, optional): 検索開始日 (YYYY-MM-DD). Defaults to None.
        end_date (str | None, optional): 検索終了日 (YYYY-MM-DD). Defaults to None.

    Returns:
        list[tuple[pd.Timestamp, float]]: 開示日とEPSのペアのリスト.

    """
    try:
        settings = Settings()
        # Settingsクラスに実装されたメソッドからリフレッシュトークンを取得
        # メソッド名が違う場合は、下の行を修正してください
        token_dict = settings.get_jquants_token()
        refresh_token = token_dict["refreshToken"]

        print(refresh_token)
        client = jquantsapi.Client(refresh_token=refresh_token)

        # "Basic earnings (loss) per share (IFRS)"
        # return client.get_fs_details_range()
        # return client.get_fins_statements(code=code, date_yyyymmdd=start_date)
        # df = client.get_fs_details_range(code=code, date_yyyymmdd=start_date)
        # df = client.get_statements(code=code, start_date=start_date, end_date=end_date)

        # 必要な列を抽出
        # eps_data = df[["DisclosedDate", "EarningsPerShare"]].copy()

        # 'EarningsPerShare'がNoneや0の行を削除
        eps_data = eps_data.dropna(subset=["EarningsPerShare"])
        eps_data = eps_data[eps_data["EarningsPerShare"] != 0]

        if eps_data.empty:
            return []

        # 日付とEPSのリストを作成
        eps_list = [
            (
                pd.to_datetime(row["DisclosedDate"]),
                row["EarningsPerShare"],
            )
            for _, row in eps_data.iterrows()
        ]

        # 日付でソート
        eps_list.sort(key=operator.itemgetter(0))

        return eps_list

    except Exception as e:
        print(f"J-Quants APIからのデータ取得中にエラーが発生しました: {e}")
        return []


def search_undervalued():
    """割安タイミングを返す.

    割安: 理論株価 > 実際の株価

    """

