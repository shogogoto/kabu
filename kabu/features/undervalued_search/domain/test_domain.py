import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from kabu.features.undervalued_search.domain import EPS, resample_eps_to_daily


def test_resample():
    """EPSをdailyに引き伸ばす."""
    v1 = 81.82
    v2 = np.nan
    v3 = 70.79

    eps_ls = [
        EPS(report_date="2023-12-31", value=v1),
        EPS(report_date="2024-03-31", value=v2),
        EPS(report_date="2024-06-30", value=v3),
    ]

    dailies = resample_eps_to_daily(eps_ls, "2025-01-01")
    with pytest.raises(KeyError):
        dailies["2023-12-30"]
    assert dailies["2023-12-31"] == v1
    assert dailies["2024-01-01"] == v1

    assert dailies["2024-03-30"] == v1
    assert np.isnan(dailies["2024-03-31"])
    assert np.isnan(dailies["2024-04-01"])

    assert np.isnan(dailies["2024-06-29"])
    assert dailies["2024-06-30"] == v3
    assert dailies["2024-07-01"] == v3

    assert dailies["2024-07-01"] == v3

    assert dailies["2024-12-31"] == v3
    assert dailies["2025-01-01"] == v3
    with pytest.raises(KeyError):
        dailies["2025-01-02"]


"""割安期間を検出する.

まず、 epsのdailyの値を10倍したものを理論株価(theoretical_stock_price)とする
実株価を取得して以下のように割安比率(underval_rate)を計算する

underval_rate = (理論株価 - 実株価) / 理論株価

これがunderval_target_rateよりも高い日を割安期間として取得する
割安期間のリストが得られる

また、underval_target_rateが 正から負へ変わるときを 追いつき日(CatchUpDate)一覧として取得する

これには２つのシナリオがある
1. 理論株価より低かった実株価が上がって理論株価に追いついた
2. 決算発表日でEPSが更新されるのに伴って理論株価が下がって


"""


def test_find_undervalued_terms():
    """割安期間を検出する."""
    # 2024-01-01 ~ 2024-12-31 を検索期間とする
    # 実株価のテストケース を sinカーブで作りたい

    v1 = 100.0
    v2 = 50.0
    v3 = 90.0
    v4 = 70.0

    eps_ls = [
        EPS(report_date="2023-12-31", value=v1),
        EPS(report_date="2024-03-31", value=v2),
        EPS(report_date="2024-06-30", value=v3),
        EPS(report_date="2024-09-30", value=v4),
    ]
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # 実株価のテストケース sinカーブ
    price_center = 800  # 中心
    amplitude = 400  # 振幅
    days = len(dates)  # 2024 is a leap year 閏年
    real_price = price_center + amplitude * np.sin(np.linspace(0, 4 * np.pi, days))
    real_price_sr = pd.Series(real_price, index=dates, name="real_price")

    theoretical_price_sr = resample_eps_to_daily(eps_ls, end_date) * 10
    theoretical_price_sr.name = "theoretical_price"

    underval_rate_sr = (theoretical_price_sr - real_price_sr) / theoretical_price_sr
    underval_rate_sr.name = "underval_rate"

    df = pd.concat([real_price_sr, theoretical_price_sr], axis=1)  # DataFrameにまとめる

    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax, title="Undervalued Search", grid=True)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    fig.savefig("threo_real_price.png")
    plt.close(fig)

    # 割安期間を検出するロジック
    # 本来は domain.find_undervalued_terms に実装されるべき
    # underval_target_rate = 0.2
    # is_undervalued = df["underval_rate"] > underval_target_rate

    # 連続した True のブロックを見つける
    # undervalued_terms = []
    # in_term = False
    # start_of_term = None
    # for date, is_under in is_undervalued.items():
    #     if is_under and not in_term:
    #         in_term = True
    #         start_of_term = date
    #     elif not is_under and in_term:
    #         in_term = False
    #         end_of_term = date - pd.Timedelta(days=1)
    #         undervalued_terms.append((start_of_term, end_of_term))

    # if in_term:
    #     undervalued_terms.append((start_of_term, is_undervalued.index[-1]))
    #
    # # アサーション
    # assert len(undervalued_terms) == 2
    # assert undervalued_terms[0][0] == pd.Timestamp("2024-07-15")
    # assert undervalued_terms[0][1] == pd.Timestamp("2024-09-29")
    # assert undervalued_terms[1][0] == pd.Timestamp("2024-10-07")
    # assert undervalued_terms[1][1] == pd.Timestamp("2024-12-25")


def test_find_catchup_dates():
    """追いつき日を検出する."""

