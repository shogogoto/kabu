"""usecase."""

import pandas as pd

from kabu.features.undervalued_search.domain import (
    resample_eps_to_daily,
    to_theorical_price_and_rate,
)
from kabu.features.undervalued_search.domain.service import (
    find_undervalued,
    save_undervalued_img,
    to_result,
)
from kabu.features.undervalued_search.repo.source import get_eps_from_jquants
from kabu.shared.source.stock_price import get_stock_price


def search_undervalued(
    code: str,
    r_target: float,
    start_yyyymmdd: str = "20230613",
    end_yyyymmdd: str = "20250613",
    save_img: bool = False,  # noqa: FBT001, FBT002
):
    """全部まとめた.

    Args:
        code: 銘柄コード
        r_target: r < 理論株価 - 実株価 / 理論株価 な期間を絞る割安比率
        start_yyyymmdd: 検索期間の始まり
        end_yyyymmdd: 検索期間の終わり
    Returns:
        割安期間と追いつき日とそれぞれの日の実株価と利益のリスト
        割安期間: 割安ターゲット比よりも割安な期間
        買い時 = 追いつき日 + 1
        株価
            割安期間
            買いタイミング
        利益 = 買い時 - 割安開始日

    """
    eps_ls = get_eps_from_jquants(code, start_yyyymmdd, end_yyyymmdd)
    eps_daily = resample_eps_to_daily(eps_ls)

    start_date = eps_daily.index.min()
    end_date = eps_daily.index.max()
    price_raw = get_stock_price(code, start_date, end_date)["Open"]

    theo_price, r_underval = to_theorical_price_and_rate(price_raw, eps_ls)
    df = pd.concat([price_raw, theo_price], axis=1)

    # locで使うための補間済み株価を作成
    all_days = pd.date_range(start=start_date, end=end_date, freq="D")
    price = price_raw.reindex(all_days, method="bfill")

    terms, catchups = find_undervalued(r_underval, r_target)
    results = []
    for term, catchup in zip(terms, catchups, strict=False):
        results.append(
            to_result(code, start_date, end_date, r_target, term, catchup, price),
        )

    if save_img:
        save_name = f"{code}_{r_target}"
        save_undervalued_img(df, terms, catchups, save_name)
    return pd.DataFrame(results)
