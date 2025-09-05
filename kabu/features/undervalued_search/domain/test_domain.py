"""domain test."""

from datetime import date

import numpy as np
import pandas as pd
import pytest
from pandas.core.common import flatten

from kabu.features.undervalued_search.domain import (
    find_latest_catch_up_date,
    find_undervalued_terms,
    resample_eps_to_daily,
    to_theorical_price_and_rate,
)
from kabu.features.undervalued_search.domain.model import EPS


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


def mk_real_price_sr(dates: list[date]) -> pd.Series:
    """実株価のテストケース sinカーブ."""
    price_center = 800  # 中心
    amplitude = 400  # 振幅
    days = len(dates)  # 2024 is a leap year 閏年
    real_price = price_center + amplitude * np.sin(np.linspace(0, 4 * np.pi, days))
    return pd.Series(real_price, index=dates, name="real_price")


def mk_eps_ls():
    """テストケース作成."""
    v1 = 100.0
    v2 = 50.0
    v3 = 90.0
    v4 = 70.0

    return [
        EPS(report_date="2023-12-31", value=v1),
        EPS(report_date="2024-03-31", value=v2),
        EPS(report_date="2024-06-30", value=v3),
        EPS(report_date="2024-09-30", value=v4),
    ]


def test_find_undervalued_terms_and_catchup_date():
    """割安期間とその直後の追いつき日を検出する."""
    # 2024-01-01 ~ 2024-12-31 を検索期間とする
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    real_price_sr = mk_real_price_sr(dates)
    theoretical_price_sr, underval_rate_sr = to_theorical_price_and_rate(
        real_price_sr,
        mk_eps_ls(),
    )
    terms = find_undervalued_terms(underval_rate_sr, underval_target_rate=0.2)

    assert len(terms) == 1
    assert terms[0].interval == (date(2024, 10, 19), date(2024, 12, 12))

    catchup_date = find_latest_catch_up_date(terms[0], underval_rate_sr)
    assert catchup_date is not None
    assert catchup_date.date == date(2024, 12, 23)

    # 可視化
    df = pd.concat([real_price_sr, theoretical_price_sr], axis=1)  # DataFrameにまとめる
    target_rates = [0, 0.1, 0.15, 0.2]
    for r in target_rates:
        aboves = find_undervalued_terms(underval_rate_sr, underval_target_rate=r)
        catchups = [find_latest_catch_up_date(a, underval_rate_sr) for a in aboves]

        dates = flatten([above.interval for above in aboves])
        # df = pd.concat([real_price_sr, theoretical_price_sr], axis=1)
        # saveimg(
        #     df,
        #     f"threo_real_price_{r}",
        #     ax_proces=(
        #         add_axes_span([a.interval for a in aboves]),
        #         add_axes_vertical_line([c.date for c in catchups if c is not None]),
        #     ),
        # )
