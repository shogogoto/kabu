import numpy as np
import pandas as pd
import pytest

from kabu.features.undervalued_search.domain import EPS, resample_eps_to_daily

# Set plotly as the default backend for pandas plotting
pd.options.plotting.backend = "plotly"


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
    v2 = 50
    v3 = 80
    v4 = 90

    eps_ls = [
        EPS(report_date="2023-12-31", value=v1),
        EPS(report_date="2024-03-31", value=v2),
        EPS(report_date="2024-06-30", value=v3),
        EPS(report_date="2024-09-30", value=v4),
    ]

    # underval_rate = (理論株価 - 実株価) / 理論株価

    # 実株価と理論株価と割安率をそれぞれプロットしたい


def test_find_catchup_dates():
    """追いつき日を検出する."""
