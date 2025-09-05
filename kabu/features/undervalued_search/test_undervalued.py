"""割安検索テスト."""

import pandas as pd

from kabu.features.undervalued_search.domain import (
    resample_eps_to_daily,
    to_theorical_price_and_rate,
)
from kabu.features.undervalued_search.domain.service import (
    find_undervalued,
)
from kabu.features.undervalued_search.repo.source import get_eps_from_jquants
from kabu.shared.source.stock_price import get_stock_price


def test_get_eps():
    """EPS取得テスト."""
    code = "8473"
    eps_ls = get_eps_from_jquants(code)
    eps_daily = resample_eps_to_daily(eps_ls)

    start_date = eps_daily.index.min()
    end_date = eps_daily.index.max()
    price = get_stock_price(code, start_date, end_date)["Open"]

    theo_price, r_underval = to_theorical_price_and_rate(price, eps_ls)
    df = pd.concat([price, theo_price], axis=1)  # DataFrameにまとめる
    target_rates = [0.1, 0.15, 0.2]
    for r in target_rates:
        save_name = f"{code}_{r}"
        _terms, _catchups = find_undervalued(r_underval, r)
        # save_undervalued_img(df, terms, catchups, save_name)
